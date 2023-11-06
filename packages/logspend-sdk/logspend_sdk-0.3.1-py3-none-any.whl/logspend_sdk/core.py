import time
import uuid
import asyncio
import httpx
import logging

from logspend_sdk.constants import SDK_VERSION

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LogBuilder:
    def __init__(self, input_data):
        """
        Initializes a new instance of LogBuilder.

        :param input_data: dict - A dictionary containing the initial input data for the LLM call log, e.g. prompt, model and model parameters like temperature, max_tokens.
        """
        self.data = {
            "input": input_data,
            "output": None,
            "custom_properties": None,
            "start_time_ms": int(time.time() * 1000),
            "end_time_ms": None,
            "request_id": str(uuid.uuid4()),
        }

    def set_output(self, output_data):
        """
        Sets the output data from the LLM generation call.

        :param output_data: dict - A dictionary containing the output data of the LLM log, this includes the generated text.
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        if not self.data["output"]:
            self.data["output"] = output_data
            if not self.data["end_time_ms"]:
                self.data["end_time_ms"] = int(time.time() * 1000)
        return self

    def set_custom_properties(self, custom_properties_data):
        """
        Sets custom properties for the LLM log. This could be a user_id, generation_id, session_id, etc.

        :param custom_properties_data: dict - A dictionary containing custom properties to be added to the log.
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["custom_properties"] = custom_properties_data
        return self
    
    def set_start_time(self, start_time):
        """
        Sets the start time of the log event, representing when the LLM call request was made.
        This is used to estimate the latency.

        :param start_time: float - A floating-point number representing the start time. 
                                  This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["start_time_ms"] = int(start_time * 1000)
        return self
    
    def set_end_time(self, end_time):
        """
        Sets the end time of the log event, representing when the LLM call response was received from the server.
        This is used to estimate the latency.

        :param end_time: float - A floating-point number representing the end time. 
                                This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["end_time_ms"] = int(end_time * 1000)
        return self

    def build(self):
        """
        Finalizes and returns the constructed log data.

        :return: dict - A dictionary containing the structured log data.
        """
        return self.data


class LogSpendLogger:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
                
    def send(self, data):
        async def async_send(data):
            # Check if input and output are defined
            if not data.get("input") or not data.get("output"):
                logger.warning("Input or Output data missing. Will skip sending the log.")
                return None
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "LogSpend-SDK-Version": SDK_VERSION,
                "LogSpend-Project-ID": self.project_id,
                "LogSpend-Request-ID": data["request_id"]
            }

            timeout_duration = 0.5  # 500 milliseconds
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post("https://api.logspend.com/llm/v1/log", headers=headers, json=data, timeout=timeout_duration)
                    return data["request_id"]
                except Exception as e:
                    logger.error(f"Error sending data: {e}")
                    
                    
        # Get or create an event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # No current loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # If loop is already running, use run_coroutine_threadsafe, else use run_until_complete
        if loop.is_running():
            # Loop already running, for example in an async application
            future = asyncio.run_coroutine_threadsafe(async_send(data), loop)
            return future.result()
        else:
            # This will be the common scenario, where the loop isn't running and needs to be started
            return loop.run_until_complete(async_send(data))
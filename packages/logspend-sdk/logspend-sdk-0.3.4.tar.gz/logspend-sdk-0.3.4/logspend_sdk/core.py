import time
import uuid
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
            "output": {},
            "custom_properties": {},
            "start_time_ms": int(time.time() * 1000),
            "end_time_ms": 0,
            "latency_ms": 0,
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
    
    def set_latency(self, latency):
        """
        Sets the latency in milliseconds, representing the elapsed time between the start time (when the LLM request was made)
        and the end time (when the LLM response was received from the server).
        Example: 
        start_time = time.time()
        # Make LLM call ...
        end_time = time.time()
        latency = end_time - start_time

        :param end_time: float - A floating-point number representing the difference between the end time and start time. 
                                This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["latency_ms"] = int(latency * 1000)
        return self

    def build(self):
        """
        Finalizes and returns the constructed log data.

        :return: dict - A dictionary containing the structured log data.
        """
        return self.data


class LogSpendLogger:
    def __init__(self, api_key, project_id, api_url="https://api.logspend.com/llm/v1/log"):
        self.api_key = api_key
        self.project_id = project_id
        self.api_url = api_url
                
    def send(self, data):
        # Check if input and output are defined
        if not data.get("input") or not data.get("output"):
            logger.warning("Input or Output data missing. Will skip sending LLM log to LogSpend.")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "LogSpend-SDK-Version": SDK_VERSION,
            "LogSpend-Project-ID": self.project_id,
            "LogSpend-Request-ID": data["request_id"]
        }

        timeout_duration = 0.5  # max timeout 500 milliseconds
        with httpx.Client() as client:
            try:
                response = client.post(self.api_url, headers=headers, json=data, timeout=timeout_duration)
                # Check if the request was successful
                if response.is_success:
                    response_data = response.json()
                    return response_data["data"]["request_id"]
                else:
                    logger.error(f"HTTP Error when sending LLM log to LogSpend: {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"Error sending LLM log to LogSpend: {e}")
                return None
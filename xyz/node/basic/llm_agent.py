""" 
========
LLMAgent
========
@file_name: llm_agent.py
@description:

This module implements an agent that processes messages using an LLM (Language Learning Model). Its primary function is
to process messages with a predefined template and then utilize various language models for further processing.

## Features of the LLMAgent include:
1. Template Usage: The agent utilizes a template, which is a list of strings formatted in OpenAI’s message structure.
    The text content within this template can be dynamically formatted using f-strings.
2. LLM Client: The agent includes a llm_client for invoking language model APIs. **Currently**, we use the OpenAI API.
    Users can also create their own LLM API by emulating the code found in `utils.llm.openai_client`.
3. Streaming Option: The agent has a stream parameter that controls whether the assistant’s messages are processed in a
    streaming manner.
4. Original Response Control: There is an original_response parameter that determines whether to return the raw
    response. If original_response is set to True, the raw response is returned; otherwise, only the content part is
        returned.

## Motivation
When creating a llm based agent, we need to pass messages and tools to the API. However, these items often require
    preprocessing before being sent. This agent facilitates this process, simplifying the engineering of prompts.
"""

import string
from copy import deepcopy
from typing import Generator, Any

from xyz.node.agent import Agent
from xyz.utils.llm.openai_client import OpenAIClient

__all__ = ["LLMAgent"]


class LLMAgent(Agent):
    """ 
    An assistant that uses the LLM (Language Learning Model) for processing messages.
    """
    information: dict
    llm_client: OpenAIClient
    last_request_info: dict
    node_config: dict
    template: list
    generate_parameters: dict
    stream: bool
    original_response: bool

    def __init__(self, template: list, llm_client: OpenAIClient,
                 stream: bool = False, original_response: bool = False) -> None:
        # noinspection PyUnresolvedReferences
        """
        Initialize the assistant with the given template and core agent.

        Parameters
        ----------
        template: list
            The template for the assistant's prompts. It should be a list of OpenAI's messages.
        llm_client: OpenAIClient
            The core agent for the assistant.
        stream: bool, optional
            Whether to stream the assistant's messages, by default False.
        original_response: bool, optional
            Whether to return the original response, by default False.
        """
        super().__init__()

        self.llm_client = llm_client

        self.template = template
        self.stream = stream
        self.original_response = original_response

        self.last_request_info = {}

    def flowing(self, messages: list = None,
                tools: list = None,
                images: list = None, **kwargs) -> str | Generator[str, None, None]:
        """When you call this assistant, we will run the assistant with the given keyword arguments from the prompts.
        Before we call the OpenAI's API, we do some interface on this message.

        Parameters
        ----------
        messages: list, optional
            The messages to use for completing the prompts, by default None.
        tools: list, optional
            The tools to use for completing the prompts, by default None.
        images: list, optional
            The images to use for completing the prompts, by default None.
        **kwargs
            The placeholders in the templates' text. They will be used to complete the prompts.

        Returns
        -------
        str/generator
            The response from the assistant. If stream == True, we will return a generator.
        """

        local_messages, messages = self._reset_default_list(messages)
        local_tools, tools = self._reset_default_list(tools)
        local_messages.extend(self._complete_prompts(**kwargs))

        return self.request(messages=local_messages, tools=local_tools, images=images)

    def request(self, messages: list, tools: list, images: list) -> str | Generator[str, None, None]:
        """
        Run the assistant with the given messages tools and images.
        """

        self.last_request_info = {
            "messages": messages,
            "tools": tools
        }

        if self.stream:
            return self._stream_run(messages=messages, images=images)
        else:
            response = self.llm_client.run(messages=messages, tools=tools, images=images)
            if self.original_response:
                return response

            content = response.choices[0].message.content

            if content is None:
                return response.choices[0].message.tool_calls[0].function
            else:
                return content

    def _stream_run(self, messages: list, images: list) -> Generator[str, None, None]:
        """
        Run the assistant in a streaming manner with the given messages or images.

        Parameters
        ----------
        messages: list
            The messages which be used for call the LLM API.

        Returns
        -------
        generator
            The generator for the token(already be decoded) in assistant's messages.
        """

        return self.llm_client.stream_run(messages=messages, images=images)

    def debug(self) -> dict[Any, Any]:
        """
        Reset the assistant's messages.

        Returns
        -------
        dict
            The last time the request messages, tools and images.
        """

        return self.last_request_info

    @staticmethod
    def _reset_default_list(parameter) -> tuple[list, Any]:
        """
        Reset the parameters in a method to the default values.

        Reason
        ------
        In Python's object methods, if a parameter has a default value, this value is only assigned at the initial
        invocation. Should the parameter's value be altered in subsequent calls, the modified value persists and is used
        in future invocations, rather than reverting to the original default value. This behavior highlights the
        importance of carefully managing mutable defaults to avoid unintended side effects in object state across method
        calls.

        Parameters
        ----------
        parameter
            The parameter to reset.

        Returns
        -------
        tuple
            The value of this parameter in this time, and reset the parameter to None.
        """

        if parameter is None:
            local = []
        else:
            local = deepcopy(parameter)
            parameter = None

        return local, parameter

    def _complete_prompts(self, **kwargs) -> list:
        """
        Complete the assistant's prompts with the given keyword arguments.

        Parameters
        ----------
        **kwargs
            They are the placeholders in the templates' text.

        Returns
        -------
        tuple
            A tuple containing the system message and the user message.
        """

        if type(self.template) is list:

            current_messages = deepcopy(self.template)

            for i in range(len(current_messages)):

                if isinstance(current_messages[i]['content'], str):
                    try:
                        current_messages[i]['content'] = current_messages[i]['content'].format(**kwargs)
                    except KeyError:
                        variables = self.get_variables_from_fstring(current_messages[i]['content'])
                        not_provided = [var for var in variables if var not in kwargs]
                        raise ValueError(f"Missing required arguments: {not_provided} when calling the LLMAgent.")
                elif isinstance(current_messages[i]['content'], list):
                    for j in range(len(current_messages[i]['content'])):
                        try:
                            current_messages[i]['content'][j]['content'] = current_messages[i]['content'][j][
                                'content'].format(**kwargs)
                        except KeyError:
                            variables = self.get_variables_from_fstring(current_messages[i]['content'][j]['content'])
                            not_provided = [var for var in variables if var not in kwargs]
                            raise ValueError(f"Missing required arguments: {not_provided} when calling the LLMAgent.")

            return current_messages

    @staticmethod
    def get_variables_from_fstring(fstring):
        formatter = string.Formatter()
        return [name for _, name, _, _ in formatter.parse(fstring) if name is not None]

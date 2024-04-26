"""
============
OpenAIClient
============
@file_name: openai_client.py
@description:
This module provides an interface to interact with OpenAI services. We have encapsulated the functionality into a simple
-to-use class, enabling users to easily interface with OpenAI.

## Initialization
Users initialize the OpenAIClient by specifying the api_key and generate_args:

- `api_key`: The API key for OpenAI. This must be obtained from your OpenAI account.
- `generate_args`: Arguments for the chat completion request. For detailed information on these parameters, refer to the
 OpenAI documentation. https://platform.openai.com/docs/api-reference/chat/create

## Methods
The class includes two primary methods for interacting with OpenAI:

- `run`: This method is used to make standard requests to OpenAI. It accepts messages, images, and optionally tools as
parameters:
    - `messages`: A list of strings, each representing a conversation turn.
    - `images`: A list of URLs pointing to images to be included in the request.
    - `tools`: An optional list that specifies additional tools to be used in the request.
- `stream_run`: This method is designed for streaming requests to OpenAI and also requires the messages and images
parameters.
These methods simplify the process of integrating OpenAI functionalities into your applications, allowing for both
standard and streaming interactions.

## Motivation
Certainly, it's possible to use OpenAI's API directly, but by encapsulating it within a class, we can **simplify** the
process and make it more convenient for users to utilize OpenAI's services. Most importantly, this approach enhances
code reusability. Parameters commonly used in API requests can be encapsulated as arguments to class methods.
"""


import os
import time
import traceback
from typing import Generator

from dotenv import load_dotenv
from openai import OpenAIError
from openai import OpenAI
from openai import Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

__all__ = ["OpenAIClient"]


class OpenAIClient:
    """
    The OpenAI client which uses the OpenAI API to generate responses to messages.
    """
    client: OpenAI
    generate_args: dict
    last_time_price: float

    def __init__(self, api_key=None, **generate_args):
        """Initializes the OpenAI Client.

        Parameters
        ----------
        api_key : str, optional
            The OpenAI API key.
        generate_args : dict, optional
            Arguments for the chat completion request.
            ref: https://platform.openai.com/docs/api-reference/chat/create
        """

        try:
            if api_key is None:
                load_dotenv()
                api_key = os.getenv('OPENAI_API_KEY')
            self.client = OpenAI(api_key=api_key)
        except OpenAIError:
            raise OpenAIError("The OpenAI client is not available. Please check the OpenAI API key.")

        # Set the default generate arguments for OpenAI's chat completions
        self.generate_args = {
            "model": "gpt-4-turbo",
            "temperature": 0.,
            "top_p": 1.0
        }
        # If the user provides generate arguments, update the default values
        self.generate_args.update(generate_args)

    def run(self, messages: list, tools: list = None,
            images: list = None) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Run the assistant with the given messages.

        Parameters
        ----------
        messages : list
            A list of messages to be processed by the assistant.
        tools : list, optional
            A list of tools to be used by the assistant, by default [].
        images : list, optional
            A list of image URLs to be used by the assistant, by default [].

        Returns
        -------
        str
            The assistant's response to the messages.

        Raises
        ------
        OpenAIError
            There may be different errors in different situations, which need to be handled according to the actual
                situation. An error message is printed in the console when an error is reported.
            ref: https://platform.openai.com/docs/guides/error-codes/python-library-error-types
        """

        if images:
            last_message = messages.pop()
            text = last_message['content']
            content = [
                {"type": "text", "text": text},
            ]
            for image_url in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                })
            messages.append({
                "role": last_message['role'],
                "content": content
            })

        # If the user provides tools, use them; otherwise, this client will not use any tools
        if tools:
            tool_choice = "auto"
            local_tools = tools
            # noinspection PyUnusedLocal
            tools = None  # pyright: ignore[reportIncompatibleVariableOverride]
        else:
            local_tools = []
            tool_choice = "none"

        get_response_signal = False
        count = 0
        while not get_response_signal and count < 10:
            try:
                # In OpenAI's api, if we request with tools == [], it will make an error. Caz the OpenAI use the default
                # value is 'NOT_GIVEN' which is a special type designed by them.
                if tool_choice == "auto":
                    response = self.client.chat.completions.create(
                        messages=messages,
                        tools=local_tools,
                        tool_choice="auto",
                        **self.generate_args
                    )
                else:
                    response = self.client.chat.completions.create(
                        messages=messages,
                        **self.generate_args
                    )
                get_response_signal = True

                return response
            except OpenAIError:
                count += 1
                error_message = str(traceback.format_exc())
                print(f"The error: {error_message}")
                print(f"The messages: {messages}")
                if count < 10:
                    print("We will try again in 2 seconds.")
                time.sleep(2)

    def stream_run(self, messages: list, images: list) -> Generator[str, None, None]:
        """
        Run the assistant with the given messages in a streaming manner.

        Parameters
        ----------
        images : list
            A list of image URLs to be used by the assistant.
        messages : list
            A list of messages to be processed by the assistant.

        Yields
        ------
        str
            The assistant's response to the messages, yielded one piece at a time.

        Raises
        ------
        OpenAIError
            There may be different errors in different situations, which need to be handled according to the actual
                situation. An error message is printed in the console when an error is reported.
            ref: https://platform.openai.com/docs/guides/error-codes/python-library-error-types
        """

        if images:
            last_message = messages.pop()
            text = last_message['content']
            content = [
                {"type": "text", "text": text},
            ]
            for image_url in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                })
            messages.append({
                "role": last_message['role'],
                "content": content
            })

        get_response_signal = False
        count = 0
        while not get_response_signal and count < 10:
            try:
                for response in self.client.chat.completions.create(
                        messages=messages,
                        stream=True,
                        timeout=5,
                        **self.generate_args
                ):
                    if response.choices[0].delta.content is None:
                        return None
                    else:
                        text = response.choices[0].delta.content
                        yield text
            except OpenAIError:
                count += 1
                error_message = str(traceback.format_exc())
                print(f"The error: {error_message}")
                print(f"The messages: {messages}")
                time.sleep(2)

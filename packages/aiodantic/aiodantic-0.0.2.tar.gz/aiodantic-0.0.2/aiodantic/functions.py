from abc import ABC
from typing import Any, List, Optional, Type, TypeVar

import openai
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from .utils import handle  # pylint: disable=E0401

T = TypeVar("T")
P = ParamSpec("P")


class FunctionCall(BaseModel):
    """
    Datastructure for rendering function calls
    """

    name: str
    data: Any


class OpenAIFunction(BaseModel, ABC):
    """
    OpenAI Function
    ---------------

    Schema-driven natural language function orchestration engine, powered by OpenAI functions feature and Pydantic.

    It enables the users to easily create and orchestrate functions that can be called from a natural language interface by defining the input schema and implementing the execution logic.

    The schema is defined using Pydantic models, and the execution logic is implemented by overriding the `run` method.

    It's an abstract class, so it can't be instantiated directly, but it can be subclassed to create new functions.

    Example:

    ```python

    import asyncio

    from typing import Any, Optional

    from pydantic import BaseModel

    from liferay_llm import OpenAIFunction

    class AddFunction(OpenAIFunction):
        '''
        Adds two numbers
        '''

        x: int
        y: int

        async def run(self, **kwargs: Any):
            return self.x + self.y

    async def main():
        print(await function_call("add 2 and 3"))

    if __name__ == "__main__":
        asyncio.run(main())

    >>> 5

    ```
    """

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        _schema = cls.schema()
        if cls.__doc__ is None:
            raise ValueError(
                f"OpenAIFunction subclass {cls.__name__} must have a docstring"
            )
        cls.openaischema = {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    k: v for k, v in _schema["properties"].items() if k != "self"
                },
                "required": _schema.get("required", []),
            },
        }

    @handle
    async def __call__(self, **kwargs: Any) -> FunctionCall:
        response = await self.run(**kwargs)
        return FunctionCall(name=self.__class__.__name__, data=response)

    async def run(self, **kwargs: Any) -> Any:
        """Main function to be implemented by subclasses"""
        raise NotImplementedError


@handle
async def parse_openai_function(
    response: dict[str, Any],
    functions: List[Type[OpenAIFunction]] = OpenAIFunction.__subclasses__(),
) -> FunctionCall:
    """Parses the response from the OpenAI API and returns a FunctionCall object, meant to have an uniform interface for rendering the response"""
    choice = response["choices"][0]["message"]
    if "function_call" in choice:
        function_call_ = choice["function_call"]
        name = function_call_["name"]
        arguments = function_call_["arguments"]
        print(name, arguments)
        for i in functions:
            if i.__name__ == name:
                result = await i.parse_raw(arguments)()  # type: ignore
                break
        else:
            raise ValueError(f"Function {name} not found")
        return result
    return FunctionCall(name="chat", data=choice["content"])


@handle
async def function_call(
    text: str,
    model: str = "gpt-3.5-turbo-16k-0613",
    functions: List[Type[OpenAIFunction]] = OpenAIFunction.__subclasses__(),
    **kwargs: Any,
) -> FunctionCall:
    """Given the user input, it will infer the appropiate function to call and it's `json_schema`, then it will call the function and return a FunctionCall object"""
    messages = [
        {"role": "user", "content": text},
        {"role": "system", "content": "You are a function Orchestrator"},
    ]
    response = await openai.ChatCompletion.acreate(  # type: ignore
        model=model,
        messages=messages,
        functions=[func.openaischema for func in functions],
    )
    return await parse_openai_function(response, functions=functions, **kwargs)  # type: ignore


@handle
async def chat_completion(text: str, context: Optional[str] = None) -> str:
    """

    Chat Completion
    ---------------

    Args:

                    text (str): The text to generate from

                    context (Optional[str], optional): The context to generate from. Defaults to None.

    Returns:

                    str: The generated text

    Simple chat completion outside agent context
    """

    if context is not None:
        messages = [
            {"role": "user", "content": text},
            {"role": "system", "content": context},
        ]
    else:
        messages = [{"role": "user", "content": text}]
    response = await openai.ChatCompletion.acreate(  # type: ignore
        model="gpt-3.5-turbo-16k-0613", messages=messages
    )
    return response["choices"][0]["message"]["content"]  # type: ignore


@handle
async def instruction(
    text: str, temperature: float = 0.2, max_tokens: int = 1024
) -> str:
    """

    Instruction Completion
    ---------------

    Args:

                    text (str): The text to generate from

    Returns:

                    str: The generated text

    Simple instruction completion outside agent context
    """
    response = await openai.Completion.acreate(  # type: ignore
        model="gpt-3.5-turbo-instruct",
        prompt=text,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    return response.choices[0].text  # type: ignore


async def instruction_stream(
    text: str, temperature: float = 0.2, max_tokens: int = 1024
):
    """

    Instruction Completion
    ---------------

    Args:

                    text (str): The text to generate from

    Returns:

                    str: The generated text

    Simple instruction completion outside agent context
    """
    response = await openai.Completion.acreate(  # type: ignore
        model="gpt-3.5-turbo-instruct",
        prompt=text,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    async for i in response:
        yield i.choices[0].text  # type: ignore

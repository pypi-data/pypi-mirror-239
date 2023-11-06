import os
from typing import AsyncGenerator

from pydantic import Field

import openai

from .schema import (
    AudioRequest,
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionRequest,
    CompletionResponse,
    Embedding,
    Message,
    Query,
    QueryBuilder,
    QueryRequest,
    QueryResponse,
    UpsertRequest,
    UpsertResponse,
)
from .service import APIClient
from .typedef import (
    AudioFormat,
    AudioModel,
    ChatModel,
    CompletionModel,
    Dict,
    EmbeddingModel,
    ImageFormat,
    ImageModel,
    List,
    Literal,
    OpenAIResource,
    Size,
    Vector,
)
from .utils import handle


class ChatGPT(OpenAIResource):
    """OpenAI Chat Completion API.
    ---
    ChatGPT: A Chat Generative Pretrained Transformer, is a SOAT Large Language model trained on 175 billion parameters with the Reinforcement Learning with Human Feedback technique, a novel invention launched in November's 2022 it's currently enhancing human capabilities around the world in a fast paced way unseen before, you can read more about it at the [OpenAI blog post](https://openai.com/blog/chatgpt).
    """

    model: ChatModel = Field(default="gpt-3.5-turbo-16k")

    @handle
    async def run(self, text: str, context: str):  # type: ignore
        """
        Given an input text and a computed context, decorated with the `handle` utility, this method safely makes calls to the OpenAI Chat Completion API with the appropiate format for an user-llm conversation that has a context window which can store additional contextual information such as memory, similarity retrieval or customized prompts to enforce the behavior of the model for any specific use case. The computation of this context window is up to the user, however sensible defaults such as `retrieval augmented generation` are provided out of the box.

        Args:
            text (str): The user input text.
            context (str): The computed context window.

        Raises:
            NotImplementedError: when an action regarding the retrieval engine which is not implemented is requested.

        Returns:

            ChatCompletionResponse: The response object from the OpenAI Chat Completion API.
        """
        request = ChatCompletionRequest(
            messages=[Message(content=text), Message(content=context, role="system")]
        )
        response = await openai.ChatCompletion.acreate(**request.dict())  # type: ignore
        return ChatCompletionResponse(**response)  # type: ignore

    async def stream(self, text: str, context: str) -> AsyncGenerator[str, None]:
        """
        Similar to the `run` method, but instead of returning a response object, it yields the response chunks of the response message as they are received from the OpenAI Chat Completion API.

        Args:
            text (str): The user input text.
            context (str): The computed context window.

        Raises:
            NotImplementedError: when an action regarding the retrieval engine which is not implemented is requested.

        Yields:
            AsyncGenerator[str, None]: The response chunks of the response message as they are received from the OpenAI Chat Completion API.
        """

        request = ChatCompletionRequest(
            messages=[Message(content=text), Message(content=context, role="system")],
            stream=True,
        )
        response = await openai.ChatCompletion.acreate(**request.dict())  # type: ignore
        async for message in response:  # type: ignore
            data = message.choices[0].delta.get("content", "")  # type: ignore
            yield data  # type: ignore


class DaVinci(OpenAIResource):
    """OpenAI Completion API.
    ---
    Da Vinci is a former version of the GPT-3 model. Da Vinci is a series of text generations models which generate text following the transformer's architecture for a given input with the primary goal of following the input text, it was novel at the time of its release because it was on top of the few text generative models as of today is used for autocompletions, summarizations, translations, etc. and mostly non conversational instruct based tasks, it's drop-in replacement is gpt-3.5-turbo-instruct.
    Read more about it in the [OpenAI blog post](https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates).
    """

    model: CompletionModel = Field(default="gpt-3.5-turbo-instruct")

    @handle
    async def run(self, text: str):  # type: ignore
        """
        Given an input text, decorated with the `handle` utility, this method safely makes calls to the OpenAI Completion API with the appropiate format for an user-llm conversation with no context window.
        It is meant for simplier tasks that do not require a context window, such as summarization, translation, autocompletion, etc.

        Args:
            text (str): The user input text.

        Returns:

            CompletionResponse: The response object from the OpenAI Completion API.

        """

        request = CompletionRequest(prompt=text)
        response = await openai.Completion.acreate(**request.dict())  # type: ignore
        return CompletionResponse(**response)  # type: ignore

    async def stream(self, text: str) -> AsyncGenerator[str, None]:
        """

        Similar to the `run` method, but instead of returning a response object, it yields the response chunks of the response message as they are received from the OpenAI Completion API.

        Args:
            text (str): The user input text.

        Yields:
            AsyncGenerator[str, None]: The response chunks of the response message as they are received from the OpenAI Completion API.

        """

        request = CompletionRequest(prompt=text, stream=True)
        response = await openai.Completion.acreate(**request.dict())  # type: ignore
        async for message in response:  # type: ignore
            data = message.choices[0].get("text", "")  # type: ignore
            yield data  # type: ignore


class AdaEmbeddings(OpenAIResource):
    """OpenAI Embeddings API.
    ---
    Ada is a transformer-based language model that can be used to generate embeddings for text. It is trained on a variety of text sources, including books, scientific papers, and reddit comments. You can read more about it in the [OpenAI blog post](https://openai.com/blog/new-and-improved-embedding-model).
    """

    model: EmbeddingModel = Field(default="text-embedding-ada-002")

    @handle
    async def run(self, texts: List[str]) -> List[Vector]:  # type: ignore
        """

        Given a list of texts, decorated with the `handle` utility, this method safely makes calls to the OpenAI Embeddings API with the appropiate format for a list of texts.
        It's purpose is to convert a list of texts into a list of vectors that can be consumed by the vector database for further implementation of the `query` and `upsert` methods of the `VectorClient` class regarding the `retrieval augmented generation` use case.

        Args:
            texts (List[str]): The list of texts.

        Returns:

                List[Vector]: The list of vectors.

        """

        response = await openai.Embedding.acreate(input=texts, model=self.model)  # type: ignore
        return [r.embedding for r in response.data]  # type: ignore


class DallE(OpenAIResource):
    """OpenAI Image API.
    ---
    Dall-E is a neural network that generates images from text descriptions, for example: "an illustration of a baby daikon radish in a tutu walking a dog". While it can be used for image generation in general, it was trained on text paired with images, so it works best when the text describes something in the image. You can read more about it in the [OpenAI blog post](https://openai.com/blog/dall-e/).
    """

    model: ImageModel = Field(default="dall-e")
    size: Size = Field(default="1024x1024")
    format: ImageFormat = Field(default="url")

    @handle
    async def run(self, text: str, n: int = 1) -> List[str]:  # type: ignore
        """

        Given an input text, decorated with the `handle` utility, this method safely makes calls to the OpenAI Image API with the appropiate format to generate a set of images from the input text.

        Args:

            text (str): The input text.

            n (int, optional): The number of images to generate. Defaults to 1.

        Returns:

            List[str]: The list of images.

        """

        response = await openai.Image.acreate(prompt=text, n=n, size=self.size, response_format=self.format)  # type: ignore
        return [r[self.format] for r in response.data]  # type: ignore


class Whisper(OpenAIResource):
    """OpenAI Audio API.
    ---
    Whisper is a neural network that converts text to speech. It is trained on a variety of English language audio sources, including audiobooks, podcasts, and YouTube videos. You can read more about it in the [OpenAI blog post](https://openai.com/research/whisper).
    """

    model: AudioModel = Field(default="whisper-1")

    @handle
    async def run(self, content: bytes, audioformat: AudioFormat = "wav") -> str:  # type: ignore
        """

        Given an input text, decorated with the `handle` utility, this method safely makes calls to the OpenAI Audio API with the appropiate format to infer the text from the input audio.

        Args:

            content (bytes): The input audio.

            audioformat (AudioFormat, optional): The audio format. Defaults to "wav".

        Returns:

            str: The inferred text.

        """

        response = await openai.Audio.acreate(self.model, AudioRequest(file=content, format=audioformat)())  # type: ignore
        return response.get("text", "")  # type: ignore


class VectorClient(APIClient):
    """

    A client for the vector database.

    Args:

        base_url (str, optional): The base url of the vector database. Defaults to "https://api.pinecone.io".

        headers (Dict[str, str], optional): The headers to use for the requests. Defaults to {"api-key": os.getenv("PINECONE_API_KEY"), "Content-Type": "application/json", "Accept": "application/json"}.

    """

    base_url: str = Field(
        default_factory=lambda: os.getenv("PINECONE_URL", "https://api.pinecone.io")
    )
    headers: Dict[str, str] = Field(
        default_factory=lambda: {
            "api-key": os.getenv("PINECONE_API_KEY"),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    @property
    def embeddings(self) -> AdaEmbeddings:
        """

        Returns an instance of the `AdaEmbeddings` class to consume its methods.

        Returns:

            AdaEmbeddings: An instance of the `AdaEmbeddings` class.

        """
        return AdaEmbeddings()

    @handle
    async def upsert(self, embeddings: List[Embedding]) -> UpsertResponse:
        """
        Upserts embeddings into the vector database.

        Args:

                embeddings (List[Embedding]): The list of embeddings to upsert.

        Returns:

            UpsertResponse: The response object from the vector database.

        """
        response = await self.post(
            "/vectors/upsert",
            data={
                "vectors": [
                    UpsertRequest(
                        values=embedding.values, metadata=embedding.metadata
                    ).dict()
                    for embedding in embeddings
                ]
            },
        )
        assert response is not None, "Response is None"
        return UpsertResponse(**response)

    @handle
    async def query(
        self, expr: Query, vector: Vector, topK: int, includeMetadata: bool = True
    ) -> QueryResponse:
        """

        Queries the vector database.

        Args:

            expr (Query): The query expression.

            vector (Vector): The vector to query.

            topK (int): The number of results to return.

            includeMetadata (bool, optional): Whether to include metadata in the response. Defaults to True.

        Returns:

            QueryResponse: The response object from the vector database.

        """

        payload = QueryRequest(
            topK=topK,
            filter=expr,  # type: ignore
            vector=vector,
            includeMetadata=includeMetadata,
        ).dict()
        response = await self.post(
            "/query",
            data=payload,
        )
        assert response is not None, "Response is None"
        return QueryResponse(**response)

    @handle
    async def search(self, text: str, namespace: str, top_k: int = 5) -> List[str]:
        """Search for a text into a namespace

        Args:
            text (str): The text to search
            namespace (str): The namespace to search into
            top_k (int, optional): The number of results to return. Defaults to 5.

        Returns:
            List[str]: The list of results
        """
        response = await self.query(
            expr=(QueryBuilder("namespace") == namespace).query,
            vector=(await self.embeddings.run([text]))[0],
            topK=top_k,
            includeMetadata=True,
        )

        return [match.metadata["text"] for match in response.matches]  # type: ignore

    @handle
    async def run(
        self,
        text: str,
        namespace: str,
        vector: Vector,
        action: Literal["query", "upsert"],
    ):
        """Run a query or upsert a vector

        Args:
            text (str): The text to search
            namespace (str): The namespace to search into
            vector (Vector): The vector to upsert
            action (Literal["query", "upsert"]): The action to perform

        Raises:
            NotImplementedError: When an action that is not implemented is requested

        Returns:

            Union[List[str], int]: The list of results or the number of upserted vectors
        """

        if action == "query":
            response = await self.query(
                expr=(QueryBuilder("namespace") == namespace).query,
                vector=vector,
                topK=5,
                includeMetadata=True,
            )
            return [match.metadata["text"] for match in response.matches]  # type: ignore
        if action == "upsert":
            response = await self.upsert(
                [
                    Embedding(
                        values=vector, metadata={"text": text, "namespace": namespace}
                    )
                ]
            )
            return response.upsertedCount
        else:
            raise NotImplementedError("Action not implemented")

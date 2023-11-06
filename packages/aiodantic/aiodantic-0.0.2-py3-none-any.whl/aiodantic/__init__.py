from .functions import *
from .openai import *
from .schema import *
from .server import *
from .service import *
from .typedef import *
from .utils import *


class Agent(BaseModel):
    """
    First class interface for interacting with openai large scale language models.
    """

    namespace: str = Field(...)
    chat_completion: ChatGPT = Field(default_factory=ChatGPT)
    completion: DaVinci = Field(default_factory=DaVinci)
    embeddings: AdaEmbeddings = Field(default_factory=AdaEmbeddings)
    audio: Whisper = Field(default_factory=Whisper)
    image: DallE = Field(default_factory=DallE)
    vector: VectorClient = Field(default_factory=VectorClient)

    async def run(self, text: str) -> AsyncGenerator[str, None]:
        """
        Streams the response from chatcompletion using retrieval augmented generation technique
        """
        try:
            string = ""
            knn = await self.vector.search(text, self.namespace)
            context = "Suggestions from the knowledge base:\n\n" + "\n".join(knn)
            async for message in self.chat_completion.stream(text, context):
                string += message
                yield message
            response_vector = (await self.embeddings.run([string]))[0]
            await self.vector.run(
                text=string,
                namespace=self.namespace,
                vector=response_vector,
                action="upsert",
            )
        except Exception as e:
            yield e.__class__.__name__ + ": " + str(e)

    async def __call__(self, text: str):
        """
        Function calling orchestration
        """
        return await function_call(text)

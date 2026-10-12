from ollama._types import ChatResponse
from ollama import Client
from pathlib import Path

from app.LLMResponse import LLMResponse
# from ollama._client import Client

class LLM:
    PROMPT_DIR: Path =Path("app\\prompts")

    def __init__(self,model:str="qwen3:4b-instruct") -> None:
        self.client: Client = Client(host="http://localhost:11434")
        self.model: str = model
        self.system_prompt: str = self.load_prompts()

    def load_prompts(self) -> str:
        try:
            md_files = sorted(path for path in Path(self.PROMPT_DIR).rglob("*.md") if path.is_file()
            )

            if not md_files:
                raise FileNotFoundError(
                    f"No Markdown files found in: {self.PROMPT_DIR}"
                )

            system_prompt: str = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in md_files)

            return system_prompt.strip()

        except FileNotFoundError as error:
            raise RuntimeError(
                f"Failed to load prompts from: {self.PROMPT_DIR}"
            ) from error

    def interpret(self, text: str) -> LLMResponse:
        chat_response: ChatResponse = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            stream=False,
            # think=False,
        )

        llm_response: LLMResponse = LLMResponse(thinking=chat_response.message.thinking,
                                                content=chat_response.message.content)
        return llm_response

if __name__ == "__main__":
    llm = LLM(model="qwen3:4b")

    response = llm.interpret("Hola, gilipollas")

    print(response.thinking,f"\n{'-'*20}\n",response.content)
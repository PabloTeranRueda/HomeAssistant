from ollama._types import ChatResponse
from ollama import Client

from app.LLMResponse import LLMResponse
# from ollama._client import Client

class LLM:
    def __init__(self,model:str="qwen3:4b-instruct") -> None:
        self.client: Client = Client(host="http://localhost:11434")
        self.model: str = model
        self.system_prompt: str = self.load_prompt("system_role")

    def load_prompt(self,prompt_name:str) -> str:
        try:
            with open(f"app\\prompts\\{prompt_name}.md","r",encoding="utf-8") as prompt:
                contents = prompt.read()
        except FileNotFoundError as error:
            raise RuntimeError(
                f"System prompt not found: {prompt_name}"
            ) from error
        
        return contents.strip()

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
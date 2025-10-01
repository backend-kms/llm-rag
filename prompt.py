import config
from openai import OpenAI

class GPTClient:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # 원하는 GPT 모델명 (ex. "gpt-4o", "gpt-4o-mini", "gpt-4.1-mini")

    def generate_response(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            # reasoning={"effort": "low"}, # medium, high 등의 선택 옵션, 얼마나 깊게 추론할지 설정
            # instructions="",  # system 역할에 해당
            input=prompt
        )
        print(response)
        return f"Response to '{prompt}'"

client = GPTClient()
client.generate_response(prompt="2024년 미스터트롯 우승자는?")
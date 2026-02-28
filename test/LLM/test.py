import os
import openai


agent = openai.OpenAI()

response = agent.responses.create(
    model='gpt-5-nano',                     # 모델 선택
    reasoning={'effort': 'medium'},         # 추론 정도
    input="사용가능한 openai의 모델 종류"        
)

print(response)
# test.py
from promptmodel import PromptModel, Client

client = Client()

prompt = PromptModel("function_call_test").get_prompts()

# prompt = PromptModel("function_call_test").get_prompts()

from typing import Optional
def get_current_weather(location: str, unit: Optional[str]):
    return "13 degrees celsius"

    
# @client.register_agent("lawyer_bot")
# def lawyer_bot(user_message: str):
#     context = client.get_agent_context(agent_name="lawyer_bot")
    
#     res = PromptModel("func_1", use_in_agent=True, tag="agent").run() # 각 run 하나하나가 Agent 내에서 설정된 version을 가져온다
    
#     res = PromptModel("func_1", context = context).run() 
#     # 데코레이터 안에서 flag를 가지고 있거나, 데코레이터가 agent에 대해 설정된 모든 version을 미리 가져오고,
#     # PromptModel은 이게 있는지 확인해서 이를 사용한다
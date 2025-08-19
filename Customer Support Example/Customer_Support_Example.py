from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage

def add_exclamation(message: str) -> str:
    """add!!!!"""
    return f"{message}!!!!"

# ����һ���򵥵�ģ�Ϳͻ���
model_client = OpenAIChatCompletionClient(
    model="deepseek-chat", 
    api_key="sk-",
    base_url="https://api.deepseek.com",
    model_info={
        family: unknown
        function_calling: true
        json_output: false
        multiple_system_messages: true
        structured_output: true
        vision: false
    },
)

# ����һ���򵥵Ĵ�����������Ϣ����ϸ�̾��
simple_agent = AssistantAgent(
    "simple_agent",  # ��������
    model_client=model_client,
    handoffs=["user"],  # ֻ��һ������������������
    tools=[add_exclamation],  # ʹ�üӸ�̾�ŵĹ���
    system_message="""You are a simple agent that adds an exclamation mark to every response you generate.
    Just add "!" at the end of the response.""",
)

# ����ִ��ʱ���򵥴��������û����벢�Ӹ�̾��
async def run_team_stream() -> None:
    task = "Hello, how are you?"  # ��ʼ������
    task_result = await Console(simple_agent.run_stream(task=task))  # ��������������
    last_message = task_result.messages[-1]

    # �ȴ��û����벢����
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")  # ��ȡ�û�����
        task_result = await Console(
            simple_agent.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]��
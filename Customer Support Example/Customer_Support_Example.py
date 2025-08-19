from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage

def add_exclamation(message: str) -> str:
    """add!!!!"""
    return f"{message}!!!!"

# 创建一个简单的模型客户端
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

# 创建一个简单的代理，它会在消息后加上感叹号
simple_agent = AssistantAgent(
    "simple_agent",  # 代理名称
    model_client=model_client,
    handoffs=["user"],  # 只有一个代理，处理所有任务
    tools=[add_exclamation],  # 使用加感叹号的工具
    system_message="""You are a simple agent that adds an exclamation mark to every response you generate.
    Just add "!" at the end of the response.""",
)

# 任务执行时，简单代理将处理用户输入并加感叹号
async def run_team_stream() -> None:
    task = "Hello, how are you?"  # 初始化任务
    task_result = await Console(simple_agent.run_stream(task=task))  # 启动代理处理任务
    last_message = task_result.messages[-1]

    # 等待用户输入并处理
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        user_message = input("User: ")  # 获取用户输入
        task_result = await Console(
            simple_agent.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]，
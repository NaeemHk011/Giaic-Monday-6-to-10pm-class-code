from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner , function_tool, ModelSettings,enable_verbose_stdout_logging, RunHooks, RunContextWrapper
from agents.agent import StopAtTools

# enable_verbose_stdout_logging()
# High temperature (0.9) = More creative, varied responses
@function_tool
def weather_tool(city:str):
    """
    tell the weather of city
    """
    print('tool called')
    return f"the weather in {city} is cloudy"

@function_tool
def sum(num:int,num2:int):
    print('sum tool called')
    return num+num

Customer_support = Agent(
    name="customer support",
    instructions="You are a customer support agent use tool to give answer to user.",
    tools=[weather_tool,sum],
    tool_use_behavior=StopAtTools(
        stop_at_tool_names=['sum']
    ),
    model_settings=ModelSettings(
        parallel_tool_calls=True,
    )
    
)

class RunnerHook(RunHooks):
    def __init__(self):
        self.event_count = 0
        self.name = "TestHooks"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_count = self.event_count + 1
        print(f"### {self.name} {self.event_count}: Agent {agent.name} started")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent,output) -> None:
        
        print(f"### Agent {agent.name} ended with {output}")
        
        

start_hook = RunnerHook()
prompt=input('write your question here: ')
result = Runner.run_sync(Customer_support,prompt,hooks=start_hook)

print(result.final_output)

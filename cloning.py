from typing import Any
from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner , function_tool, RunContextWrapper,input_guardrail,GuardrailFunctionOutput, enable_verbose_stdout_logging,ModelSettings,AgentHooks
from pydantic import BaseModel
from dotenv import load_dotenv

enable_verbose_stdout_logging()

class myContext(BaseModel):
    inputType:str


def check_enabled(ctx:RunContextWrapper,agent:Agent)->bool:
    if ctx.context.inputType=='weather':
        return True
    else:
        return False

@function_tool(is_enabled=check_enabled)
def weather_tool(city:str):
    """
    tell the weather of city
    """
    print('tool called')
    return f"the weather in {city} is cloudy"


story_writer_agent_one = Agent(
    name="story writer agent one",
    instructions="you are a customer support agent use the weather tool to tell the weather and use sum tool to add two numbers",
    tools=[weather_tool],
    
)

context = myContext(
    inputType="useless"
)

result = Runner.run_sync(story_writer_agent_one,"what is the weather in karachi",context=context)
print(result.final_output)



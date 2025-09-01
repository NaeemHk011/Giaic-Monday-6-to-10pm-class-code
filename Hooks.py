from typing import Any
from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner , function_tool, RunContextWrapper,input_guardrail,GuardrailFunctionOutput, enable_verbose_stdout_logging,ModelSettings,AgentHooks
from pydantic import BaseModel
from dotenv import load_dotenv


class UserContext(BaseModel):
    usertype:str


def dynamic_instructions(ctx:RunContextWrapper[UserContext],agent:Agent)->str:
    if ctx.context.usertype=='normal user':
        return "You are a customer support agent. You should answer the question in a very simple way that a normal user can understand."
    elif ctx.context.usertype=='premium user':
        return "You are a customer support agent. You should answer the question in a very polite and in detail also say thank you."
    else:
        return "You are a customer support agent. according to the question answer it."



Customer_support = Agent(
    name="customer support",   
    instructions=dynamic_instructions,
)

userContext = UserContext(
    usertype='premium user'
)


prompt=input('write your question here: ')
result = Runner.run_sync(Customer_support,prompt,context=userContext)


context_data = RunContextWrapper(context=userContext) 

print("instructions>>>>",result.last_agent.instructions(ctx = context_data,agent = Customer_support))

print("finaloutput>>>>",result.final_output)
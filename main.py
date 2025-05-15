from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class InformationAgent(BaseModel):
    topic: str
    sumamry: str
    sources: list[str]
    tools_used: list[str]
    
    
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
llm = ChatOpenAI(model="gpt-4o")
parser = PydanticOutputParser(pydantic_object=InformationAgent)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
    
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
query = input("What can i help you with? ")
# raw_response = agent_executor.invoke({"query": "what is the capital of ghana?", "name": "Minnie"})
raw_response = agent_executor.invoke({"query": query})
print(raw_response)

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    # print("Error parsing response:", e, "Raw response:", raw_response)
    print("Error parsing response:", e)
    print("Raw response:", raw_response)

# structured_response = parser.parse(raw_response.get("output")[0]['text'])
# response = llm.invoke("What is a semiconductor?")
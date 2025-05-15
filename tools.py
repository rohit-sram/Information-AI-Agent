from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from pydantic import BaseModel

def save_to_txt(data:str, filename:str = 'research_output.txt'):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if isinstance(data, BaseModel):
        data = data.dict()
    if isinstance(data, dict):
        formatted_data = "\n".join([
            f"Topic: {data.get('topic', '')}",
            f"Summary:\n{data.get('summary', '')}",
            f"Sources:\n" + "\n".join(data.get("sources", [])),
            f"Tools Used: {', '.join(data.get('tools_used', []))}",
        ])
    else:
        formatted_data = data

    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{formatted_data}\n\n"

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(formatted_text)
        
    return f"Data saved successfully to {filename}"

save_tool = Tool(
    name='save_to_txt',
    # func=save_to_txt,
    func=lambda d: save_to_txt(d if isinstance(d, (dict, str)) else d.dict()),
    description="Saves structured research data to a text file."
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name='search',
    func=search.run,
    description="Search the Web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_char_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


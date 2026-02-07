import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1) LLM (OpenAI)
# Pick a model you have access to. "gpt-4o-mini" is commonly used for structured JSON tasks.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 2) Schema (Pydantic)
class Book(BaseModel):
    """Information about a book."""
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: int = Field(description="The year the book was published")

# 3) Parser + format instructions
parser = JsonOutputParser(pydantic_object=Book)
format_instructions = parser.get_format_instructions()

# 4) Prompt
template = ChatPromptTemplate.from_messages([
    ("system", "You output ONLY valid JSON that matches the schema exactly. No backticks."),
    ("human",
     "Generate JSON about the user input according to the format instructions.\n"
     "Input: {input}\n"
     "{format_instructions}"
    )
])

# 5) Chain
chain = template.partial(format_instructions=format_instructions) | llm | parser

# Single call
print(chain.invoke({"input": "East of Eden"}))

# Batch call
book_titles = ["Dune", "Neuromancer", "Snow Crash", "The Left Hand of Darkness", "Foundation"]
print(chain.batch([{"input": t} for t in book_titles]))

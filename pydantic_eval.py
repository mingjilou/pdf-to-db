import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.pydantic_v1 import BaseModel, Field


base_url = os.getenv("NVIDIA_BASE_URL")
model = 'meta/llama-3.1-8b-instruct'
llm = ChatNVIDIA(base_url=base_url, model=model, temperature=0)


book_template = ChatPromptTemplate.from_template('''\
Make a JSON object representing the details of the following book: {book_title}. \
It should have fields for:
- The title of the book.
- The author of the book.
- The year the book was originally published.

Only return the JSON. Never return non-JSON text including backtack wrappers around the JSON.''')

class Book:
    """Information about a book."""
    
    def __init__(self, title, author, year_of_publication):
        self.title = title
        self.author = author
        self.year_of_publication = year_of_publication

from langchain_core.pydantic_v1 import BaseModel, Field


class Book(BaseModel):
    """Information about a book."""

    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: str = Field(description="The year the book was published")


from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=Book)


format_instructions = parser.get_format_instructions()


print(format_instructions)

class Book(BaseModel):
    """Information about a book."""

    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: str = Field(description="The year the book was published")

template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that generates JSON and only JSON according to the instructions provided to you."),
    ("human", (
        "Generate JSON about the user input according to the provided format instructions.\n" +
        "Input: {input}\n" +
        "Format instructions {format_instructions}")
    )
])

chain = template | llm | parser # Created above with `parser = JsonOutputParser(pydantic_object=Book)`

chain.invoke({
    "input": "East of Eden",
    "format_instructions": format_instructions
})

chain = template.partial(format_instructions=format_instructions) | llm | parser # Created above with `parser = JsonOutputParser(pydantic_object=Book)`


book_titles = ["Dune", "Neuromancer", "Snow Crash", "The Left Hand of Darkness", "Foundation"]


chain.batch(book_titles)


city_names = ['Tokyo', 'Busan', 'Cairo', 'Perth']


class City(BaseModel):
    """Information about a city."""

    name: str = Field(description="The name of the city")
    country: str = Field(description="The the country the city is located in")
    capital: bool = Field(description="Is the city the capital of the country it is located in")
    population: int = Field(description="The population of the city")


template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that generates JSON and only JSON according to the instructions provided to you."),
    ("human", (
        "Generate JSON about the user input according to the provided format instructions.\n" +
        "Input: {input}\n" +
        "Format instructions {format_instructions}")
    )
])


parser = JsonOutputParser(pydantic_object=City)


template_with_format_instructions = template.partial(format_instructions=parser.get_format_instructions())

chain = template_with_format_instructions | llm | parser

chain.batch(city_names)
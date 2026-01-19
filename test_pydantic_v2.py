#!/usr/bin/env python
"""Test Pydantic v2 with LangChain and OpenAI"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test imports
print("Testing imports...")
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

print("✓ All imports successful!")

# Define a simple Pydantic v2 model
class Book(BaseModel):
    """Information about a book."""
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: int = Field(description="The year the book was published")

print("\n✓ Pydantic v2 BaseModel class defined successfully!")

# Test JsonOutputParser with Pydantic v2
parser = JsonOutputParser(pydantic_object=Book)
format_instructions = parser.get_format_instructions()
print("\n✓ JsonOutputParser works with Pydantic v2!")
print(f"\nFormat instructions preview:\n{format_instructions[:200]}...")

# Test API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"\n✓ API key loaded: {api_key[:20]}...{api_key[-4:]}")
    
    # Create LLM instance
    llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0)
    print("✓ ChatOpenAI instance created successfully!")
    
    # Test a simple structured output
    template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI that generates JSON and only JSON according to the instructions provided."),
        ("human", "Generate JSON about the book: {input}\n\nFormat instructions: {format_instructions}")
    ])
    
    chain = template.partial(format_instructions=format_instructions) | llm | parser
    print("✓ Chain created successfully!")
    
    print("\n" + "="*60)
    print("Testing with a real API call...")
    print("="*60)
    
    try:
        result = chain.invoke({"input": "The Great Gatsby"})
        print("\n✓ SUCCESS! Structured output generated:")
        print(f"  Title: {result.get('title')}")
        print(f"  Author: {result.get('author')}")
        print(f"  Year: {result.get('year_of_publication')}")
        print(f"\nFull result: {result}")
    except Exception as e:
        print(f"\n✗ API call failed: {e}")
else:
    print("\n✗ API key not found. Check your .env file.")

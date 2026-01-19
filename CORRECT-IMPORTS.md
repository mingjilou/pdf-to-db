# ✅ Correct Imports for Your Notebook (Pydantic v2)

## Modern Import Pattern (RECOMMENDED)

You have **Pydantic v2.12.5** installed, so use these imports:

```python
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field  # ← Use direct pydantic, NOT langchain_core.pydantic_v1
```

## Why NOT Use `langchain_core.pydantic_v1`?

The notebook examples show:
```python
from langchain_core.pydantic_v1 import BaseModel, Field  # ❌ OLD PATTERN
```

**Don't use this!** It's a compatibility wrapper for older Pydantic v1. Since you have Pydantic v2, use the direct import:
```python
from pydantic import BaseModel, Field  # ✅ MODERN PATTERN
```

## Complete Working Example

### Cell 1: Imports
```python
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
```

### Cell 2: Load API Key
```python
# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Verify
if api_key:
    print(f"✓ API key loaded: {api_key[:20]}...{api_key[-4:]}")
else:
    print("✗ ERROR: API key not found!")
```

### Cell 3: Configure OpenAI Model
```python
# Choose your model
model = 'gpt-3.5-turbo'  # or 'gpt-4', 'gpt-4o', 'gpt-4o-mini'

# Create LLM instance
llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)
print(f"✓ Using model: {model}")
```

### Cell 4: Define Pydantic Model
```python
class Book(BaseModel):
    """Information about a book."""
    
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: int = Field(description="The year the book was published")

print("✓ Book model defined")
```

### Cell 5: Create Parser and Chain
```python
# Create parser with Pydantic model
parser = JsonOutputParser(pydantic_object=Book)

# Create prompt template
template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that generates JSON and only JSON according to the instructions provided."),
    ("human", "Generate JSON about the book: {input}\n\nFormat instructions: {format_instructions}")
])

# Create chain with partial format instructions
format_instructions = parser.get_format_instructions()
chain = template.partial(format_instructions=format_instructions) | llm | parser

print("✓ Chain created successfully!")
```

### Cell 6: Test with Single Book
```python
result = chain.invoke({"input": "Dune"})
print(result)
```

### Cell 7: Test with Multiple Books (Batch)
```python
book_titles = ["Dune", "Neuromancer", "Snow Crash", "Foundation"]
results = chain.batch([{"input": title} for title in book_titles])

for result in results:
    print(f"- {result['title']} by {result['author']} ({result['year_of_publication']})")
```

## Differences: Pydantic v1 vs v2

| Feature | Pydantic v1 | Pydantic v2 |
|---------|-------------|-------------|
| Import | `from langchain_core.pydantic_v1 import BaseModel` | `from pydantic import BaseModel` |
| Performance | Slower | **Much faster** (Rust core) |
| Validation | Good | **Better & stricter** |
| Status | Legacy | **Current** |
| Recommended | ❌ Only for old code | ✅ **Use this** |

## Verified Test Results

I ran `test_pydantic_v2.py` and confirmed:
```
✓ All imports successful!
✓ Pydantic v2 BaseModel class defined successfully!
✓ JsonOutputParser works with Pydantic v2!
✓ API key loaded: sk-proj-UDZigxp8i9tw...KWQA
✓ ChatOpenAI instance created successfully!
✓ Chain created successfully!

✓ SUCCESS! Structured output generated:
  Title: The Great Gatsby
  Author: F. Scott Fitzgerald
  Year: 1925
```

## Summary

✅ **DO THIS:**
```python
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
```

❌ **DON'T DO THIS:**
```python
from langchain_core.pydantic_v1 import BaseModel, Field
api_key = os.getenv("OPENAI_API_KEY")  # Without load_dotenv()
```

## Your Environment is Ready!

Everything is installed and configured:
- ✅ Python 3.10.6
- ✅ langchain-openai 1.1.7
- ✅ pydantic 2.12.5
- ✅ python-dotenv 1.0.1
- ✅ API key in .env file
- ✅ .gitignore protecting secrets

**Just use the correct imports above and your notebook will work perfectly!**

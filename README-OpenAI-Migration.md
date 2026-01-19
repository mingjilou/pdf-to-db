# Migration Guide: NVIDIA to OpenAI API

This guide explains how to migrate your code from the NVIDIA environment to use OpenAI's API instead.

## Key Changes

### 1. **Import Statement**
**NVIDIA Version:**
```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA
```

**OpenAI Version:**
```python
from langchain_openai import ChatOpenAI
```

### 2. **Model Initialization**

**NVIDIA Version:**
```python
base_url = os.getenv("NVIDIA_BASE_URL")
model = 'meta/llama-3.1-8b-instruct'
llm = ChatNVIDIA(base_url=base_url, model=model, temperature=0)
```

**OpenAI Version:**
```python
api_key = os.getenv("OPENAI_API_KEY")
model = 'gpt-3.5-turbo'  # or 'gpt-4', 'gpt-4o', etc.
llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)
```

### 3. **Structured Output Support**

Both versions support the `with_structured_output` method, but OpenAI has more robust support:

```python
llm_structured = llm.with_structured_output(Book)
```

OpenAI models (especially GPT-4) have excellent native support for structured output generation.

## Installation Requirements

### Install Required Packages

```bash
pip install langchain-openai langchain-core
```

Or if you're using the complete LangChain package:

```bash
pip install langchain openai
```

### Complete Requirements List

Create a `requirements.txt` file:

```txt
langchain-openai>=0.0.2
langchain-core>=0.1.0
openai>=1.0.0
pydantic>=2.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Setup Instructions

### Step 1: Get Your OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Create a new API key
5. Copy and save it securely

### Step 2: Set Your API Key

**Option A: Environment Variable (Recommended)**

On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

On Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=your-api-key-here
```

On macOS/Linux:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: .env File**

Create a `.env` file in your project root:
```
OPENAI_API_KEY=your-api-key-here
```

Then load it in your code:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Option C: Direct in Code (Not Recommended for Production)**

```python
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

### Step 3: Choose Your Model

OpenAI offers several models with different capabilities and pricing:

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| `gpt-3.5-turbo` | Fast, cost-effective tasks | $ | Fast |
| `gpt-4o-mini` | Balanced performance | $$ | Fast |
| `gpt-4o` | High quality, complex tasks | $$$ | Medium |
| `gpt-4-turbo` | Most capable, complex reasoning | $$$$ | Slower |
| `gpt-4` | Legacy high-quality model | $$$$ | Slower |

**Recommendation:** Start with `gpt-3.5-turbo` for testing, then upgrade to `gpt-4o` or `gpt-4o-mini` for production if needed.

## Code Comparison

### Complete Example - NVIDIA Version
```python
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

base_url = os.getenv("NVIDIA_BASE_URL")
model = 'meta/llama-3.1-8b-instruct'
llm = ChatNVIDIA(base_url=base_url, model=model, temperature=0)

class Book(BaseModel):
    """Information about a book."""
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: int = Field(description="The year the book was published")

parser = JsonOutputParser(pydantic_object=Book)
template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that generates JSON."),
    ("human", "Input: {input}\nFormat instructions: {format_instructions}")
])

chain = template.partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({"input": "Dune"})
```

### Complete Example - OpenAI Version
```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

api_key = os.getenv("OPENAI_API_KEY")
model = 'gpt-3.5-turbo'
llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)

class Book(BaseModel):
    """Information about a book."""
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year_of_publication: int = Field(description="The year the book was published")

parser = JsonOutputParser(pydantic_object=Book)
template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that generates JSON."),
    ("human", "Input: {input}\nFormat instructions: {format_instructions}")
])

chain = template.partial(format_instructions=parser.get_format_instructions()) | llm | parser
result = chain.invoke({"input": "Dune"})
```

## Running the Notebook

1. Open the new notebook: `42-Pydantic-OpenAI.ipynb`
2. Ensure your OpenAI API key is set (see Step 2 above)
3. Run all cells sequentially
4. The code should work exactly the same as the NVIDIA version

## Troubleshooting

### Error: "No API key provided"
**Solution:** Make sure you've set the `OPENAI_API_KEY` environment variable.

### Error: "You exceeded your current quota"
**Solution:** Check your OpenAI account billing and add payment method at https://platform.openai.com/account/billing

### Error: "Module 'langchain_openai' not found"
**Solution:** Install the package:
```bash
pip install langchain-openai
```

### Error: "Rate limit exceeded"
**Solution:** OpenAI has rate limits. Add retry logic or reduce your request rate.

## Cost Considerations

OpenAI charges per token used. Approximate costs (as of 2024):

- **GPT-3.5-turbo:** ~$0.0015 per 1K tokens (input) / $0.002 per 1K tokens (output)
- **GPT-4o-mini:** ~$0.15 per 1M tokens (input) / $0.60 per 1M tokens (output)
- **GPT-4o:** ~$5 per 1M tokens (input) / $15 per 1M tokens (output)

For the examples in the notebook (processing 5 book titles), you'll typically use:
- ~500-1000 tokens total
- Cost: Less than $0.01 with GPT-3.5-turbo

## Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)
- [OpenAI Pricing](https://openai.com/pricing)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)

## Summary

The migration from NVIDIA to OpenAI is straightforward:
1. Change the import from `langchain_nvidia_ai_endpoints` to `langchain_openai`
2. Replace `ChatNVIDIA` with `ChatOpenAI`
3. Update initialization to use API key instead of base URL
4. Choose an appropriate OpenAI model
5. Everything else remains the same!

The rest of your LangChain code (prompts, chains, parsers, Pydantic models) works identically with both providers.

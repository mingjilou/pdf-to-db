# Quick Start Guide - OpenAI Notebook

## ✅ Setup Complete!

Your environment is now configured correctly:
- ✅ `langchain-openai` packages installed
- ✅ `.env` file created with your API key
- ✅ `python-dotenv` installed
- ✅ `.gitignore` configured to protect your API key

## How to Use Your Notebook

### Step 1: Update the API Key Cell in Your Notebook

Find the cell that looks like this:
```python
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

api_key = os.getenv("OPENAI_API_KEY")
```

**Replace it with this:**
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Verify the key is loaded
if api_key:
    print(f"✓ API key loaded: {api_key[:20]}...{api_key[-4:]}")
else:
    print("✗ ERROR: API key not found. Check your .env file.")
```

### Step 2: Verify Your Kernel

1. In VS Code, look at the **top-right corner** of your notebook
2. Click on the kernel selector (shows "Python 3.x.x")
3. Select: **Python 3.10.6** at `C:\Program Files\Python\Python310\python.exe`

### Step 3: Restart the Kernel

- Click the "Restart" button in the kernel selector
- This ensures all environment variables are loaded fresh

### Step 4: Run From the Beginning

Run all cells from the top in order. The first cell should be:
```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.pydantic_v1 import BaseModel, Field
```

Then the API key cell (from Step 1), then continue with the rest.

## Verification Cell

Add this cell right after loading the API key to verify everything works:

```python
# Verification: Test the setup
import sys
print("Python executable:", sys.executable)
print()

# Test imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.pydantic_v1 import BaseModel, Field
    print("✓ All imports successful!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Run: pip install langchain langchain-core langchain-openai pydantic")

# Test API key
if api_key:
    print(f"✓ API key loaded successfully")
    
    # Test a simple API call
    try:
        llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke("Say 'Hello, I am working!'")
        print(f"✓ OpenAI API connection successful!")
        print(f"  Response: {response.content}")
    except Exception as e:
        print(f"✗ API call failed: {e}")
else:
    print("✗ API key not loaded. Check your .env file.")
```

## Troubleshooting

### If imports still fail:
```python
# Run this in a notebook cell to install packages
import sys
!{sys.executable} -m pip install -U langchain langchain-core langchain-openai pydantic
```

### If API key is not found:
1. Check that `.env` file exists in the project root
2. Verify it contains: `OPENAI_API_KEY=your-key-here`
3. Restart the kernel after creating/modifying `.env`
4. Re-run the `load_dotenv()` cell

### If you get "kernel not found":
1. Install ipykernel: `pip install ipykernel`
2. Register the kernel: `python -m ipykernel install --user --name=python310`
3. Restart VS Code
4. Select the "Python 3.10.6" kernel

## Files Created

- `.env` - Contains your OpenAI API key (DO NOT commit to git)
- `.gitignore` - Prevents committing sensitive files
- `SOLUTION-Environment-Mismatch.md` - Detailed environment setup guide
- `SOLUTION-OpenAI-API-Key.md` - API key configuration guide
- `test_import.py` - Command-line test script

## Next Steps

Once everything is working:
1. Run through the notebook cells in order
2. Complete the exercises at the end
3. Experiment with different models and temperatures

## Security Reminder

🔒 **Your `.env` file contains your API key and is now protected by `.gitignore`**

- Never commit `.env` to version control
- Never share your API key publicly
- Monitor your usage at: https://platform.openai.com/usage

---

**Need Help?** Check the detailed solution files:
- `SOLUTION-Environment-Mismatch.md`
- `SOLUTION-OpenAI-API-Key.md`

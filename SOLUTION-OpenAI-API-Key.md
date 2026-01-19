# Solution: OpenAI API Key Configuration

## Problem
Getting error: `OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable`

## Root Cause
The notebook is calling `api_key = os.getenv("OPENAI_API_KEY")` which returns `None` because the environment variable isn't set in the Jupyter kernel's environment.

## Solutions

### Option 1: Set API Key Directly in Notebook (QUICKEST)

In your notebook, find this cell:
```python
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

api_key = os.getenv("OPENAI_API_KEY")
```

Replace it with:
```python
import os

# Set your OpenAI API key directly
os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR-ACTUAL-KEY-HERE"

api_key = os.getenv("OPENAI_API_KEY")
```

Or even simpler, just pass the key directly:
```python
api_key = "sk-proj-YOUR-ACTUAL-KEY-HERE"
```

### Option 2: Create a .env File (RECOMMENDED FOR SECURITY)

1. **Create a `.env` file** in your project directory:
   ```
   OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
   ```

2. **Install python-dotenv**:
   ```cmd
   pip install python-dotenv
   ```

3. **Update your notebook cell**:
   ```python
   import os
   from dotenv import load_dotenv
   
   # Load environment variables from .env file
   load_dotenv()
   
   api_key = os.getenv("OPENAI_API_KEY")
   
   llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)
   ```

4. **Add `.env` to your `.gitignore`** to prevent committing your API key:
   ```
   .env
   ```

### Option 3: Set Environment Variable in VS Code

1. Create a `.vscode/settings.json` file:
   ```json
   {
     "jupyter.envFile": "${workspaceFolder}/.env"
   }
   ```

2. Create the `.env` file as described in Option 2

3. Restart VS Code and reload the notebook kernel

### Option 4: Set System Environment Variable (Windows)

⚠️ **Note**: This makes the key available system-wide, which may be a security concern.

**PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
```

**Command Prompt:**
```cmd
set OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
```

**Permanently (System-wide):**
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `OPENAI_API_KEY`
6. Variable value: Your API key
7. Click OK and **restart VS Code**

## Verification

Run this in a notebook cell to verify:
```python
import os

# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print(f"✓ API key is set: {api_key[:20]}...{api_key[-4:]}")
else:
    print("✗ API key is NOT set")
    print("Please set it using one of the methods above")
```

## Security Best Practices

1. **Never commit API keys to version control**
   - Add `.env` to `.gitignore`
   - Use environment variables or secret management

2. **Regenerate keys** if accidentally exposed
   - Go to https://platform.openai.com/api-keys
   - Delete the exposed key
   - Generate a new one

3. **Use different keys** for different projects/environments
   - Development key
   - Production key

4. **Monitor API usage** regularly
   - Check https://platform.openai.com/usage

## Quick Fix for Right Now

**Replace this cell in your notebook:**
```python
api_key = os.getenv("OPENAI_API_KEY")
```

**With this:**
```python
import os

# Temporarily set the API key directly (for testing)

api_key = os.getenv("OPENAI_API_KEY")
```

**⚠️ IMPORTANT**: After testing, move to Option 2 (.env file) for better security!

---

**After setting the key, restart your notebook kernel:**
1. In VS Code, click on "Restart" in the kernel selector
2. Re-run all cells from the beginning

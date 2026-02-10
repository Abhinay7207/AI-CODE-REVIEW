import os
import re
import json
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Code Review & Rewrite Agent")

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("ERROR: GROQ_API_KEY is not set in .env file. Please replace 'your_groq_api_key_here' with your actual API key.")

client = Groq(api_key=api_key)

# Model configuration
MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.7
MAX_TOKENS = 4096

# History Configuration
HISTORY_FILE = "history.json"

# Pydantic models for request body
class ReviewRequest(BaseModel):
    code: str
    language: str
    focus_areas: str = "Bugs, Security, Performance, Best Practices"
    custom_rules: str = ""  # Custom coding standards

class RewriteRequest(BaseModel):
    code: str
    language: str

class HistoryItem(BaseModel):
    id: str
    timestamp: str
    type: str  # "review" or "rewrite"
    language: str
    code: str
    result: str
    focus_areas: Optional[str] = None

# --- Helper Functions ---

def load_history() -> List[dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history_item(item: dict):
    history = load_history()
    # Prepend new item
    history.insert(0, item)
    # Keep only last 15 items
    if len(history) > 15:
        history = history[:15]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def parse_review_response(review_text: str):
    """
    Parses the LLM review response to categorize feedback.
    This is a simplified regex parser as per requirements.
    """
    # Simply returns text for now as frontend handles markdown
    return review_text

# --- Routes ---

# Templates
templates = Jinja2Templates(directory="templates")

# Ensure templates directory exists
if not os.path.exists("templates"):
    os.makedirs("templates")

@app.get("/", response_class=HTMLResponse)
async def serve_tool(request: Request):
    """Serves the main tool page (index.html)."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history", response_model=List[HistoryItem])
async def get_history():
    """Returns the list of past reviews/rewrites."""
    return load_history()

@app.get("/history/{item_id}", response_model=HistoryItem)
async def get_history_item(item_id: str):
    """Returns a specific history item by ID."""
    history = load_history()
    for item in history:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="History item not found")

@app.delete("/history/{item_id}")
async def delete_history_item(item_id: str):
    """Deletes a specific history item."""
    history = load_history()
    new_history = [item for item in history if item["id"] != item_id]
    with open(HISTORY_FILE, "w") as f:
        json.dump(new_history, f, indent=2)
    return {"message": "Item deleted"}

@app.post("/review")
async def review_code(request: ReviewRequest):
    """
    Handles code review requests.
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    # Build custom rules section if provided
    custom_rules_section = ""
    if request.custom_rules and request.custom_rules.strip():
        custom_rules_section = f"""

**CUSTOM CODING STANDARDS TO ENFORCE**:
{request.custom_rules}

Make sure to check the code against these custom rules and highlight any violations.
"""

    prompt = f"""
You are an expert Senior Software Engineer. Provide a code review for this {request.language} code.

**STRICT OUTPUT FORMATTING RULES**:
1. Use bullet points (-) for all explanations.
2. ALL code snippets MUST be in their own triple-backtick blocks.
3. You MUST leave a BLANK LINE before and after every triple-backtick block.
4. NEVER indent code blocks. They must start at the very beginning of the line.
5. Keep explanations brief (1-2 sentences).

Focus: {request.focus_areas}.
{custom_rules_section}

## Critical Issues (Bugs, Security)
- **Issue**: [Description]
- **Fix**: [Description]

**Fixed Code Example**:

```{request.language}
[Fixed code snippet]
```

## High Priority (Performance, Logic)
- **Issue**: [Description]
- **Recommendation**: [Description]

**Improved Code Example**:

```{request.language}
[Improved code snippet]
```

## Medium Priority (Best Practices)
- **Issue**: [Description]
- **Suggestion**: [Description]

## Low Priority (Formatting, Comments)
- [Bullet points only]

## Refactoring Suggestions
- [Bullet points only]

**Original Code for Context**:

```{request.language}
{request.code}
```
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a world-class Senior Software Engineer. You provide code reviews that are strictly formatted in Markdown. You MUST ensure all code examples are strictly wrapped in triple backtick code blocks with the correct language identifier. Never leave raw code outside of blocks."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        response_text = chat_completion.choices[0].message.content
        
        # Save to history
        try:
            history_item = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "type": "review",
                "language": request.language,
                "code": request.code,
                "result": response_text,
                "focus_areas": request.focus_areas
            }
            save_history_item(history_item)
        except Exception as e:
            print(f"Failed to save history: {e}")
            
        return {"review": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rewrite")
async def rewrite_code(request: RewriteRequest):
    """
    Handles code rewrite requests.
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    prompt = f"""
You are an expert Senior Software Engineer.
Rewrite the following {request.language} code to be optimized, clean, secure, and production-ready.

**Requirements**:
1. Apply best practices and design patterns
2. Add clear, concise comments explaining key sections
3. Optimize for performance and readability
4. Fix any security vulnerabilities
5. Use proper naming conventions

**Format your response as**:

## Optimized Code
```{request.language}
[Your rewritten code here]
```

## Key Improvements Made
- **[Category]**: [What was improved]
- **[Category]**: [What was improved]

## Additional Recommendations
- [Any further suggestions as bullet points]

Original Code:
```{request.language}
{request.code}
```

Provide the complete rewritten code with explanations.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a production-focused Senior Software Engineer. Rewrite code to be extremely clean and efficient. Always wrap the final code in triple backticks."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        response_text = chat_completion.choices[0].message.content

        # Save to history
        try:
            history_item = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "type": "rewrite",
                "language": request.language,
                "code": request.code,
                "result": response_text
            }
            save_history_item(history_item)
        except Exception as e:
            print(f"Failed to save history: {e}")

        return {"rewritten_code": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel serverless handler
handler = app

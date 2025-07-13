from fastapi import FastAPI
from pydantic import BaseModel
from ollama_interface import query_ollama

app = FastAPI()

# Global variable to store the last prompt
last_prompt = ""

class PromptRequest(BaseModel):
    prompt: str

@app.post("/complete")
async def complete(request: PromptRequest):
    global last_prompt
    last_prompt = request.prompt

    print("\n" + "="*40)
    print("📥 Prompt received by Derick:")
    print(request.prompt)
    print("="*40)

    response = query_ollama(request.prompt)

    print("📤 Completion sent:")
    print(response)
    print("="*40 + "\n")

    # Log to file for backup
    with open("prompt_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\nPrompt: {request.prompt}\nResponse: {response}\n{'-'*50}")

    return {"completion": response}


@app.get("/last-prompt")
async def show_last_prompt():
    return {"last_prompt": last_prompt}

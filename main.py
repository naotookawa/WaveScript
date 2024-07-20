# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/generate_script")
async def generate_script(prompt: Prompt):
    api_key = os.getenv('OPEN_API_KEY')
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt.prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        script = response_json['choices'][0]['message']['content']
        return {"script": script}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    # プロンプトに基づいてラジオ番組の脚本を生成するロジックを追加
    # script = f"Generated script based on prompt: {prompt.prompt}"
    # return {"script": script}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime
import random
import uvicorn

app = FastAPI(title="ABS AI", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель запроса
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

# Хранилище чатов
chats = {}

# ABS AI ответы с оранжевой тематикой
def abs_ai_response(message: str) -> str:
    message_lower = message.lower()
    
    # Приветствия
    if any(word in message_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
        responses = [
            "🔥 Привет! Я ABS AI с неоново-оранжевым интерфейсом!",
            "✨ Здравствуйте! ABS AI к вашим услугам.",
            "🚀 Приветствую! Готов помочь с любыми вопросами."
        ]
        return random.choice(responses)
    
    # Программирование
    elif 'python' in message_lower or 'код' in message_lower:
        if 'сортиров' in message_lower:
            return """🔥 **Сортировка пузырьком на Python:**

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Пример использования
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(f"Отсортированный массив: {sorted_numbers}")

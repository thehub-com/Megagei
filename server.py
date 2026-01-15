import os
import json
import random
from datetime import datetime
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# ============ ABS AI ЛОГИКА ============
class ABS_AI:
    """AI движок ABS AI"""
    
    def __init__(self):
        self.knowledge_base = {
            "приветствия": [
                "Привет! Я ABS AI, ваш умный помощник.",
                "Здравствуйте! Чем могу помочь?",
                "Приветствую! Готов помочь с любыми вопросами."
            ],
            "возможности": [
                "Я могу: отвечать на вопросы, помогать с кодом, анализировать тексты, объяснять сложные темы.",
                "Мои возможности: программирование, анализ данных, обучение, творческие задачи.",
                "Помогаю с: Python, JavaScript, анализом, обучением, решением задач."
            ],
            "помощь": [
                "Просто напишите ваш вопрос, и я постараюсь помочь!",
                "Задайте вопрос или опишите задачу, и я дам подробный ответ.",
                "Напишите что вас интересует, и я предоставлю полезную информацию."
            ]
        }
        
        self.code_examples = {
            "python": {
                "сортировка": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
                "факториал": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
                "фибоначчи": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
            },
            "javascript": {
                "сортировка": "function bubbleSort(arr) {\n    let n = arr.length;\n    for(let i = 0; i < n; i++) {\n        for(let j = 0; j < n-i-1; j++) {\n            if(arr[j] > arr[j+1]) {\n                [arr[j], arr[j+1]] = [arr[j+1], arr[j]];\n            }\n        }\n    }\n    return arr;\n}",
                "факториал": "function factorial(n) {\n    if (n === 0) return 1;\n    return n * factorial(n-1);\n}"
            }
        }
    
    def process_message(self, message: str, history: List[Dict]) -> str:
        """Обработка сообщения пользователя"""
        message_lower = message.lower()
        
        # Приветствия
        if any(word in message_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
            return random.choice(self.knowledge_base["приветствия"])
        
        # Вопросы о возможностях
        if any(word in message_lower for word in ['умеешь', 'можешь', 'возможности', 'функции']):
            return random.choice(self.knowledge_base["возможности"])
        
        # Помощь
        if any(word in message_lower for word in ['помоги', 'помощь', 'как использовать']):
            return random.choice(self.knowledge_base["помощь"])
        
        # Программирование
        if any(word in message_lower for word in ['python', 'питон', 'код', 'программирование']):
            if 'сортировка' in message_lower:
                return f"Вот пример сортировки пузырьком на Python:\n```python\n{self.code_examples['python']['сортировка']}\n```"
            elif 'факториал' in message_lower:
                return f"Вот пример вычисления факториала:\n```python\n{self.code_examples['python']['факториал']}\n```"
            elif 'фибоначчи' in message_lower:
                return f"Вот пример чисел Фибоначчи:\n```python\n{self.code_examples['python']['фибоначчи']}\n```"
            else:
                return "Я могу помочь с Python кодом. Спросите конкретнее: сортировка, факториал, фибоначчи и т.д."
        
        # JavaScript
        if any(word in message_lower for word in ['javascript', 'js', 'джаваскрипт']):
            if 'сортировка' in message_lower:
                return f"Вот пример сортировки пузырьком на JavaScript:\n```javascript\n{self.code_examples['javascript']['сортировка']}\n```"
            elif 'факториал' in message_lower:
                return f"Вот пример вычисления факториала:\n```javascript\n{self.code_examples['javascript']['факториал']}\n```"
            else:
                return "Я могу помочь с JavaScript кодом. Задайте конкретный вопрос."
        
        # Общие вопросы
        if '?' in message:
            responses = [
                f"Отличный вопрос! По теме '{message}': я могу сказать, что это интересная тема для изучения.",
                f"Вопрос о '{message}' требует внимательного рассмотрения. Вот что я знаю...",
                f"Отвечаю на ваш вопрос: '{message}'. Это важная тема в современном мире.",
                f"По вопросу '{message}': рекомендую изучить основные концепции и практические примеры."
            ]
            return random.choice(responses)
        
        # Анализ текста
        if any(word in message_lower for word in ['анализ', 'проанализируй', 'разбери']):
            word_count = len(message.split())
            return f"📊 Анализ текста:\n- Слов: {word_count}\n- Символов: {len(message)}\n- Примерная тема: {self.detect_topic(message)}\n- Рекомендация: {self.get_recommendation(message)}"
        
        # Обучение
        if any(word in message_lower for word in ['объясни', 'что такое', 'как работает']):
            topic = self.extract_topic(message)
            return f"📚 Объясняю тему '{topic}':\n\nЭто важная концепция, которая включает в себя несколько ключевых аспектов. Основные принципы:\n1. Фундаментальные основы\n2. Практическое применение\n3. Примеры использования\n\nДля глубокого понимания рекомендую изучить дополнительные материалы."
        
        # Стандартный ответ
        responses = [
            f"ABS AI: Я получил ваш запрос: '{message}'. Это интересная тема!",
            f"По вашему вопросу '{message}' могу сказать следующее...",
            f"Отличный запрос! '{message}' - это важная тема для обсуждения.",
            f"ABS AI анализирует: '{message}'. Вот что я могу предложить...",
            f"По теме '{message}': рекомендую рассмотреть несколько подходов...",
            f"Ваш запрос '{message}' заслуживает внимательного изучения.",
            f"ABS AI: Изучаю ваш вопрос о '{message}'...",
            f"Интересный запрос! '{message}' требует детального рассмотрения."
        ]
        
        # Добавляем контекст из истории
        if history:
            last_msgs = history[-3:]  # Последние 3 сообщения
            context = " ".join([msg['content'][:50] for msg in last_msgs])
            responses.append(f"Учитывая предыдущий разговор, по вопросу '{message}' могу добавить...")
        
        return random.choice(responses)
    
    def detect_topic(self, text: str) -> str:
        """Определение темы текста"""
        text_lower = text.lower()
        topics = {
            'технологии': ['технология', 'ии', 'искусственный', 'программирование', 'код', 'алгоритм'],
            'образование': ['обучение', 'учеба', 'школа', 'университет', 'курс'],
            'наука': ['наука', 'исследование', 'эксперимент', 'теория'],
            'бизнес': ['бизнес', 'стартап', 'компания', 'продукт', 'маркетинг']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return 'общая тема'
    
    def extract_topic(self, text: str) -> str:
        """Извлечение темы из вопроса"""
        words = text.lower().split()
        question_words = ['что', 'как', 'почему', 'зачем', 'объясни']
        
        for i, word in enumerate(words):
            if word in question_words and i + 1 < len(words):
                return ' '.join(words[i+1:i+3])
        
        return text[:20] + '...'
    
    def get_recommendation(self, text: str) -> str:
        """Рекомендации по тексту"""
        length = len(text)
        if length < 50:
            return "Добавьте больше деталей для лучшего анализа"
        elif length < 200:
            return "Хороший объем для анализа"
        else:
            return "Большой текст, рекомендую разбить на части"

# ============ FASTAPI APP ============
app = FastAPI(title="ABS AI", version="2.0")
ai_engine = ABS_AI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="."), name="static")

# МОДЕЛИ
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

class FileUpload(BaseModel):
    filename: str
    content: str

# ХРАНИЛИЩЕ
conversations = {}

# API ЭНДПОИНТЫ
@app.get("/")
async def serve_home():
    """Главная страница"""
    return FileResponse("index.html")

@app.get("/api/health")
async def health_check():
    """Проверка работы API"""
    return {
        "status": "active",
        "service": "ABS AI",
        "version": "2.0",
        "ai_engine": "ABS AI Engine"
    }

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Обработка чата"""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(400, "Сообщение не может быть пустым")
        
        # Инициализация диалога
        conv_id = request.conversation_id
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        # Добавляем сообщение пользователя
        user_msg = {
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        }
        conversations[conv_id].append(user_msg)
        
        # Получаем историю
        history = conversations[conv_id][-10:] if len(conversations[conv_id]) > 10 else conversations[conv_id]
        
        # Обрабатываем сообщение AI
        ai_response = ai_engine.process_message(request.message, history)
        
        # Добавляем ответ AI
        ai_msg = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        conversations[conv_id].append(ai_msg)
        
        # Ограничиваем историю
        if len(conversations[conv_id]) > 30:
            conversations[conv_id] = conversations[conv_id][-30:]
        
        return {
            "success": True,
            "response": ai_response,
            "conversation_id": conv_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": f"Ошибка: {str(e)}",
            "error": str(e)
        }

@app.post("/api/upload")
async def upload_file(file: FileUpload):
    """Загрузка файлов"""
    try:
        return {
            "success": True,
            "filename": file.filename,
            "size": len(file.content),
            "message": f"Файл '{file.filename}' успешно загружен"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.get("/api/conversations")
async def list_conversations():
    """Список диалогов"""
    conv_list = []
    
    for conv_id, messages in conversations.items():
        if messages:
            conv_list.append({
                "id": conv_id,
                "title": messages[0]["content"][:30] + "...",
                "message_count": len(messages)
            })
    
    return {
        "success": True,
        "conversations": conv_list,
        "total": len(conv_list)
    }

# ЗАПУСК СЕРВЕРА
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 ABS AI запущен на порту {port}")
    print(f"🌐 Откройте: http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

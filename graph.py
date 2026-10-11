from langgraph.graph import StateGraph, END
from state import MovieState
from llm import llm
from fastmcp import Client
import json
import asyncio

mcp_client = Client("http://localhost:8000/mcp")

def extract_genre(state: MovieState):
    prompt = f"""
این جمله را در نظر بگیر:
{state["user_message"]}
---
از جمله‌ی بالا فقط ژانر فیلم را فقط با یک کلمه انگلیسی استخراج کن
توجه کن که فقط یک ژانر را انتخاب کنی و آن را به صورت انگلیسی برگردانی
بدون هیچ حرف اضافی
ژانرها به این صورت است:
Drama
Action
Crime
Drama
Sci-Fi
Thriller
"""
    state["genre"] = llm.invoke(prompt).content.strip()
    return state

async def fetch_movies_async(state: MovieState):
    async with mcp_client:
        result = await mcp_client.call_tool(
            "search_movies",
            {
                "genre": state["genre"],
                "min_rating": 8.5,
            }
        )
    
    return [
        movie
        for c in result.content
        if c.type == "text"
        for movie in json.loads(c.text)
    ]

def fetch_movies(state: MovieState):
    
    movies = asyncio.run(fetch_movies_async(state))
    state["movies"] = movies
    
    return state

def generate_response(state: MovieState):
    if not state["movies"]:
        state["response"] = "فیلم مناسبی با این ژانر پیدا نشد."
        return state
    
    movies_text = "\n".join(
        [f"{m['title']} ({m['year']}) - IMDb {m['rating']}" for m in state["movies"]]
    )
    
    user_question = state['user_message']
    prompt = f"""
تو یک سیستم پیشنهاد دهنده فیلم هستی
کاربر فارسی زبان است و این سوال را کرده است:
{user_question}
---
متنوع کرده‌ایم و فیلم‌های زیر را بر اساس ژانر مورد نظر کاربر پیدا کرده‌ایم
فقط از فیلم‌های زیر استفاده کن:

{movies_text}

پیشنهادها را شبیه سرویس استریم بنویس.
"""

    state["response"] = llm.invoke(prompt).content
    return state

def build_graph():
    graph = StateGraph(MovieState)
    
    graph.add_node("genre", extract_genre)
    graph.add_node("movies", fetch_movies)
    graph.add_node("response", generate_response)
    
    graph.set_entry_point("genre")
    graph.add_edge("genre", "movies")
    graph.add_edge("movies", "response")
    graph.add_edge("response", END)
    
    return graph.compile()
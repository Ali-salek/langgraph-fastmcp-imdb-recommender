from typing import TypedDict, List, Dict

class MovieState(TypedDict):
    user_message: str
    genre: str
    movies: List[Dict]
    response: str
from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {
    1: {"title": "My first post her", "content": "This is my first post here, am so excited"},
    2: {"title": "My second post her", "content": "This is my second post here"},
    3: {"title": "Hello everyone", "content": "Fuck, am so happy :)"},
    4: {"title": "Learning FastAPI", "content": "Just started building APIs with FastAPI and it's blazing fast"},
    5: {"title": "Weekend vibes", "content": "Nothing beats a lazy Sunday with coffee and code"},
    6: {"title": "Food review", "content": "Tried that new ramen spot downtown, absolutely delicious"},
    7: {"title": "Gym progress", "content": "Hit a new personal record on deadlift today, feeling strong"},
    8: {"title": "Movie night", "content": "Finally watched Dune Part Two, the visuals were insane"},
    9: {"title": "Travel plans", "content": "Booking flights to Japan next month, can't wait for the cherry blossoms"},
    10: {"title": "Project update", "content": "Deployed the new feature to production, smooth sailing so far"},
}


@app.get("/posts")
def get_all_post(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int) -> dict:
    if id not in text_posts:
        raise HTTPException(404, "Post not found")

    return text_posts[id]

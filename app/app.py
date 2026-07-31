from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from app.schemas import PostCreate, PostResponse
from app.database import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_post(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    post = Post(caption=caption, url="dummy_url", file_type="photo", file_name=file.filename)

    # Prepare the post object to be added to the database
    session.add(post)
    # Write the post to the database
    await session.commit()
    # Refresh the post object to get the auto-generated fields (like id) from the database
    await session.refresh(post)

    return post


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )

    return {"posts": post_data}

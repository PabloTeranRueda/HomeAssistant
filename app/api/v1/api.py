from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("TERA_HOST", "127.0.0.1")
port = os.getenv("TERA_ANGULAR_PORT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{host}:{port}",f"http://localhost:{port}"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/v1/shopping-list")
def get_shopping_list() -> list[str]:
    try:
        with open(file=r"resources\shopping_list.csv", mode="r", encoding="utf-8") as file:
            contents = file.read().splitlines()

        return contents

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Shopping list not found") from error

@app.delete("/api/v1/shopping-list")
def delete_item(item: str):

    return {"message": f"Deleted {item}"}



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
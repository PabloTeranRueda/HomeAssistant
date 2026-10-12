from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

@app.get("/api/v1/shopping-list")
def get_shopping_list() -> list[str]:
    try:
        with open(file=r"resources\shopping_list.csv", mode="r", encoding="utf-8") as file:
            contents = file.read().splitlines()

        return contents

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Shopping list not found") from error
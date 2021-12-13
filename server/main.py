from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from server.actions.api import (action_router,
                                actiontype_router, reaction_router)

app = FastAPI()

origins = [
    "http://localhost",
    "http://192.168.1.181",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.1.181:8081",
    "http://192.168.1.181:8080",
    "http://192.168.1.181:8000",
    "*"
]

origins_all = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_all,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
-----------------------------------------
API Landing Page
-----------------------------------------
"""
api_landing = """
<!DOCTYPE html>
<html>
    <head>
        <title>Raspberry Display Remote Conrtoller</title>
    </head>
    <body>
    <h1> Landing Page for Controller API </h1>
    </body>
</html>
"""

app.include_router(action_router)
app.include_router(actiontype_router)
app.include_router(reaction_router)


@app.get("/")
async def get():
    return HTMLResponse(api_landing)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=True)

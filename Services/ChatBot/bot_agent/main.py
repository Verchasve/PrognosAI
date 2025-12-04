from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

from model_client import get_prediction
#from github_utils import analyze_branch

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatInput(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/chat")
# def chat_handler(user_input: ChatInput):
#     prediction = get_prediction(user_input.message)

#     # Expecting model to return a ticket like: {"type": "jira", "ticket": "JIRA-101"}
#     if prediction.get("type") == "jira":
#         branch = f"feature/{prediction['ticket']}"
#         analysis = analyze_branch(branch)
#         return {"prediction": prediction, "analysis": analysis}

#     return {"prediction": prediction}

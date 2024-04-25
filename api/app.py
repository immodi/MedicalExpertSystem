from sys import path
path.append("../")

import pathlib
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from experta import Fact
from main import MedicalExpert

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
current_path = pathlib.Path(__file__).parent.resolve()

@app.get("/", response_class=HTMLResponse)
async def get_username(request: Request):
    return templates.TemplateResponse(
        request=request, name="username.html", context={}
    )

@app.post("/test/", response_class=HTMLResponse)
async def start_test(request: Request, username: Annotated[str, Form()]):
    input_questions = [
        "Do you have chest pain?",
        "Do you have cough?",
        "Do you faint occasionally?",
        "Do you experience fatigue occasionally?",
        "Do you experience headaches?",
        "Do you experience back pains?",
        "Do you experience sunken eyes?",
        "Do you experience fever?",
        "Do you experience sore throat?",
        "Do you experience restlessness?"
    ]
    return templates.TemplateResponse(
        request=request, name="test.html", context={"username": username, "questions": input_questions}
    )

@app.get("/test/", response_class=HTMLResponse)
async def start_test(request: Request):
    return templates.TemplateResponse(request=request)


@app.post("/result/", response_class=HTMLResponse)
async def display_results(request: Request, username: Annotated[str, Form()], answers: List[str] = Form(...)):
    facts = [username, *answers]
    engine = MedicalExpert()
    engine.reset()
    engine.change_facts(facts)
    engine.run()

    disease = engine.get_disease_name()
    if disease is None:
        return templates.TemplateResponse(
            request=request, name="negative.html", context={"disease": "No diseases found. You are healthy!"}
        )
    else:
        with open("../disease/disease_descriptions/" + disease + ".txt", "r") as des_file:
            description = des_file.read()

        with open("../disease/disease_treatments/" + disease + ".txt", "r") as mes_file:
            measures = mes_file.read()

        return templates.TemplateResponse(
            request=request, name="positive.html", context={
                "disease": f"The most probable illness you are suffering from is: {disease}",
                "description": description,
                "measures": measures,
                "username": username
            }
        )

@app.get("/result/", response_class=HTMLResponse)
async def display_results(request: Request):
    return templates.TemplateResponse(request=request)
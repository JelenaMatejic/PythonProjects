from fastapi import Request, FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import calculation

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html") as f:
        return f.read()

@app.post("/max-plus")
async def maxPlus(
    file1: UploadFile = File(),
    file2: UploadFile = File(),
    forwardSimulation: bool = Form(...),
    backwardSimulation: bool = Form(...),
    forwardBisimulation: bool = Form(...),
    backwardBisimulation: bool = Form(...),
    forwardBackwardBisimulation: bool = Form(...),
    backwardForwardBisimulation: bool = Form(...)
):

    f1_content = file1.file.read()
    with open(file1.filename, "wb") as f:
        f.write(f1_content)

    f2_content = file2.file.read()
    with open(file2.filename, "wb") as f:
        f.write(f2_content)

    selected_options = []
    if forwardSimulation:
        selected_options.append("forwardSimulation")
    if backwardSimulation:
        selected_options.append("backwardSimulation")
    if forwardBisimulation:
        selected_options.append("forwardBisimulation")
    if backwardBisimulation:
        selected_options.append("backwardBisimulation")
    if forwardBackwardBisimulation:
        selected_options.append("forwardBackwardBisimulation")
    if backwardForwardBisimulation:
        selected_options.append("backwardForwardBisimulation")
    
    res = calculation.compute(file1.filename, file2.filename, selected_options)

    # Return the response as a JSON object
    return JSONResponse(content=res)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import Request, FastAPI, File, UploadFile, Form, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import calculation
import shutil
import os
from pathlib import Path
import tempfile

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine the path to the "results" directory
results_path = Path(__file__).parent / "results"

# Mount the "results" directory to serve the generated files
app.mount("/results", StaticFiles(directory=results_path), name="results")


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
    with open("results/automatonA.txt", "wb") as f:
        f.write(f1_content)

    f2_content = file2.file.read()
    with open("results/automatonB.txt", "wb") as f:
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
    
    res = calculation.compute("results/automatonA.txt", "results/automatonB.txt", selected_options)

    # Return the response as a JSON object
    return JSONResponse(content=res)

@app.get("/download_zip")
async def download_zip():
    # Create a temporary directory to hold the zip file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary zip file
        temp_zip_file = os.path.join(temp_dir, "temp_results.zip")
        shutil.make_archive(os.path.splitext(temp_zip_file)[0], "zip", "results")

        # Open the temporary zip file in binary read mode
        with open(temp_zip_file, "rb") as file:
            # Read the binary content of the zip file
            zip_content = file.read()

        # Create a response with the zip content
        response = Response(content=zip_content, media_type="application/zip")

        # Set the response headers to trigger the download
        response.headers["Content-Disposition"] = 'attachment; filename="results.zip"'

        return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

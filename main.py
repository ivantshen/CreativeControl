from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import papermill as pm

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class UserInput(BaseModel):
    message: str

@app.post("/process-message/")
async def process_message(input: UserInput):
    output_notebook = "output.ipynb"
    try:
        # Execute the notebook with user input
        pm.execute_notebook(
            "MAIN.ipynb",  # Path to your notebook
            output_notebook,
            parameters={"user_message": input.message}  # Pass user input
        )
        
        # Simulate parsing the notebook's output
        with open("output_full_actual.txt", "r") as f:
            response = f.read()
        return {"response": f"Processed message: {response}"}
    except Exception as e:
        print(f"Error during notebook execution: {e}")
        return {"error": str(e)}

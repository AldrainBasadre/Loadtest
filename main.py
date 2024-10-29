from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class CalculationRequest(BaseModel):
    number1: float
    number2: float


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Calculator</title>
        </head>
        <body>
            <h1>Simple Calculator</h1>
            <form action="/calculate" method="post">
                <label for="number1">Number 1:</label>
                <input type="number" step="any" name="number1" required>
                <br><br>
                <label for="number2">Number 2:</label>
                <input type="number" step="any" name="number2" required>
                <br><br>
                <button name="operation" value="add">Add</button>
                <button name="operation" value="subtract">Subtract</button>
                <button name="operation" value="multiply">Multiply</button>
                <button name="operation" value="divide">Divide</button>
            </form>
        </body>
    </html>
    """


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    number1: float = Form(...), number2: float = Form(...), operation: str = Form(...)
):
    try:
        if operation == "add":
            result = number1 + number2
        elif operation == "subtract":
            result = number1 - number2
        elif operation == "multiply":
            result = number1 * number2
        elif operation == "divide":
            if number2 == 0:
                raise HTTPException(
                    status_code=400, detail="Division by zero is not allowed."
                )
            result = number1 / number2
        else:
            raise HTTPException(status_code=400, detail="Invalid operation.")
    except HTTPException as e:
        return f"<html><body><h1>Error: {e.detail}</h1></body></html>"

    return f"""
    <html>
        <body>
            <h1>Result: {result}</h1>
            <a href="/">Back to Calculator</a>
        </body>
    </html>
    """

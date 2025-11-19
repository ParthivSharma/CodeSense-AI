# CodeSense-AI

CodeSense-AI is an intelligent code analysis backend built using **FastAPI**. It performs static code analysis on Python code using the AST (Abstract Syntax Tree) module and provides insights, suggestions, and metrics.

## 🚀 Features (Current Progress)

* FastAPI backend fully set up
* Working `/analyze` endpoint
* Python AST-based analyzer
* Detects:

  * Total functions
  * Imports used in code
  * Missing docstrings
* Modular project structure using routers and service layers

## 📁 Project Structure

```
backend/
 ├── app.py
 ├── routers/
 │    └── analyze.py
 └── services/
      └── code_analyzer.py
```

## 🛠 Tech Stack

* **Python 3.12**
* **FastAPI**
* **Uvicorn**
* **Pydantic**

## 📦 Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## ▶️ Run the Server

```bash
uvicorn backend.app:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

## 📡 API Endpoint

### POST `/analyze`

Analyzes Python code and returns:

* Number of functions
* Imports
* Suggestions based on rules

#### Example Request

```json
{
  "code": "import math\n\ndef hello():\n    print('Hello')\n\ndef world():\n    pass"
}
```

#### Example Response

```json
{
  "status": "success",
  "analysis": {
    "total_functions": 2,
    "imports": ["math"],
    "suggestions": [
      "Function 'hello' has no docstring.",
      "Function 'world' has no docstring."
    ]
  }
}
```

## 📌 Next Steps (Planned)

* Add advanced static analysis rules
* Cyclomatic complexity
* Nested loop detection
* Long function warnings
* Unused variable detection
* Multi-language support (JS, C++, Java)
* React frontend with Monaco editor
* AI-powered code suggestions

## © Author

Parthiv Sharma

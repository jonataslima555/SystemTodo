from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import datetime

app = FastAPI(title="Todo List App")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Banco de dados em memória
todos = []
counter = 1


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, filter: Optional[str] = "all"):
    if filter == "active":
        filtered = [t for t in todos if not t["done"]]
    elif filter == "done":
        filtered = [t for t in todos if t["done"]]
    else:
        filtered = todos

    total = len(todos)
    done_count = len([t for t in todos if t["done"]])
    pending_count = total - done_count

    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": filtered,
        "filter": filter,
        "total": total,
        "done_count": done_count,
        "pending_count": pending_count,
    })


@app.post("/add")
async def add_todo(title: str = Form(...), priority: str = Form("normal")):
    global counter
    todos.append({
        "id": counter,
        "title": title,
        "done": False,
        "priority": priority,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })
    counter += 1
    return RedirectResponse("/", status_code=303)


@app.post("/toggle/{todo_id}")
async def toggle_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            break
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return RedirectResponse("/", status_code=303)


@app.post("/clear-done")
async def clear_done():
    global todos
    todos = [t for t in todos if not t["done"]]
    return RedirectResponse("/", status_code=303)
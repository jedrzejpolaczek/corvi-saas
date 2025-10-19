from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

app = FastAPI(title="Corvi Dashboard")
tpl = Environment(loader=FileSystemLoader("templates"))

@app.get("/exports/experiments/{id}.pdf")
def pdf(id: int):
    html = tpl.get_template("export_pdf.html").render(id=id)
    return HTMLResponse(html)

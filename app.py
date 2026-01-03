import os
from dotenv import load_dotenv

load_dotenv()

# HARD FAIL if Ollama missing
if not os.getenv("OLLAMA_BASE_URL"):
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

print("🔎 OLLAMA_BASE_URL =", os.getenv("OLLAMA_BASE_URL"))

import gradio as gr
import tempfile

from graph.workflow import build_graph
from graph.state import JobHuntState
from utils.io_helpers import extract_cv_text, fetch_job_text
from utils.pdf_export import save_cover_letter_pdf

app = build_graph()

def run(cv_pdf, job_url, task, feedback, satisfied):
    if cv_pdf is None:
        return "❌ Upload CV", None
    if not job_url.strip():
        return "❌ Job URL missing", None

    # ✅ SINGLE SOURCE OF TRUTH
    model_name = "ollama:llama3.1"
    print("🔥 USING MODEL:", model_name)

    cv_text = extract_cv_text(cv_pdf.name)
    job_description = fetch_job_text(job_url)

    state = JobHuntState(
        cv_text=cv_text,
        job_title="Auto",
        job_description=job_description,
        task=task,
        model_name=model_name,
        feedback=feedback,
        satisfied=satisfied,
    )

    result = app.invoke(state)

    if task == "cover":
        return result.cover_letter, None
    if task == "networking":
        return result.networking["text"], None
    if task == "review":
        return result.review["text"], None

    return "Unknown task", None

gr.Interface(
    fn=run,
    inputs=[
        gr.File(label="CV (PDF)"),
        gr.Textbox(label="Job URL"),
        gr.Radio(["cover", "networking", "review"], value="cover"),
        gr.Textbox(label="Feedback"),
        gr.Checkbox(label="Satisfied"),
    ],
    outputs=[gr.Textbox(lines=25), gr.File()],
).launch()

from concurrent.futures import ThreadPoolExecutor
import uuid
from typing import Dict

from app.ai_agent import generate_notes_from_topic
from app.pdf_generator import generate_pdf_from_markdown

_pool = ThreadPoolExecutor(max_workers=4)
_tasks: Dict[str, "Future"] = {}

def start_generate_notes_task(topic: str) -> str:
    def _work():
        markdown = generate_notes_from_topic(topic)
        pdf_path = generate_pdf_from_markdown(markdown)
        return {"status": "done", "pdf_path": pdf_path}

    task_id = str(uuid.uuid4())
    _tasks[task_id] = _pool.submit(_work)
    return task_id

def get_task_result(task_id: str):
    fut = _tasks.get(task_id)
    if fut is None:
        return "UNKNOWN", {"error": "task_id not found"}
    if fut.done():
        try:
            return "SUCCESS", fut.result()
        except Exception as exc:
            return "FAILURE", {"error": str(exc)}
    return "PENDING", {}

from app.ai_agent import generate_notes_from_topic
from app.pdf_generator import generate_pdf_from_markdown
from celery import Celery
import os

celery = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

@celery.task(bind=True)
def generate_notes_task(self, topic):
    try:
        markdown = generate_notes_from_topic(topic)
        pdf_path = generate_pdf_from_markdown(markdown)
        return {"status": "done", "pdf_path": pdf_path}
    except Exception as e:
        self.retry(exc=e, countdown=10)

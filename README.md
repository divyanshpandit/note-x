# Note‑X

Note‑X is a Flask-based web application that generates concise PDF study notes from any user-supplied topic using an AI model. It includes a responsive UI, background note generation with a minimal in-process task queue , and instant PDF download.

---

## Features

- Clean, single-page UI with textarea input
- AI-based note generation from any topic
- PDF export with download link
- Live status updates using JavaScript polling
- No external queue/broker dependencies
- Simple deployment (just run it)

---

## Technologies Used

- Python 3.10+
- Flask
- OpenAI or custom LLM backend (via `app/ai_agent.py`)
- Pure CSS animations (no JS frameworks)
- `concurrent.futures` for background task execution

---

## Folder Structure

note-x/
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── ai_agent.py
│ └── pdf_generator.py
├── static/
│ ├── style.css
│ └── chat.js
├── templates/
│ ├── base.html
│ ├── index.html
│ └── status.html
├── tasks.py
├── run.py
├── requirements.txt
└── README.md

---

## Installation

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/note-x.git
cd note-x
python -m venv venv
source venv/bin/activate     # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py


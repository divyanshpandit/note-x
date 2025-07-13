# app/ai_agent.py
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# --------------------------------------------------------------- #
# Load environment variables (.env must contain OPENROUTER_API_KEY)
# --------------------------------------------------------------- #
load_dotenv()
OR_KEY = os.getenv("OPENROUTER_API_KEY")  # e.g. or_12345...
if not OR_KEY:
    raise RuntimeError("OPENROUTER_API_KEY missing in .env")

# --------------------------------------------------------------- #
# Helper: call Qwen‑32B‑free via OpenRouter
# --------------------------------------------------------------- #
def openrouter_qwen_chat(prompt: str) -> str:
    """
    Send a prompt to the Qwen 32‑B (free) model on OpenRouter
    and return the assistant's reply.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OR_KEY,
    )

    try:
        resp = client.chat.completions.create(
            model="qwen/qwq-32b:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": os.getenv("REFERER_URL", "http://localhost"),
  # update if deployed
                "X-Title": "Note-X",                 # ASCII only
            },
        )
        return resp.choices[0].message.content

    except OpenAIError as e:
        raise RuntimeError(f"[OpenRouter] {e}")

# --------------------------------------------------------------- #
# Public function consumed by tasks.py
# --------------------------------------------------------------- #
def generate_notes_from_topic(topic: str) -> str:
    """
    Generate detailed study notes on the given topic.
    Returns Markdown content ready for PDF conversion.
    """
    prompt = (
        f"Generate a well‑structured set of study notes on the topic **{topic}**.\n"
        "Include:\n"
        "1. A concise introduction\n"
        "2. Key concepts (bulleted)\n"
        "3. Practical examples or applications\n"
        "4. A short summary\n"
        "5. Math formulas related to topic if they exist\n"
        "6. All important points that must be important to remember line wise\n"
    )

    try:
        return openrouter_qwen_chat(prompt)
    except Exception as err:
        print("[ai_agent] OpenRouter Qwen failed:", err)
        return "❌ Failed to generate notes via OpenRouter Qwen."

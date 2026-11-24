# AI Job Interview Simulator (website version)

A simple web app that interviews you for an entry-level business position involving AI:

1. It asks a **basic question** and waits for your answer.
2. It asks a **harder, applied question** and waits for your answer.
3. It gives **feedback**: a verdict per question, strengths, knowledge gaps, incorrect answers and what to review.

You can download the full transcript at the end.

## How it works

- **Frontend and hosting:** [Streamlit](https://streamlit.io), deployed on Streamlit Community Cloud.
- **LLM:** Google Gemini (`gemini-3.5-flash-lite`, with `gemini-3.8-flash` as fallback) through the Gemini API (`google-genai`). The API key is stored as a Streamlit secret and never sent to the browser.
- **Grounding:** `topics.md` is the course topic map (28 topics with must-know points, taken from the course videos and the Anthropic Academy course). For each interview the app picks two topics from different sections. The question prompts and the grading prompt contain only those topics' must-know points, so questions and feedback stick to the course material.
- **Reliability:** Gemini's free tier is sometimes overloaded (HTTP 503). The app retries several times, falls back to a second model, and otherwise shows a "Try again" button without losing your answer.

## Run locally

```bash
pip install -r requirements.txt
mkdir -p .streamlit && echo 'GEMINI_API_KEY = "your-key"' > .streamlit/secrets.toml
streamlit run app.py
```

The project version (local interview simulator with `AGENTS.md` and `SKILL.md`) is in a separate repository.

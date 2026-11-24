"""AI Job Interview Simulator (website version).

Flow: start -> question 1 -> wait for answer -> question 2 -> wait for answer -> feedback.
Questions and the answer key come from topics.md (the course topic map with must-know points).
The LLM is Google Gemini, called through its API; the key is read from Streamlit secrets.
"""
import os
import random
import re
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODELS = ["gemini-3.8-flash"]
TOPICS_FILE = Path(__file__).parent / "topics.md"

# Readable names for the source files listed in topics.md
SOURCE_TITLES = {
    "00-foundations-karpathy": "Karpathy – Deep Dive into LLMs like ChatGPT",
    "01-how-llms-work": "IBM – How Large Language Models Work",
    "02-ai-machine-learning-and-generative-ai": "IBM – AI, Machine Learning, Deep Learning and Generative AI Explained",
    "03-transformers": "IBM – What are Transformers?",
    "04-context-windows": "IBM – What is a Context Window?",
    "05-hallucinations": "IBM – Why Large Language Models Hallucinate",
    "06-probabilistic-versus-deterministic-outcomes": "IBM – AI Agents vs Business Rules",
    "07-embeddings": "IBM – What are Word Embeddings?",
    "08-vector-databases": "IBM – What is a Vector Database?",
    "09-retrieval-augmented-generation-rag": "IBM – What is Retrieval-Augmented Generation?",
    "10-prompt-versus-context-engineering": "IBM – Context Engineering vs. Prompt Engineering",
    "11-tool-calling": "IBM – What is Tool Calling?",
    "12-mcp-and-apis": "IBM – MCP vs API",
    "13-ai-agents": "IBM – What are AI Agents?",
    "14-business-workflows": "IBM – Building AI Agents for Real-World Problems & Workflows",
    "15-agent-skills": "IBM – What AI Agent Skills Are and How They Work",
    "16-memory": "IBM – The Four Types of Memory Every AI Agent Needs",
    "17-reasoning-models": "IBM – What Are Large Reasoning Models?",
    "18-complete-ai-systems": "IBM – What Is an AI Stack?",
    "19-prompt-injection": "IBM – What Is a Prompt Injection Attack?",
    "20-benchmarks": "IBM – What are Large Language Model Benchmarks?",
    "21-evaluating-ai-outputs": "IBM – LLM as a Judge",
    "22-explainability": "IBM – What is Explainable AI?",
    "23-synthetic-data": "IBM – What is Synthetic Data?",
    "24-selecting-business-applications": "IBM – Select the right AI use case for your business",
    "01-intro": "Anthropic Academy – Intro to AI Capabilities and Limitations",
    "02-what-we-mean-by-ai": "Anthropic Academy – What We Mean by AI",
    "03-how-ai-gets-its-character": "Anthropic Academy – How AI Gets Its Character",
    "04-next-token-prediction": "Anthropic Academy – Next Token Prediction",
    "05-next-token-prediction-try-it-out": "Anthropic Academy – Next Token Prediction: Try it out",
    "06-knowledge": "Anthropic Academy – Knowledge",
    "07-knowledge-try-it-out": "Anthropic Academy – Knowledge: Try it out",
    "08-working-memory": "Anthropic Academy – Working Memory",
    "10-steerability": "Anthropic Academy – Steerability",
    "11-steerability-try-it-out": "Anthropic Academy – Steerability: Try it out",
    "12-when-properties-collide": "Anthropic Academy – When Properties Collide",
    "13-next-steps": "Anthropic Academy – Next Steps",
}

INTERVIEWER = """You are a professional interviewer for an entry-level business position that involves AI
(e.g. junior business analyst). The candidate is a business student. Write ONE interview question only:
no greeting, no preamble, no hints, no answer, no numbering. Keep it answerable in 30-60 seconds of speaking.
Base the question strictly on the topic notes you are given."""

GRADER = """You are a strict but fair interview examiner. Grade the candidate's answers ONLY against the
must-know points given for each topic (they come from the course materials). Do not reward vague, generic
or padded answers. A partly right answer is "Partly correct". Do not invent facts beyond the notes."""


# ---------- topics ----------------------------------------------------------------------
@st.cache_data
def load_topics():
    """Parse topics.md into {code: {"name", "section", "sources", "points"}}."""
    text = TOPICS_FILE.read_text(encoding="utf-8")
    topics = {}
    for block in re.split(r"\n(?=### [A-E]\d+\. )", text):
        m = re.match(r"### ([A-E]\d+)\. (.+)", block)
        if not m:
            continue
        code, name = m.group(1), m.group(2).strip()
        block = block.split("\n---")[0]
        src = re.search(r"- Source: (.+)", block)
        files = re.findall(r"(?:transcripts|coursera)/([\w-]+)\.md", src.group(1) if src else "")
        sources = []
        for f in files:
            title = SOURCE_TITLES.get(f)
            if title and title not in sources:
                sources.append(title)
        if src and "Karpathy" in src.group(1) and SOURCE_TITLES["00-foundations-karpathy"] not in sources:
            sources.append(SOURCE_TITLES["00-foundations-karpathy"])
        points = block.split("- Must-know:", 1)[1] if "- Must-know:" in block else block
        points = points.split("- Levels:")[0].strip()
        topics[code] = {"name": name, "section": code[0], "sources": sources, "points": points}
    return topics


def pick_two(topics):
    """Q1 = a basic (L1) question, Q2 = a harder applied (L3) question on a topic from another section."""
    codes = list(topics)
    first = random.choice(codes)
    second = random.choice([c for c in codes if topics[c]["section"] != topics[first]["section"]])
    return first, second


# ---------- Gemini ----------------------------------------------------------------------
def api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:  # noqa: BLE001 - no secrets file locally
        return os.getenv("GEMINI_API_KEY")


@st.cache_resource
def client():
    # Short timeout + few retries, so an overloaded API gives a clear error instead of hanging.
    return genai.Client(
        api_key=api_key(),
        http_options=types.HttpOptions(timeout=60_000, retry_options=types.HttpRetryOptions(attempts=1)),
    )


def ask_gemini(system, prompt, temperature, rounds=6):
    """Gemini's free tier often answers '503 high demand' for a few seconds at a time, so retry
    a few rounds (main model, then fallback) with short pauses before giving up."""
    last_error = None
    for attempt in range(rounds):
        for model in [MODEL] + FALLBACK_MODELS:
            try:
                r = client().models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=system, temperature=temperature),
                )
                if r.text:
                    ss.models_used.add(model)
                    return r.text.strip()
            except Exception as e:  # noqa: BLE001 - try again / try the next model
                last_error = e
                if "429" in str(e) and "PerDay" in str(e):
                    continue  # daily quota of this model used up: go straight to the next one
        time.sleep(2 + 2 * attempt)
    raise last_error or RuntimeError("The model returned an empty answer.")


def make_question(topic, level):
    levels = {
        "L1": "Level: BASIC. Ask the candidate to define or explain the core idea in their own words.",
        "L3": "Level: ADVANCED. Put the candidate in a short, concrete business situation (finance, accounting, "
              "operations, HR or customer service) and ask them to apply the concept: decide, design or "
              "explain a trade-off or risk.",
    }
    prompt = f"Topic: {topic['name']}\n\nTopic notes:\n{topic['points']}\n\n{levels[level]}"
    return ask_gemini(INTERVIEWER, prompt, temperature=0.9)


def make_feedback(qas):
    parts = []
    for i, qa in enumerate(qas, 1):
        t = qa["topic"]
        parts.append(
            f"QUESTION {i} (topic: {t['name']}, level {qa['level']})\n{qa['question']}\n\n"
            f"MUST-KNOW POINTS:\n{t['points']}\n\nSOURCES TO REVIEW: {'; '.join(t['sources'])}\n\n"
            f"CANDIDATE'S ANSWER:\n{qa['answer']}"
        )
    prompt = "\n\n==========\n\n".join(parts) + """

Write the feedback in Markdown with exactly these sections:

**Overall:** one or two honest sentences.

| # | Topic | Verdict |
(one row per question; verdict = ✅ Correct, 🟡 Partly correct or ❌ Incorrect)

### Strengths
### Knowledge gaps
(must-know points the candidate missed or was vague about)
### Incorrect answers
(quote what was wrong and give the correct version from the notes; write "None." if nothing was wrong)
### What to review
(name the specific videos/lessons from SOURCES TO REVIEW and what to focus on in each)

Address the candidate as "you". Be specific and concise."""
    return ask_gemini(GRADER, prompt, temperature=0.2)


# ---------- page ------------------------------------------------------------------------
st.set_page_config(page_title="AI Interview Simulator", page_icon="🎤", layout="centered")
st.title("🎤 AI Job Interview Simulator")
st.caption("Entry-level business role involving AI · two questions, then feedback · questions drawn from the course "
           "materials (Karpathy, IBM Technology, Anthropic Academy)")

if not api_key():
    st.error("No Gemini API key found. Add GEMINI_API_KEY to the app's secrets.")
    st.stop()

ss = st.session_state
ss.setdefault("stage", "start")  # start -> q1 -> q2 -> done
ss.setdefault("qas", [])
ss.setdefault("feedback", "")
ss.setdefault("models_used", set())


def reset():
    ss.stage, ss.qas, ss.feedback, ss.models_used, ss.pending = "start", [], "", set(), None


def new_question(code, level):
    topic = load_topics()[code]
    ss.qas.append({"topic": topic, "level": level, "question": make_question(topic, level), "answer": ""})


def explain(error):
    msg = str(error)
    print(f"[api error] {type(error).__name__}: {msg[:500]}", flush=True)  # visible in the app logs
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        return "The free Gemini quota is used up for now. Wait a minute, then press **Try again**."
    if any(s in msg for s in ("503", "504", "UNAVAILABLE", "DEADLINE", "timed out", "Timeout")):
        return "Google's AI service is overloaded right now. Wait a moment, then press **Try again**."
    return f"The AI service returned an error: {msg[:300]}"


# Each API step is stored as "pending" first, so the page can show the candidate's answer
# right away and offer a retry (without losing the answer) if the API call fails.
STEPS = {
    "q1": ("Preparing your first question…", lambda: new_question(*ss.plan[0]), "q1"),
    "q2": ("Next question…", lambda: new_question(*ss.plan[1]), "q2"),
    "feedback": ("Evaluating your answers…", lambda: setattr(ss, "feedback", make_feedback(ss.qas)), "done"),
}
ss.setdefault("pending", None)

if ss.stage == "start" and not ss.pending:
    st.markdown(
        "You are applying for an **entry-level business position that involves AI**. "
        "The interviewer will ask **two questions**, one at a time: first a basic one, then a harder applied one. "
        "Answer each in your own words (3–6 sentences). After your second answer you get feedback on your "
        "strengths, knowledge gaps and incorrect answers, plus what to review."
    )
    if st.button("Start interview", type="primary"):
        q1, q2 = pick_two(load_topics())
        ss.plan = [(q1, "L1"), (q2, "L3")]
        ss.pending = "q1"
        st.rerun()

# conversation so far
for i, qa in enumerate(ss.qas, 1):
    with st.chat_message("assistant", avatar="🧑‍💼"):
        st.markdown(f"**Question {i} of 2**\n\n{qa['question']}")
    if qa["answer"]:
        with st.chat_message("user"):
            st.markdown(qa["answer"])

if ss.pending:
    label, action, next_stage = STEPS[ss.pending]
    try:
        with st.spinner(label):
            action()
        ss.stage, ss.pending = next_stage, None
        st.rerun()
    except Exception as e:  # noqa: BLE001 - show API problems and offer a retry
        st.error(explain(e))
        st.button("Try again", type="primary")  # any click reruns the page, which retries the step
        st.stop()

if ss.stage in ("q1", "q2"):
    answer = st.chat_input("Type your answer and press Enter")
    if answer and answer.strip():
        ss.qas[-1]["answer"] = answer.strip()
        ss.pending = "q2" if ss.stage == "q1" else "feedback"
        st.rerun()

if ss.stage == "done":
    with st.chat_message("assistant", avatar="🧑‍💼"):
        st.markdown("That's the end of the interview. Here is your feedback.\n\n" + ss.feedback)

    models = ", ".join(sorted(ss.models_used)) or MODEL
    lines = [f"# AI interview transcript – {datetime.now():%Y-%m-%d %H:%M}", "",
             f"Website version · model: {models} (Google Gemini API)", ""]
    for i, qa in enumerate(ss.qas, 1):
        lines += [f"**Interviewer (Question {i}, {qa['topic']['name']}):** {qa['question']}", "",
                  f"**Candidate:** {qa['answer']}", ""]
    lines += ["**Interviewer:** That's the end of the interview. Here is your feedback.", "", ss.feedback]
    c1, c2 = st.columns(2)
    c1.download_button("Download transcript", "\n".join(lines), file_name="interview-transcript.md",
                       mime="text/markdown")
    c2.button("New interview", on_click=reset)

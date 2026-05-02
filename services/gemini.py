"""
services/gemini.py
Google Gemini API integration for JEE doubt solving.
Handles: rate limits, timeouts, API errors, clean prompt formatting.
"""
import asyncio
import logging

import config

logger = logging.getLogger(__name__)

# Try importing google-generativeai; graceful fallback if not installed
try:
    import google.generativeai as genai
    _GEMINI_AVAILABLE = bool(config.GEMINI_API_KEY)
    if _GEMINI_AVAILABLE:
        genai.configure(api_key=config.GEMINI_API_KEY)
        _model = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info("[gemini] Gemini API configured successfully.")
    else:
        logger.warning("[gemini] GEMINI_API_KEY not set. Doubt solver will use fallback.")
        _model = None
except ImportError:
    logger.warning("[gemini] google-generativeai not installed. Doubt solver disabled.")
    _GEMINI_AVAILABLE = False
    _model = None


_SYSTEM_PROMPT = """You are an expert JEE (Joint Entrance Examination) tutor for Indian students.

Rules:
- Answer ONLY Physics, Chemistry, and Mathematics questions relevant to JEE Main/Advanced syllabus.
- If the question is not related to JEE subjects, politely decline and redirect.
- Keep answers concise but complete (max 400 words).
- Use step-by-step explanations where needed.
- Use plain text only — no markdown, no asterisks, no hashtags.
- End every answer with 1 key exam tip related to the topic.
- Be encouraging and motivating.

Student's question:
"""

_FALLBACK_MESSAGES = [
    (
        "⚠️ Our AI tutor is taking a short break right now.\n\n"
        "Try these resources instead:\n"
        "📘 HC Verma / NCERT for theory\n"
        "📗 Arihant for practice questions\n"
        "🔍 YouTube: search '[topic] JEE explained'\n\n"
        "Ask again in a minute — it'll be back soon!"
    ),
    (
        "⚠️ Gemini AI is temporarily unavailable.\n\n"
        "Quick tip: For most JEE doubts, NCERT solutions + PYQs solve 80% of confusion.\n"
        "Please try again shortly!"
    ),
]


async def solve_doubt(question: str) -> str:
    """
    Send question to Gemini and return formatted answer.
    Returns a fallback message if API is unavailable.
    """
    if not _GEMINI_AVAILABLE or _model is None:
        return _FALLBACK_MESSAGES[0]

    # Clean and validate input
    question = question.strip()
    if len(question) < 5:
        return "❓ Please type a proper question. Example: 'What is Gauss's Law?'"
    if len(question) > config.MAX_DOUBT_LENGTH:
        return (
            f"❗ Question too long (max {config.MAX_DOUBT_LENGTH} characters).\n"
            "Please shorten your question."
        )

    full_prompt = _SYSTEM_PROMPT + question

    try:
        # Run blocking Gemini call in thread pool to avoid blocking the event loop
        loop    = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: _model.generate_content(full_prompt)),
            timeout=config.GEMINI_TIMEOUT,
        )

        if response and response.text:
            answer = response.text.strip()
            # Remove any accidental markdown bold/headers
            answer = answer.replace("**", "").replace("##", "").replace("###", "")
            return f"🎓 <b>JEE Doubt Solved</b>\n\n{answer}"
        else:
            logger.warning("[gemini] Empty response from Gemini.")
            return _FALLBACK_MESSAGES[0]

    except asyncio.TimeoutError:
        logger.warning("[gemini] Request timed out.")
        return (
            "⏱ AI tutor is thinking too hard! Request timed out.\n"
            "Please try a shorter/simpler question."
        )
    except Exception as e:
        logger.error(f"[gemini] Error: {e}")
        return _FALLBACK_MESSAGES[1]

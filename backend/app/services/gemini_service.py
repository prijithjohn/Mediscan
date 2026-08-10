import importlib
import re

from fastapi import HTTPException, status

from backend.app.core.config import settings


def _get_gemini_module():
    for module_name in ("google.genai", "google.generativeai"):
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Gemini SDK is not installed. Install google.genai or google-generativeai.",
    )


def _configure_gemini():
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini API key is not configured. Set GEMINI_API_KEY in the environment.",
        )

    genai = _get_gemini_module()
    configure = getattr(genai, "configure", None)
    if not callable(configure):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini SDK does not expose a configure function.",
        )
    configure(api_key=settings.gemini_api_key)


def _normalize_list(text: str) -> list[str]:
    if not text:
        return []

    items = re.split(r"[\n,;]+", text)
    return [item.strip() for item in items if item.strip()]


def _generate_content(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini API key is not configured. Set GEMINI_API_KEY in the environment.",
        )

    _configure_gemini()
    genai = _get_gemini_module()
    model_class = getattr(genai, "GenerativeModel", None)
    if model_class is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini SDK does not expose GenerativeModel.",
        )

    model = model_class("gemini-2.5-flash")
    generate_content = getattr(model, "generate_content", None)
    if not callable(generate_content):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini SDK does not support generate_content.",
        )

    response = generate_content(prompt)
    return getattr(response, "text", "").strip()


def summarize_text(text: str) -> str:
    if not settings.gemini_api_key:
        return text[:250] + ("..." if len(text) > 250 else "")

    prompt = (
        "Summarize the following medical prescription or note into a concise, readable summary."
        f"\n\n{text}"
    )
    return _generate_content(prompt)


def extract_medicines(text: str) -> list[str]:
    if not settings.gemini_api_key:
        return []

    prompt = (
        "Extract the medication names from the following prescription or summary."
        " Return a short comma-separated list." 
        f"\n\n{text}"
    )
    answer = _generate_content(prompt)
    return _normalize_list(answer)


def identify_conditions(text: str) -> list[str]:
    if not settings.gemini_api_key:
        return []

    prompt = (
        "Identify possible medical conditions or diagnoses from the following prescription or summary."
        " Return a list of conditions separated by commas." 
        f"\n\n{text}"
    )
    answer = _generate_content(prompt)
    return _normalize_list(answer)


def extract_warnings(text: str) -> str:
    if not settings.gemini_api_key:
        return "No warnings generated because Gemini API is not configured."

    prompt = (
        "Read the following prescription or summary and extract any safety warnings, precautions,"
        " or patient instructions in a concise paragraph." 
        f"\n\n{text}"
    )
    return _generate_content(prompt)


def assess_emergency_risk(text: str) -> tuple[bool, str]:
    if not settings.gemini_api_key:
        return False, "Emergency assessment skipped because Gemini API is not configured."

    prompt = (
        "Determine whether the following prescription content indicates an immediate emergency"
        " or high-risk condition. Reply with a short answer that begins with Yes or No,"
        " and include a brief reason." 
        f"\n\n{text}"
    )
    answer = _generate_content(prompt)
    return ("yes" in answer.lower(), answer)

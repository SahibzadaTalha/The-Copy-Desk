from dataclasses import dataclass

@dataclass(frozen=True)
class PlatformProfile:
    name: str
    max_characters: int
    structure_note: str
    default_temperature: float

PLATFORM_PROFILES = {
    "linkedin": PlatformProfile("LinkedIn", 3000, "Hook line se start, short paragraphs, soft CTA.", 0.4),
    "instagram": PlatformProfile("Instagram", 2200, "Punchy first line, emoji-friendly, hashtags end mein.", 0.8),
    "email": PlatformProfile("Email", 1500, "Subject line + greeting + short body + ek CTA.", 0.3),
}

TONE_PARAMETERS = {
    "witty": {"temperature": 0.9, "top_p": 0.95},
    "professional": {"temperature": 0.25, "top_p": 0.85},
    "friendly": {"temperature": 0.7, "top_p": 0.9},
    "persuasive": {"temperature": 0.6, "top_p": 0.9},
}
DEFAULT_TONE_PARAMS = {"temperature": 0.5, "top_p": 0.9}

DEFAULT_MODEL = "llama-3.3-70b-versatile"

def resolve_token_param(model: str, requested_tokens: int) -> int:
    return min(max(requested_tokens, 50), 500)

def resolve_generation_params(platform: str, tone: str) -> dict:
    profile = PLATFORM_PROFILES[platform.lower()]
    tone_params = TONE_PARAMETERS.get(tone.lower(), DEFAULT_TONE_PARAMS)
    blended_temp = round((profile.default_temperature + tone_params["temperature"]) / 2, 2)
    return {
        "temperature": blended_temp,
        "top_p": tone_params["top_p"],
        "max_characters": profile.max_characters,
        "structure_note": profile.structure_note,
        "platform_display": profile.name,
    }
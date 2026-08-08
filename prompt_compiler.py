from config import resolve_generation_params

MASTER_SYSTEM_TEMPLATE = """You are a senior marketing copywriter.

BRAND SAFETY RULES:
- Never invent stats/claims not given by the user.
- Stay within platform structure below.

PLATFORM: {platform_display}
STRUCTURE: {structure_note}
CHARACTER LIMIT: {max_characters}
TONE: {tone}

Return ONLY JSON:
{{"headline": "...", "body": "...", "call_to_action": "...", "hashtags": []}}
"""

def compile_prompt(product_description: str, platform: str, tone: str) -> dict:
    gen_params = resolve_generation_params(platform, tone)
    system_prompt = MASTER_SYSTEM_TEMPLATE.format(
        platform_display=gen_params["platform_display"],
        structure_note=gen_params["structure_note"],
        max_characters=gen_params["max_characters"],
        tone=tone,
    )
    user_prompt = f"Product/service description: {product_description}"
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "temperature": gen_params["temperature"],
        "top_p": gen_params["top_p"],
        "max_characters": gen_params["max_characters"],
    }
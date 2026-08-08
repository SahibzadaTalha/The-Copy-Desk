import argparse
import asyncio

from dotenv import load_dotenv

from config import DEFAULT_MODEL, PLATFORM_PROFILES
from engine import generate_many
from prompt_compiler import compile_prompt

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Automated Copywriting & Tone Transformer")
    parser.add_argument("--product", required=True, help="Product name")
    parser.add_argument("--description", required=True, help="Raw product description / facts")
    parser.add_argument("--platform", required=True, help=f"Comma-separated: {list(PLATFORM_PROFILES)}")
    parser.add_argument("--tone", required=True, help="e.g. witty, professional, persuasive, friendly")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true", help="Preview prompt without calling the API")
    return parser.parse_args()


def dry_run_preview(product, description, platforms, tone):
    for platform in platforms:
        compiled = compile_prompt(description, platform, tone)
        print(f"\n--- DRY RUN: {product} / {platform} / {tone} ---")
        print(f"temperature={compiled['temperature']}  top_p={compiled['top_p']}")
        print("System prompt:\n" + compiled["system_prompt"])


def main():
    args = parse_args()
    platforms = [p.strip().lower() for p in args.platform.split(",")]

    if args.dry_run:
        dry_run_preview(args.product, args.description, platforms, args.tone)
        return

    requests = [
        {"product_name": args.product, "product_description": args.description, "platform": p, "tone": args.tone}
        for p in platforms
    ]
    results = asyncio.run(generate_many(requests, model=args.model))

    for r in results:
        limit = PLATFORM_PROFILES[r.platform].max_characters
        print(f"\n=== {r.platform.upper()} ({r.character_count}/{limit} chars, compliant={r.compliance_check(limit)}) ===")
        print(r.full_text)


if __name__ == "__main__":
    main()
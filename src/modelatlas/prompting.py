"""Check a bound prompt's exact text length; this is not a visual quality score."""
import argparse
import hashlib
from importlib.resources import files
import json
from pathlib import Path


def count_detail(text):
    return sum(not char.isspace() for char in text)


def check_prompt(prompt, profile="sivia-overview-v1", template_bytes=None):
    profiles = json.loads(files("modelatlas").joinpath("knowledge/prompt-profiles.json").read_text(encoding="utf-8"))
    if profile not in profiles["profiles"]:
        raise ValueError("Unknown prompt profile")
    binding = profiles["profiles"][profile]
    if template_bytes is not None:
        if hashlib.sha256(template_bytes).hexdigest() != binding["template_sha256"]:
            raise ValueError("Template hash differs from the frozen binding; review a new profile")
        if count_detail(template_bytes.decode("utf-8-sig")) != binding["minimum_non_whitespace_characters"]:
            raise ValueError("Template count differs from the frozen binding")
    length = count_detail(prompt)
    length_pass = length >= binding["minimum_non_whitespace_characters"]
    size_pass = len(prompt) <= binding["maximum_total_characters"]
    return {
        "profile": profile, "binding": binding,
        "total_characters": len(prompt), "non_whitespace_characters": length,
        "submitted_utf8_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "length_pass": length_pass, "tool_limit_pass": size_pass,
        "passed": length_pass and size_pass,
        "template_bytes_verified": template_bytes is not None,
        "scope": "Exact prompt-text length only; source/visual review and user approval are separate.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--profile", default="sivia-overview-v1")
    parser.add_argument("--template", type=Path)
    args = parser.parse_args()
    # Preserve newlines: this same decoded string must be sent to the image tool.
    prompt = args.prompt.read_bytes().decode("utf-8-sig")
    try:
        report = check_prompt(prompt, args.profile, args.template.read_bytes() if args.template else None)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

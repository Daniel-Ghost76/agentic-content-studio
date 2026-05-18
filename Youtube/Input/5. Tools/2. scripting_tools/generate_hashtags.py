#!/usr/bin/env python3
"""
Usage: python3 generate_hashtags.py --title "<title>" [--tools "<tool1>,<tool2>,..."]
Generates 8-12 YouTube hashtags for the YAML description field.

Rules (scripting_rules.md):
- 8-12 hashtags
- broad -> niche order
- Inside the description field, never in a tags list
"""
import argparse
import re

# Hashtag bank: (hashtag, [trigger_keywords])
# Empty keyword list = always eligible (base tags)
# Ordered broad -> niche; first to be selected gets priority slots
HASHTAG_BANK = [
    # Always included
    ("#AI", []),
    ("#ArtificialIntelligence", []),
    # Broad topic
    ("#AITools", ["tool", "workflow", "system", "automat", "build", "agent", "script"]),
    ("#Automation", ["automat", "workflow", "n8n", "zapier", "make", "trigger", "pipeline"]),
    ("#MachineLearning", ["model", "llm", "token", "context", "training", "fine"]),
    ("#LLM", ["llm", "model", "token", "context window", "gpt", "claude", "gemini", "grok"]),
    # Business / channel
    ("#AIBusiness", ["business", "income", "revenue", "client", "freelan", "agency", "skool", "monetis"]),
    ("#BuildingInPublic", ["building", "from scratch", "day 1", "series", "journey", "episode"]),
    ("#OnlineBusiness", ["business", "income", "side hustle", "freelan", "money", "earn"]),
    ("#ContentCreation", ["content", "creator", "video", "channel", "script", "youtube"]),
    ("#YouTubeAutomation", ["youtube", "channel", "video", "transcript", "upload", "publish"]),
    # Workflow / agents
    ("#AIWorkflow", ["workflow", "pipeline", "system", "automat", "agent", "orchestrat"]),
    ("#AIAgents", ["agent", "agentic", "autonomous", "multi.agent", "sub.agent", "orchestrat"]),
    ("#NoCode", ["no.code", "nocode", "n8n", "zapier", "make", "airtable", "without code"]),
    # Learning
    ("#AITutorial", ["tutorial", "how to", "step by step", "guide", "walkthrough"]),
    ("#LearnAI", ["learn", "tutorial", "beginner", "guide", "explain", "understand"]),
    ("#TechEducation", ["explain", "tutorial", "learn", "guide", "how", "what is"]),
    # Tool-specific (niche)
    ("#ClaudeAI", ["claude"]),
    ("#ChatGPT", ["chatgpt", "openai", "gpt-4", "gpt4"]),
    ("#n8n", ["n8n"]),
    ("#ElevenLabs", ["elevenlabs", "scribe", "transcri"]),
    ("#Python", ["python", ".py"]),
    ("#Remotion", ["remotion"]),
    ("#AIStartup", ["startup", "business", "from scratch", "building"]),
]

ALWAYS_INCLUDE = {"#AI", "#ArtificialIntelligence"}
MIN_HASHTAGS = 8
MAX_HASHTAGS = 12


def matches(keyword_pattern: str, text: str) -> bool:
    pattern = keyword_pattern.replace(".", r"[-\s]?")
    return bool(re.search(pattern, text, re.IGNORECASE))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--tools", default="", help="Comma-separated tool names from transcript")
    args = parser.parse_args()

    combined = f"{args.title} {args.tools}".lower()

    selected = list(ALWAYS_INCLUDE)

    for hashtag, keywords in HASHTAG_BANK:
        if hashtag in selected:
            continue
        if not keywords or any(matches(kw, combined) for kw in keywords):
            selected.append(hashtag)
        if len(selected) >= MAX_HASHTAGS:
            break

    # Pad to minimum if needed
    if len(selected) < MIN_HASHTAGS:
        for hashtag, _ in HASHTAG_BANK:
            if hashtag not in selected:
                selected.append(hashtag)
            if len(selected) >= MIN_HASHTAGS:
                break

    result = selected[:MAX_HASHTAGS]

    print("Hashtags for YAML description (broad -> niche):")
    print()
    print(" ".join(result))
    print()
    print(f"({len(result)} hashtags — paste inside the description field, not in a tags list)")


if __name__ == "__main__":
    main()

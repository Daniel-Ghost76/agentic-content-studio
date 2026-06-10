#!/usr/bin/env python3
"""
perplexity_research.py — live, cited web research via Perplexity Sonar.

This is the ideation stage's real-time research layer. Claude has a knowledge
cutoff and no live web; Perplexity fills that gap with cited, current answers.

Reads PERPLEXITY_API_KEY from ~/.claude/.env (never hardcode keys).

USAGE
  python3 perplexity_research.py "any question"          general live research
  python3 perplexity_research.py --saturation "topic"    is this video topic fresh or saturated?
  python3 perplexity_research.py --stats "topic"         current numbers / tool names (Specificity Bank)
  python3 perplexity_research.py --refs "topic"          recent YouTube videos on this topic
  python3 perplexity_research.py --pro "question"        use the larger sonar-pro model
  python3 perplexity_research.py --json "question"       raw JSON (answer + citations) for agents

FLAGS combine, e.g.  --pro --stats "n8n vs make 2026"
"""
import json
import os
import sys
import urllib.request
import urllib.error

ENV_PATH = os.path.expanduser("~/.claude/.env")
API_URL = "https://api.perplexity.ai/chat/completions"


def load_key():
    if not os.path.exists(ENV_PATH):
        sys.exit(f"ERROR: {ENV_PATH} not found.")
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "PERPLEXITY_API_KEY":
                v = v.strip().strip('"').strip("'")
                if v and "REPLACE_ME" not in v:
                    return v
    sys.exit(
        "ERROR: PERPLEXITY_API_KEY missing or unset in ~/.claude/.env.\n"
        "Add a line:  PERPLEXITY_API_KEY=pplx-...."
    )


SYSTEM = {
    "default": "You are a precise research assistant. Answer concisely with current, "
               "factual information and always cite sources.",
    "saturation": "You research YouTube content saturation. For the given topic, report: "
                  "(1) how saturated this topic is on YouTube right now, (2) which big "
                  "channels covered it in the last ~90 days and roughly how it performed, "
                  "(3) the freshest under-covered angle a new creator could take. Be blunt "
                  "about whether it is worth making. Cite sources.",
    "stats": "You gather hard specifics for a video script: real, current numbers, pricing, "
             "version numbers, exact tool/product names, and recent data points on the topic. "
             "Return a tight bulleted list of verifiable facts with dates. Cite every figure.",
    "refs": "You find recent, real YouTube videos on the given topic from credible creators. "
            "For each: title, channel, approximate publish date, and one line on its angle. "
            "Only include videos you can cite a real URL for.",
}


def build_messages(mode, query):
    return [
        {"role": "system", "content": SYSTEM.get(mode, SYSTEM["default"])},
        {"role": "user", "content": query},
    ]


def call(model, messages, key):
    payload = json.dumps({"model": model, "messages": messages}).encode()
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"ERROR {e.code} from Perplexity: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR reaching Perplexity: {e.reason}")


def extract(resp):
    answer = resp.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    cites = resp.get("citations") or []
    if not cites:
        cites = [s.get("url", "") for s in resp.get("search_results", []) if s.get("url")]
    return answer, cites


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    mode = "default"
    model = "sonar"
    as_json = False
    rest = []
    for a in args:
        if a == "--saturation":
            mode = "saturation"
        elif a == "--stats":
            mode = "stats"
        elif a == "--refs":
            mode = "refs"
        elif a == "--pro":
            model = "sonar-pro"
        elif a == "--json":
            as_json = True
        else:
            rest.append(a)
    query = " ".join(rest).strip()
    if not query:
        sys.exit("ERROR: no query provided.")

    key = load_key()
    resp = call(model, build_messages(mode, query), key)
    answer, cites = extract(resp)

    if as_json:
        print(json.dumps({"answer": answer, "citations": cites}, indent=2))
        return

    print(answer)
    if cites:
        print("\nSources:")
        for i, c in enumerate(cites, 1):
            print(f"  [{i}] {c}")


if __name__ == "__main__":
    main()

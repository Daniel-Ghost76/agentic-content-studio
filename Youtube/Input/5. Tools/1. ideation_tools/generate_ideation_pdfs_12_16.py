#!/usr/bin/env python3
"""
Generate ideation PDFs for videos 12-16 of the Building an AI Business From Scratch series.
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUTPUT_DIR = "/Users/danieldanut/Agentic Workspace/Youtube/Output/1. Ideation/"


def make_pdf(filename, sections):
    """
    sections: list of (heading, body_lines)
    body_lines: list of strings. Strings starting with "- " are bullets.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- Header block (frontmatter) ---
    # sections[0] is always the frontmatter block (heading=None, body_lines=lines)
    frontmatter_heading, frontmatter_lines = sections[0]

    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_x(pdf.l_margin)
    # Draw a filled rect for the header
    header_text = "\n".join(frontmatter_lines)
    # Use multi_cell for the dark header
    pdf.set_fill_color(28, 28, 35)
    pdf.multi_cell(
        0, 6, header_text,
        border=0, fill=True,
        new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.ln(4)

    # Reset colours for body
    pdf.set_text_color(20, 20, 20)

    for heading, body_lines in sections[1:]:
        # Section heading
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(230, 230, 240)
        pdf.multi_cell(
            0, 8, heading,
            border=0, fill=True,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        pdf.ln(1)

        pdf.set_font("Helvetica", "", 10)
        for line in body_lines:
            if line == "":
                pdf.ln(3)
            elif line.startswith("- "):
                # Bullet
                bullet_text = line[2:]
                pdf.set_x(pdf.l_margin + 5)
                pdf.multi_cell(
                    0, 6, "- " + bullet_text,
                    border=0,
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
            elif line.startswith("### "):
                # Sub-sub heading
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(
                    0, 6, line[4:],
                    border=0,
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
                pdf.set_font("Helvetica", "", 10)
            elif line.startswith("**") and line.endswith("**"):
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(
                    0, 6, line.strip("*"),
                    border=0,
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
                pdf.set_font("Helvetica", "", 10)
            elif line.startswith("**"):
                # Bold label line (e.g. **Point**: ...)
                # Split at first **: into bold part and normal part
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(
                    0, 6, line.replace("**", ""),
                    border=0,
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
                pdf.set_font("Helvetica", "", 10)
            else:
                pdf.multi_cell(
                    0, 6, line,
                    border=0,
                    new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
        pdf.ln(3)

    out_path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(out_path)
    print(f"Saved: {out_path}")
    return out_path


# ============================================================
# VIDEO 12 -- Claude Workflows Explained
# ============================================================

v12_frontmatter = [
    "---",
    "title: How to Go From Prompting to Building -- Claude Workflows Explained",
    "video no: 12 of 30",
    "series: Building an AI Business From Scratch",
    "voice_reference: ../../Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md",
    "video_type: concept",
    "hook_type: Curiosity-Gap",
    "script_versions: A + B",
    "status: DRAFT",
    "---",
]

v12_sections = [
    (None, v12_frontmatter),

    ("Reference Videos", [
        "- Every Claude Code Workflow Explained (& When to Use Each) (https://www.youtube.com/watch?v=38t5UBCa4OI)",
        "  -- Nate Herk -- Notice how he maps each workflow type to a specific use case rather than listing them abstractly.",
        "",
        "- How I'd Teach a 10 Year Old to Build Agentic Workflows (Claude Code) (https://www.youtube.com/watch?v=3GAxd90fEE4)",
        "  -- Nate Herk -- Notice how the WAT framework (Workflows, Agent, Tools) makes an abstract concept land for a non-technical viewer.",
        "",
        "- From Zero to Your First Agentic AI Workflow in 26 Minutes (Claude Code) (https://www.youtube.com/watch?v=tDGiWn0flK8)",
        "  -- Nate Herk -- Notice the pacing shift: concept explanation is brief, demo is long. Copy that ratio.",
    ]),

    ("The One Thing", [
        "Prompting is talking to AI -- workflows are making AI work for you. The moment you understand the difference, you stop treating Claude like a search engine.",
    ]),

    ("Hook", [
        "Most people are still prompting. There is a completely different way to use Claude -- and it is why some people get 10x more done with the same subscription.",
    ]),

    ("Target Viewer", [
        "Someone who has been using Claude or ChatGPT for months, mostly via chat, and senses there is a more powerful layer they are not accessing yet.",
    ]),

    ("Payoff", [
        "The viewer can describe the difference between a prompt and a workflow, name the three main Claude workflow types (single-agent, multi-agent, automated), and explain why workflows produce more consistent output than back-and-forth chat.",
    ]),

    ("Beat Structure", [
        "### Beat 1 -- The Gap",
        "**Point**: Most people use Claude as a smart autocomplete -- they prompt, it responds, they prompt again. That is the slowest, least consistent way to get value from it.",
        "**Visual**: Side-by-side: a chat thread with 12 back-and-forth messages vs. a single Claude Code run that produces a finished document.",
        "**Target words**: ~150w",
        "",
        "### Beat 2 -- What a Workflow Actually Is",
        "**Point**: A workflow is a set of instructions Claude follows end-to-end, without you hand-holding every step. You define the job once; Claude does it repeatably.",
        "**Visual**: Diagram -- input -> instructions (CLAUDE.md or system prompt) -> Claude -> output. Simple three-box flow.",
        "**Target words**: ~200w",
        "",
        "### Beat 3 -- The Three Workflow Types",
        "**Point**: Single-agent (one Claude instance, one task), multi-agent (Claude instances that hand off to each other), and automated (no human in the loop at all -- triggered by an event or schedule).",
        "**Visual**: Three labelled icons or cards. Each has a one-line example use case (write a script, research + write + review, publish blog post at 9am every day).",
        "**Target words**: ~250w",
        "",
        "### Beat 4 -- Why This Changes How You Think About Cost",
        "**Point**: Workflows shift the value equation. A single prompt costs almost nothing and produces variable output. A well-built workflow costs slightly more per run but produces consistent, production-quality output you can sell or ship.",
        "**Visual**: Two columns -- Prompt (cheap, inconsistent) vs. Workflow (slightly higher token use, consistent, reusable). No invented numbers.",
        "**Target words**: ~180w",
        "",
        "### Beat 5 -- The Entry Point",
        "**Point**: You do not need to learn to code to build your first workflow. A CLAUDE.md file and clear task instructions are enough to go from prompting to building today.",
        "**Visual**: Claude Code terminal with a simple CLAUDE.md open. Just text, no code.",
        "**Target words**: ~150w",
        "",
        "### Beat 6 -- CTA",
        "**Point**: Tease the next video -- context windows -- as the key constraint that makes workflow design decisions make sense.",
        "**Visual**: Text card with next video title.",
        "**Target words**: ~60w",
    ]),

    ("Analogy Bank", [
        "- Prompting vs. workflow: Texting someone a question each time you need something vs. hiring them and writing a job description once.",
        "- Single-agent workflow: A contractor who takes a brief and delivers a finished product -- you do not supervise every step.",
        "- Multi-agent workflow: A small team where one person researches, one writes, one reviews -- Claude plays all the roles.",
    ]),

    ("Thesis Line Location", [
        "Beat 1 -- Prompting is talking to AI. Workflows are making AI work for you.",
    ]),

    ("Framework Phrase", [
        "Talk vs. Build",
    ]),

    ("Specificity Bank", [
        "- Claude Code (Anthropic's agentic interface, distinct from Claude.ai chat)",
        "- CLAUDE.md (the project instruction file that persists across a Claude Code session)",
        "- claude-sonnet-4-5, claude-opus-4 (real model names, do not invent versions)",
        "- Anthropic's published context window for Sonnet: 200,000 tokens",
        "- Sub-agents, skills, and routines (Claude Code's three agentic building blocks as named by Anthropic)",
    ]),

    ("Constraints", [
        "- Do not explain how to build a workflow step by step -- that is a tutorial video, not this one.",
        "- Do not mention n8n, Zapier, or Make -- this video is Claude-native only.",
        "- Avoid the phrase 'artificial intelligence' -- use 'Claude' or 'AI' as a short form only.",
        "- Do not introduce context windows in depth -- that is video 13.",
    ]),

    ("CTA Direction", [
        "Next video: Context Windows Explained -- the invisible limit that determines whether your workflow succeeds or quietly fails halfway through.",
    ]),

    ("Personal Angle [DANIEL TO FILL]", [
        "Suggested: The moment Daniel stopped using Claude as a chat tool and wrote his first CLAUDE.md -- what the output difference looked like, and why it felt like finding a gear he didn't know existed.",
    ]),

    ("Vulnerability Moment [DANIEL TO FILL]", [
        "Suggested: Daniel spent weeks re-prompting Claude in chat to get consistent script drafts, not knowing a single workflow instruction file would have solved the problem on day one.",
        "Note: belongs in Beat 1 -- makes the gap feel personal, not abstract.",
    ]),
]

# ============================================================
# VIDEO 13 -- Context Windows Explained
# ============================================================

v13_frontmatter = [
    "---",
    "title: Why AI Forgets Things -- Context Windows Explained",
    "video no: 13 of 30",
    "series: Building an AI Business From Scratch",
    "voice_reference: ../../Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md",
    "video_type: concept",
    "hook_type: Curiosity-Gap",
    "script_versions: A + B",
    "status: DRAFT",
    "---",
]

v13_sections = [
    (None, v13_frontmatter),

    ("Reference Videos", [
        "- Why LLMs get dumb (Context Windows Explained) (https://www.youtube.com/watch?v=TeQDr4DkLYo)",
        "  -- Independent creator -- Notice the performance-degradation framing: the longer the context, the dumber the model gets. That is the hook mechanism to study.",
        "",
        "- Most devs don't understand how context windows work (https://www.youtube.com/watch?v=-uW5-TaVXu4)",
        "  -- Independent creator -- Notice how the creator reframes context window not as a size fact but as the central design constraint. That reframe is the payoff to reverse-engineer.",
        "",
        "- Every Claude Code Workflow Explained (& When to Use Each) (https://www.youtube.com/watch?v=38t5UBCa4OI)",
        "  -- Nate Herk -- Notice how he structures workflow explanation around constraints -- context management is always the sub-text. Use as pacing reference.",
    ]),

    ("The One Thing", [
        "The context window is not a memory limit -- it is a working desk. Everything on the desk is visible to Claude; everything off the desk is gone. Managing what stays on the desk is the core skill of building with AI.",
    ]),

    ("Hook", [
        "Claude did not forget. It never knew. Here is what is actually happening when your AI loses track of a conversation -- and the three ways to work around it.",
    ]),

    ("Target Viewer", [
        "Someone who has hit the point in a long Claude session where the output started getting weird or wrong, and blamed the AI rather than understanding the structural constraint causing it.",
    ]),

    ("Payoff", [
        "The viewer can explain what a context window is in plain language, describe why performance degrades near the limit, and name at least two practical techniques to manage context (conversation compaction, project files, fresh sessions).",
    ]),

    ("Beat Structure", [
        "### Beat 1 -- The Symptom",
        "**Point**: Mid-conversation, Claude starts contradicting itself, ignoring earlier instructions, or producing worse output than it did at the start. This is not a bug. It is a structural feature of how large language models work.",
        "**Visual**: A chat thread where early responses are sharp and late responses are noticeably worse. Highlight the degradation point.",
        "**Target words**: ~150w",
        "",
        "### Beat 2 -- The Desk Analogy",
        "**Point**: Claude does not have memory between sessions or a running log of your relationship. It only sees what is on its working desk right now. The context window IS the desk. When the desk is full, older content falls off.",
        "**Visual**: Simple graphic: a desk with papers. Papers slide off the left edge as new ones stack on the right.",
        "**Target words**: ~200w",
        "",
        "### Beat 3 -- The Numbers (No Invented Stats)",
        "**Point**: Claude Sonnet has a 200,000-token context window. A token is roughly three-quarters of a word. That sounds enormous until you start attaching files, pasting codebases, or running long agent sessions.",
        "**Visual**: Text card: 200,000 tokens. Below it: approximate page counts for reference (a 200-page book is roughly 50,000 tokens). Real published figures only.",
        "**Target words**: ~180w",
        "",
        "### Beat 4 -- Why It Gets Worse Before It Falls Off",
        "**Point**: Research on large language models shows that attention quality degrades as the context fills -- not just at the cutoff point. The model pays most attention to what is at the start and end of the context, and progressively less to the middle. This is called the lost-in-the-middle problem.",
        "**Visual**: A attention-distribution curve -- high at start, low in middle, recovers slightly at end. Label the dip 'lost in the middle.'",
        "**Target words**: ~180w",
        "",
        "### Beat 5 -- Three Ways to Work Around It",
        "**Point**: (1) Conversation compaction -- Claude Code's built-in feature that summarises old context before the window fills. (2) Project files and CLAUDE.md -- keep persistent instructions out of the conversation so they don't consume window space. (3) Fresh sessions -- for long workflows, design them so each stage starts clean with only the inputs it needs.",
        "**Visual**: Three labelled cards, one per technique. Each card has a one-line description.",
        "**Target words**: ~220w",
        "",
        "### Beat 6 -- CTA",
        "**Point**: Tease the next video -- tokens -- as the unit that determines how much fits in the window and how much each session costs.",
        "**Visual**: Text card with next video title.",
        "**Target words**: ~60w",
    ]),

    ("Analogy Bank", [
        "- Context window: A physical desk. You can only work with what is on it. When it fills up, you push old papers off to make room.",
        "- Lost-in-the-middle problem: Reading a 300-page document and only really absorbing the first chapter and the last paragraph -- everything in the middle becomes blur.",
        "- Conversation compaction: A meeting secretary who summarises the last two hours of discussion into a one-page brief before the next session starts.",
    ]),

    ("Thesis Line Location", [
        "Beat 2 -- The context window is not a memory limit. It is a working desk. Managing what stays on it is the core skill.",
    ]),

    ("Framework Phrase", [
        "Manage the Desk",
    ]),

    ("Specificity Bank", [
        "- Claude Sonnet (claude-sonnet-4-5): 200,000 token context window (Anthropic published)",
        "- 'Lost in the middle' -- documented phenomenon in LLM attention research (Liu et al., 2023)",
        "- Claude Code conversation compaction -- Anthropic's built-in context management feature",
        "- Token-to-word ratio: approximately 1 token per 0.75 words (OpenAI's published approximation, widely used as industry standard)",
    ]),

    ("Constraints", [
        "- Do not explain tokens in depth -- that is video 14.",
        "- Do not turn this into a technical deep dive on transformer attention mechanisms.",
        "- Avoid the phrase 'training data' -- the context window is a runtime concept, not a training concept.",
        "- Do not recommend third-party memory tools by name -- keep it to Claude-native solutions.",
    ]),

    ("CTA Direction", [
        "Next video: Tokens Explained -- the unit Claude actually reads in, why it matters for your subscription, and how to stop burning through your limit on things that don't move the needle.",
    ]),

    ("Personal Angle [DANIEL TO FILL]", [
        "Suggested: A specific session where Daniel was deep into a complex workflow and Claude's output quality visibly degraded -- the moment he realised the issue was not the model, it was the desk.",
    ]),

    ("Vulnerability Moment [DANIEL TO FILL]", [
        "Suggested: Daniel rebuilt the same workflow three times blaming his prompts, before discovering the actual problem was that his context window was filling up with junk (old conversation history, pasted files) and Claude was losing track of the original instructions.",
        "Note: belongs in Beat 1 -- lands the symptom with lived credibility before the explanation.",
    ]),
]

# ============================================================
# VIDEO 14 -- Tokens Explained
# ============================================================

v14_frontmatter = [
    "---",
    "title: Tokens Explained -- How to Get More Value From Your AI Subscription",
    "video no: 14 of 30",
    "series: Building an AI Business From Scratch",
    "voice_reference: ../../Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md",
    "video_type: concept",
    "hook_type: Bold-Claim",
    "script_versions: A + B",
    "status: DRAFT",
    "---",
]

v14_sections = [
    (None, v14_frontmatter),

    ("Reference Videos", [
        "- Understanding Tokens in AI: How Much Are Your LLM Requests REALLY Costing You? (https://www.youtube.com/watch?v=ZUCVRppXPSc)",
        "  -- Independent creator -- Notice the cost-framing: tokens as currency. That framing is the hook engine for the Bold-Claim hook type.",
        "",
        "- Tokens in AI - Explained (https://www.youtube.com/watch?v=S5Uo3qS9wOc)",
        "  -- Independent creator -- Notice how the creator grounds the token concept in a concrete word-to-token example before going abstract. Mirror that sequence.",
        "",
        "- How I'd Teach a 10 Year Old to Build Agentic Workflows (Claude Code) (https://www.youtube.com/watch?v=3GAxd90fEE4)",
        "  -- Nate Herk -- Use as pacing reference for how Nate handles concept-to-practical transitions without a live demo.",
    ]),

    ("The One Thing", [
        "Tokens are the currency of every AI interaction -- every word you type, every file you attach, and every response Claude writes costs tokens. Understanding this one concept changes how you prompt, what you attach, and how much value you get per dollar.",
    ]),

    ("Hook", [
        "Most people are wasting at least 30 percent of their AI subscription on tokens that do nothing. Here is what a token actually is and the three changes that will immediately get you more output for less spend.",
    ]),

    ("Target Viewer", [
        "Someone paying for Claude Pro or an API plan who has no idea why they hit usage limits, what a token is, or why some interactions feel expensive compared to their output value.",
    ]),

    ("Payoff", [
        "The viewer understands what a token is, can estimate rough token cost for common actions (short prompt, long file attachment, image), and knows three concrete techniques to reduce waste: compressed instructions, selective file attachment, and model tier matching.",
    ]),

    ("Beat Structure", [
        "### Beat 1 -- The Bold Claim Setup",
        "**Point**: Your AI subscription is a token budget, not a time budget. If you treat it like unlimited chat, you will burn through your allocation on overhead before you get to the actual work.",
        "**Visual**: An AI subscription usage bar at 80 percent, mid-month. No invented numbers -- visual metaphor only.",
        "**Target words**: ~130w",
        "",
        "### Beat 2 -- What a Token Actually Is",
        "**Point**: A token is not a word. It is a chunk of text -- typically three to four characters. 'unbelievable' might be two tokens. 'AI' is one. Claude does not read words. It reads tokens. Everything gets converted before Claude ever sees it.",
        "**Visual**: A text string split into colour-coded token chunks. Use the OpenAI tokenizer visual as a reference style. Real example: 'Building an AI business from scratch' shown as token segments.",
        "**Target words**: ~200w",
        "",
        "### Beat 3 -- Input Tokens vs. Output Tokens",
        "**Point**: Every message has two token costs: what you send in (input tokens) and what Claude sends back (output tokens). Output tokens are typically priced higher per token than input tokens on API plans. Most people only think about what they type, not what comes back.",
        "**Visual**: Diagram -- arrow in (input) and arrow out (output). Label each with relative cost indicator (input = lower, output = higher).",
        "**Target words**: ~180w",
        "",
        "### Beat 4 -- Where Tokens Get Wasted",
        "**Point**: Three common waste sources: (1) Pasting entire documents when only a section is relevant. (2) Verbose system prompts with redundant instructions. (3) Using a high-capability model (Opus) for tasks a smaller model (Haiku) handles just as well.",
        "**Visual**: Three icons labelled Document Paste, Bloated Prompt, Wrong Model. Each with a red X.",
        "**Target words**: ~200w",
        "",
        "### Beat 5 -- Three Changes That Pay Off Immediately",
        "**Point**: (1) Compress instructions -- remove filler words from prompts, use bullet points not paragraphs. (2) Attach only what Claude needs -- excerpt the relevant section, not the full file. (3) Match model to task -- Haiku for formatting and extraction, Sonnet for reasoning, Opus for highest-stakes decisions.",
        "**Visual**: Three before/after examples. Same task, different token approaches. Highlight the token count difference (directional, not fabricated numbers).",
        "**Target words**: ~220w",
        "",
        "### Beat 6 -- CTA",
        "**Point**: Tease the next video -- API, CLI, and MCP -- as the layer below the chat interface where token control becomes granular.",
        "**Visual**: Text card with next video title.",
        "**Target words**: ~60w",
    ]),

    ("Analogy Bank", [
        "- Tokens as currency: Every AI interaction is a transaction. You have a budget. Knowing what each action costs lets you spend smarter.",
        "- Token chunks: Think of tokens as syllable-sized bites. The AI does not eat whole words -- it eats bites. Some words are one bite, some are three.",
        "- Model tier matching: You would not hire a senior lawyer to file a form. Match the skill level (and cost) to the complexity of the task.",
    ]),

    ("Thesis Line Location", [
        "Beat 1 -- Your AI subscription is a token budget, not a time budget. Understanding that changes everything.",
    ]),

    ("Framework Phrase", [
        "Token Budget Mindset",
    ]),

    ("Specificity Bank", [
        "- Claude Haiku, Claude Sonnet, Claude Opus -- three real model tiers with different capability and cost profiles (Anthropic published)",
        "- Anthropic API pricing page: input vs. output token cost differential is public (do not invent exact figures -- direct viewer to anthropic.com/pricing)",
        "- Token-to-word approximation: ~1 token per 0.75 words (industry-standard approximation)",
        "- Claude Pro plan: usage limits reset monthly (Anthropic published)",
        "- OpenAI tokenizer tool (platform.openai.com/tokenizer) -- useful for visualising token splits even if using Claude",
    ]),

    ("Constraints", [
        "- Do not invent specific token counts or dollar costs -- direct viewers to Anthropic's pricing page.",
        "- Do not explain the context window in depth -- that was video 13.",
        "- Avoid getting into model training or how tokenisation works at the BPE algorithm level.",
        "- Do not recommend third-party token-counting tools beyond mentioning the OpenAI tokenizer as a reference.",
    ]),

    ("CTA Direction", [
        "Next video: API, CLI, and MCP -- the beginner guide to AI tool access and why understanding these three unlocks a completely different level of control over what Claude can do.",
    ]),

    ("Personal Angle [DANIEL TO FILL]", [
        "Suggested: The first time Daniel saw his API bill and did not understand why certain sessions cost so much more than others -- and the specific realisation (wrong model tier, bloated system prompt, or massive file paste) that changed his cost per output ratio.",
    ]),

    ("Vulnerability Moment [DANIEL TO FILL]", [
        "Suggested: Daniel was pasting entire research documents into Claude and wondering why he burned through his Pro limit so fast -- turns out he was using 90 percent of the tokens on context that Claude never actually needed for the specific task.",
        "Note: belongs in Beat 4 -- makes the waste sources feel real rather than theoretical.",
    ]),
]

# ============================================================
# VIDEO 15 -- API CLI MCP
# ============================================================

v15_frontmatter = [
    "---",
    "title: API vs CLI vs MCP -- The Beginner Guide to AI Tool Access",
    "video no: 15 of 30",
    "series: Building an AI Business From Scratch",
    "voice_reference: ../../Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md",
    "video_type: concept",
    "hook_type: Curiosity-Gap",
    "script_versions: A + B",
    "status: DRAFT",
    "---",
]

v15_sections = [
    (None, v15_frontmatter),

    ("Reference Videos", [
        "- You Need to Learn MCP RIGHT NOW (https://www.youtube.com/watch?v=7h3Bfzxv_wI)",
        "  -- NetworkChuck -- Notice how he leads with 'why it matters' before 'what it is.' That ordering keeps a non-technical audience engaged through a technical concept.",
        "",
        "- you need to learn MCP RIGHT NOW!! (Model Context Protocol) (https://www.youtube.com/watch?v=GuTcle5edjk)",
        "  -- NetworkChuck -- Notice the energy level and the practical demo structure. Reference for pacing a concept explainer that stays kinetic without a live build.",
        "",
        "- How to Build $10,000 Agentic Workflows (Claude Code Tutorial) (https://www.youtube.com/watch?v=vFepZE_wrfg)",
        "  -- Nate Herk -- Notice how API access is treated as a given prerequisite in agentic workflow videos. Use this to frame why understanding API/CLI/MCP matters for the series arc.",
    ]),

    ("The One Thing", [
        "API, CLI, and MCP are three different doors into the same building. Which door you use depends on what you are building. Most beginners do not know the doors exist -- let alone which one to choose.",
    ]),

    ("Hook", [
        "Everyone keeps saying to get API access and set up MCP. But no one explains what any of those words actually mean or which one you need. This video fixes that in under ten minutes.",
    ]),

    ("Target Viewer", [
        "Someone who has seen these terms in tutorials and installation guides, nodded along, and quietly had no idea what they were actually doing or why -- but was too embarrassed to ask.",
    ]),

    ("Payoff", [
        "The viewer can explain in plain language what an API is, what a CLI is, and what MCP is, can identify which one applies to a scenario they are in, and knows the sequence in which to learn them as they level up.",
    ]),

    ("Beat Structure", [
        "### Beat 1 -- The Three Doors",
        "**Point**: There are three different ways to access and extend Claude's capabilities beyond the chat interface. They are not competing options -- they are layers. Most builders end up using all three at some point.",
        "**Visual**: A building with three labelled doors: API, CLI, MCP. Simple graphic -- no code visible yet.",
        "**Target words**: ~130w",
        "",
        "### Beat 2 -- The API: The Programmatic Door",
        "**Point**: An API (Application Programming Interface) is how software talks to other software. When you use the Claude API, your code sends a message to Anthropic's servers and gets a response back -- just like the chat interface, but without the human in the middle. This is how you build products that use Claude.",
        "**Visual**: Diagram -- your app on the left, Anthropic API in the middle, Claude response on the right. Arrow flow. No code.",
        "**Target words**: ~200w",
        "",
        "### Beat 3 -- The CLI: The Terminal Door",
        "**Point**: A CLI (Command-Line Interface) is a text-based way to run software directly on your computer. Claude Code runs in the CLI. Instead of clicking buttons in a browser, you type commands in a terminal and Claude executes tasks directly on your machine -- reading files, writing code, running scripts.",
        "**Visual**: A terminal window with a simple Claude Code command. The output is readable text, not code. Emphasis on what it does, not how it works.",
        "**Target words**: ~200w",
        "",
        "### Beat 4 -- MCP: The Integration Door",
        "**Point**: MCP (Model Context Protocol) is a standard that lets Claude connect to external tools and data sources in a consistent way. Without MCP, connecting Claude to a tool is custom work every time. With MCP, any tool that supports the protocol can plug into Claude the same way. It is the USB standard of AI integrations.",
        "**Visual**: Diagram -- Claude in the centre, MCP connector arrows pointing to Gmail, Google Drive, a database, a browser. Each arrow is the same shape (standardised).",
        "**Target words**: ~220w",
        "",
        "### Beat 5 -- Which One Do You Need?",
        "**Point**: If you are building a product that uses Claude under the hood -- API. If you are running Claude Code to do work on your machine -- CLI. If you want Claude to connect to an external tool like Gmail or a database without custom code -- MCP. In practice, agentic workflows use all three.",
        "**Visual**: Decision tree graphic. Three branches from 'What are you trying to do?' leading to API, CLI, or MCP.",
        "**Target words**: ~180w",
        "",
        "### Beat 6 -- CTA",
        "**Point**: Tease the next video -- AI Agents Explained -- as the place where API, CLI, and MCP all come together into a system that can work on its own.",
        "**Visual**: Text card with next video title.",
        "**Target words**: ~60w",
    ]),

    ("Analogy Bank", [
        "- API: A waiter at a restaurant. You do not go into the kitchen yourself -- you place an order through the waiter (the API), and the kitchen (Claude) prepares it and sends it back.",
        "- CLI: The back door into the kitchen. You go directly and work with the tools yourself. More control, less hand-holding.",
        "- MCP: A universal power adapter. Every country has different outlets (tools). MCP is the adapter that makes Claude's plug work in all of them without rewiring anything.",
    ]),

    ("Thesis Line Location", [
        "Beat 1 -- API, CLI, and MCP are three doors into the same building. Which door you use depends on what you are building.",
    ]),

    ("Framework Phrase", [
        "Three Doors In",
    ]),

    ("Specificity Bank", [
        "- Claude API -- Anthropic's published REST API at api.anthropic.com",
        "- Claude Code -- Anthropic's CLI tool for agentic development (runs in terminal)",
        "- MCP -- Model Context Protocol, open-sourced by Anthropic in November 2024",
        "- MCP servers available for: Google Drive, Gmail, GitHub, Slack, PostgreSQL (Anthropic's published MCP server list)",
        "- Anthropic API key -- required to access the API, generated at console.anthropic.com",
    ]),

    ("Constraints", [
        "- Do not write any actual code in this video -- concept only.",
        "- Do not conflate the Claude.ai chat interface with the API -- they are different access layers.",
        "- Avoid deep technical descriptions of HTTP requests, JSON payloads, or authentication flows.",
        "- Do not cover n8n or Zapier -- keep this Claude-native.",
    ]),

    ("CTA Direction", [
        "Next video: AI Agents Explained -- how the API, CLI, and MCP combine into a system that can plan, act, and complete multi-step tasks without you in the loop.",
    ]),

    ("Personal Angle [DANIEL TO FILL]", [
        "Suggested: The first time Daniel set up an MCP server and Claude could suddenly access his Google Drive -- the specific realisation of what 'extending Claude' actually means when you see it work.",
    ]),

    ("Vulnerability Moment [DANIEL TO FILL]", [
        "Suggested: Daniel followed a tutorial that said 'just use the API' and had no idea what that meant, what key to get, or why his first API call failed -- and the embarrassingly simple fix that unlocked it.",
        "Note: belongs in Beat 2 -- normalises beginner confusion before the clear explanation lands.",
    ]),
]

# ============================================================
# VIDEO 16 -- AI Agents Explained
# ============================================================

v16_frontmatter = [
    "---",
    "title: How AI Agents Actually Work Behind the Scenes",
    "video no: 16 of 30",
    "series: Building an AI Business From Scratch",
    "voice_reference: ../../Input/4. Resources/2. scripting_resources/voice_reference/nate_herk_voice_reference.md",
    "video_type: concept",
    "hook_type: Curiosity-Gap",
    "script_versions: A + B",
    "status: DRAFT",
    "---",
]

v16_sections = [
    (None, v16_frontmatter),

    ("Reference Videos", [
        "- Learn 90% of Building AI Agents in 30 Minutes (https://www.youtube.com/watch?v=i5kwX7jeWL8)",
        "  -- Cole Medin -- Notice how he separates the concept layer (what an agent is) from the build layer (how to make one). This video covers the concept layer only. Use Cole's concept beats as a structural reference.",
        "",
        "- AI Agents Explained - How They Actually Work (https://www.youtube.com/watch?v=g24tJk8Flsk)",
        "  -- Independent creator -- Notice the loop structure explanation: perceive, think, act, repeat. That four-step loop is the mechanical model to reference and simplify.",
        "",
        "- I built 500+ AI agents, here's everything I know -- Nate Herk (https://www.youtube.com/watch?v=Svp7fbF0g2I)",
        "  -- Nate Herk -- Notice how Nate handles the authority framing for an 'explained' video vs. a build video. Energy is more measured, pacing is slower on concept beats.",
    ]),

    ("The One Thing", [
        "An AI agent is not magic -- it is a loop. Claude reads a goal, decides an action, uses a tool, reads the result, and loops until the task is done. Once you see the loop, every agent behaviour makes sense.",
    ]),

    ("Hook", [
        "Everyone is talking about AI agents like they are science fiction. They are not. Here is exactly what is happening inside every agent -- in plain English -- so you can actually build with them.",
    ]),

    ("Target Viewer", [
        "Someone who has heard the phrase 'AI agent' dozens of times, has a rough sense it means AI that does things autonomously, but could not explain the mechanics if asked -- and wants to change that.",
    ]),

    ("Payoff", [
        "The viewer can explain the agent loop (perceive, reason, act, observe), describe the role of tools in enabling agent actions, and articulate the difference between a single-step AI response and a multi-step agent run.",
    ]),

    ("Beat Structure", [
        "### Beat 1 -- The Confusion Setup",
        "**Point**: The phrase 'AI agent' is everywhere and means different things to different people. Some use it to mean any AI assistant. The accurate definition is more specific -- and once you have it, everything else in the AI space clicks into place.",
        "**Visual**: Word cloud or montage of 'AI agent' being used in different contexts -- from chatbots to autonomous coding systems. Show the span of confusion.",
        "**Target words**: ~130w",
        "",
        "### Beat 2 -- The Definition That Actually Holds",
        "**Point**: An AI agent is a system that can perceive its environment, make decisions, take actions using tools, observe the results, and loop -- repeating until a goal is completed. The key word is loop. A single Claude response is not an agent. An agent runs the loop.",
        "**Visual**: The loop diagram -- four boxes in a circle: Perceive -> Reason -> Act -> Observe. Arrow from Observe back to Perceive. Clean, minimal.",
        "**Target words**: ~200w",
        "",
        "### Beat 3 -- Tools: What Give an Agent Hands",
        "**Point**: A raw language model can only produce text. An agent has tools -- functions it can call to take real-world actions. Read a file. Search the web. Send an email. Write code and run it. The tools are what separate a conversational AI from an agent that can do work.",
        "**Visual**: Claude in the centre. Tool icons around it: file system, web search, email, code runner, calendar. Each icon has a label. No code.",
        "**Target words**: ~200w",
        "",
        "### Beat 4 -- A Real Loop in Plain English",
        "**Point**: Walk through one agent run step by step. Example: You ask Claude Code to research a topic and write a brief. Step 1 -- it reads your request (perceive). Step 2 -- it decides to search the web first (reason). Step 3 -- it calls the search tool (act). Step 4 -- it reads the results (observe). Then it loops: decides to write a draft next, writes it, observes the output, decides it is done. Loop ends.",
        "**Visual**: The loop diagram animated step by step with the research example overlaid. Each step lights up as the narration walks through it.",
        "**Target words**: ~220w",
        "",
        "### Beat 5 -- Why This Changes How You Think About Building",
        "**Point**: Once you see the loop, you realise that designing an agent is mostly about two things: (1) giving it the right tools, and (2) writing clear enough instructions that its reasoning at each step stays on track. Everything else -- memory, multi-agent coordination, cost management -- is built on top of this loop.",
        "**Visual**: The loop diagram again, with two labels: 'tools' pointing at the Act node and 'instructions' pointing at the Reason node.",
        "**Target words**: ~180w",
        "",
        "### Beat 6 -- CTA",
        "**Point**: Tease the next video -- AI Rules Explained -- as the practical guide to writing the instructions that keep an agent's reasoning on track.",
        "**Visual**: Text card with next video title.",
        "**Target words**: ~60w",
    ]),

    ("Analogy Bank", [
        "- The agent loop: A chef reading a recipe (perceive), deciding the next step (reason), performing it (act), tasting the result (observe), and adjusting until the dish is done. The recipe does not cook itself -- the chef loops through it.",
        "- Tools giving an agent hands: A brilliant strategist who can only speak. Give them a phone, a computer, and a car -- and suddenly they can execute, not just advise.",
        "- Multi-step vs. single-step: Asking someone a question (single response) vs. hiring them to complete a project (they plan, act, check their work, and report back when done).",
    ]),

    ("Thesis Line Location", [
        "Beat 2 -- An AI agent is a loop. Perceive, reason, act, observe -- repeat until done. Once you see the loop, every agent behaviour makes sense.",
    ]),

    ("Framework Phrase", [
        "The Agent Loop",
    ]),

    ("Specificity Bank", [
        "- Claude Code -- Anthropic's agentic CLI, which runs agent loops natively",
        "- Tool use (function calling) -- Anthropic's published capability that enables agents to call external functions",
        "- Sub-agents in Claude Code -- Claude Code can spin up sub-agent instances to parallelise tasks (Anthropic documentation)",
        "- ReAct pattern (Reason + Act) -- the published prompting framework that underlies most agent loop implementations (Yao et al., 2022)",
        "- MCP tools -- the standardised mechanism for extending what an agent can act on (see video 15)",
    ]),

    ("Constraints", [
        "- Do not build a live agent in this video -- concept only.",
        "- Do not cover multi-agent coordination in depth -- that is a later video.",
        "- Avoid the phrase 'autonomous AI' without immediately grounding it in the loop definition.",
        "- Do not introduce RAG (retrieval-augmented generation) -- keep the concept surface clean.",
    ]),

    ("CTA Direction", [
        "Next video: AI Rules Explained -- how to write the instructions that sit in the Reason node and keep your agent from going off the rails.",
    ]),

    ("Personal Angle [DANIEL TO FILL]", [
        "Suggested: The first time Daniel watched Claude Code run a multi-step task end to end -- the specific moment when he realised it was not just generating text but actually looping through decisions and tool calls. What that felt like to watch.",
    ]),

    ("Vulnerability Moment [DANIEL TO FILL]", [
        "Suggested: Daniel built what he thought was an 'AI agent' that was actually just a long prompt with no tool access -- and discovered the difference the hard way when it could not actually do anything beyond producing text.",
        "Note: belongs in Beat 3 -- makes the tools beat land with practical weight.",
    ]),
]


# ============================================================
# GENERATE ALL PDFs
# ============================================================

saved_files = []

saved_files.append(make_pdf("12. Claude_Workflows_Explained.pdf", v12_sections))
saved_files.append(make_pdf("13. Context_Windows_Explained.pdf", v13_sections))
saved_files.append(make_pdf("14. Tokens_Explained.pdf", v14_sections))
saved_files.append(make_pdf("15. API_CLI_MCP.pdf", v15_sections))
saved_files.append(make_pdf("16. AI_Agents_Explained.pdf", v16_sections))

print("\nAll 5 PDFs saved:")
for f in saved_files:
    print(f"  {f}")

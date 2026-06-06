#!/usr/bin/env python3
"""Create YouTube thumbnail concepts and a deterministic 1280x720 PNG."""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[4]
REVIEW_ROOT = ROOT / "Youtube" / "Output" / "6. Review  "
SCRIPTS_ROOT = ROOT / "Youtube" / "Output" / "2. Scripts"
STYLE_REFERENCE = Path("/Users/danieldanut/Downloads/www.youtube.com_@nateherk_videos.png")
W, H = 1280, 720


@dataclass
class Concept:
    name: str
    hook: str
    metaphor: str
    face: str
    background: str
    supporting: str
    scores: dict[str, int]

    @property
    def total(self) -> int:
        return sum(self.scores.values())


def clean_text(text: str) -> str:
    text = re.sub(r"\d{1,2}:\d{2}(?::\d{2})?,\d{3}\s*-->\s*\d{1,2}:\d{2}(?::\d{2})?,\d{3}", " ", text)
    text = re.sub(r"^\d+$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugish(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def is_project_id(value: str) -> bool:
    return bool(re.fullmatch(r"\d{2}(?:[_-][a-z0-9]+)+", value))


def find_review_folder(target: str | None) -> Path:
    folders = [p for p in REVIEW_ROOT.iterdir() if p.is_dir()]
    if not folders:
        raise SystemExit(f"No review folders found in {REVIEW_ROOT}")
    if not target:
        return max(folders, key=lambda p: p.stat().st_mtime)

    exact_name = [p for p in folders if p.name == target]
    if exact_name:
        return exact_name[0]

    wanted = slugish(target)
    exact = [p for p in folders if slugish(p.name) == wanted]
    if exact:
        return exact[0]
    partial = [p for p in folders if wanted in slugish(p.name) or slugish(p.name) in wanted]
    if len(partial) == 1:
        return partial[0]
    if partial:
        names = "\n".join(f"- {p.name}" for p in partial)
        raise SystemExit(f"Target is ambiguous. Matches:\n{names}")
    raise SystemExit(f"No review folder matched: {target}")


def read_source(folder: Path) -> tuple[Path, str]:
    project_id = folder.name
    txts = sorted(folder.glob(f"{project_id}_review_transcript.txt")) or sorted(folder.glob("*.txt"))
    if txts:
        return txts[0], clean_text(txts[0].read_text(encoding="utf-8", errors="ignore"))

    srts = sorted(folder.glob(f"{project_id}_review_subtitles.srt")) or sorted(folder.glob("*.srt"))
    if srts:
        return srts[0], clean_text(srts[0].read_text(encoding="utf-8", errors="ignore"))

    candidate = slugish(folder.name)
    pdfs = sorted((SCRIPTS_ROOT / project_id).glob(f"{project_id}_script.pdf"))
    if not pdfs:
        pdfs = sorted(SCRIPTS_ROOT.glob(f"*/{project_id}_script.pdf"))
    for pdf in pdfs:
        if slugish(pdf.stem) in candidate or candidate in slugish(pdf.stem):
            return pdf, read_pdf_text(pdf)

    raise SystemExit(f"No .txt, .srt, or matching script PDF found for {folder.name}")


def read_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:
        raise SystemExit(f"PDF fallback needs pypdf installed. Could not read {path}: {exc}") from exc

    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return clean_text(text)


def transcript_topics(text: str) -> set[str]:
    words = set(re.findall(r"[a-zA-Z][a-zA-Z0-9'-]{2,}", text.lower()))
    topics = set()
    mapping = {
        "transcript": {"transcript", "transcripts", "caption", "captions", "transcribe", "transcribed"},
        "youtube": {"youtube", "videos", "channel", "creator", "url", "urls"},
        "automation": {"automation", "workflow", "system", "python", "terminal", "code", "script"},
        "business": {"business", "offers", "landing", "sales", "ads", "customers", "market"},
        "ai": {"ai", "chatgpt", "claude", "agent", "assistant"},
        "data": {"data", "research", "stats", "metrics", "knowledge", "base"},
    }
    for topic, keys in mapping.items():
        if words & keys:
            topics.add(topic)
    return topics


def generate_concepts(text: str) -> list[Concept]:
    topics = transcript_topics(text)
    if {"transcript", "youtube"} <= topics:
        return [
            Concept(
                "Copy The Transcript System",
                "COPY THIS SYSTEM",
                "YouTube videos flowing into a clean transcript file, with a big green check.",
                "Daniel on the right, confident expression, pointing toward the workflow.",
                "Dark YouTube interface grid with bright teal arrows and orange app badges.",
                "YouTube icon, CSV sheet, terminal, transcript document, ChatGPT badge.",
                {"curiosity": 9, "clarity": 9, "emotion": 7, "readability": 9},
            ),
            Concept(
                "500 Videos To Data",
                "500 VIDEOS",
                "A stack of YouTube cards compressed into one glowing data document.",
                "Daniel cropped on the lower right with surprised/this-is-easy expression.",
                "Black background, teal document glow, orange count badge.",
                "Video cards, document icon, terminal prompt, progress bar.",
                {"curiosity": 8, "clarity": 8, "emotion": 8, "readability": 10},
            ),
            Concept(
                "Stop Guessing",
                "STOP GUESSING",
                "Messy creator research on the left, clean transcript database on the right.",
                "Daniel centered-right, holding the viewer's attention between both sides.",
                "Before/after split: red messy side, teal clean side.",
                "Red X, green check, transcript rows, search icon.",
                {"curiosity": 8, "clarity": 8, "emotion": 9, "readability": 9},
            ),
        ]

    if "automation" in topics or "ai" in topics:
        return [
            Concept(
                "Build The System",
                "BUILD THIS",
                "A simple AI workflow with three large connected steps.",
                "Daniel on right, pointing into the steps.",
                "Dark tech background with teal connectors and orange tool badges.",
                "ChatGPT badge, terminal icon, file icon.",
                {"curiosity": 8, "clarity": 8, "emotion": 7, "readability": 9},
            ),
            Concept(
                "Takes 5 Minutes",
                "TAKES 5 MINS",
                "A timer beside a finished workflow dashboard.",
                "Daniel surprised on left, dashboard on right.",
                "Black and white base with orange timer and teal success glow.",
                "Timer, checkmark, code window.",
                {"curiosity": 9, "clarity": 7, "emotion": 8, "readability": 9},
            ),
            Concept(
                "No Code Needed",
                "NO CODE?",
                "A terminal and ChatGPT window doing the heavy lifting.",
                "Daniel right side, skeptical expression.",
                "Dark desktop interface with bright app icons.",
                "ChatGPT, terminal, file system.",
                {"curiosity": 8, "clarity": 7, "emotion": 8, "readability": 9},
            ),
        ]

    return [
        Concept(
            "One Simple System",
            "COPY THIS",
            "A clean workflow diagram turning messy inputs into a useful output.",
            "Daniel on the right as the human anchor.",
            "Dark background with teal lines and orange highlight badges.",
            "Input cards, output file, checkmark.",
            {"curiosity": 8, "clarity": 8, "emotion": 7, "readability": 9},
        ),
        Concept(
            "Old Vs New",
            "OLD vs NEW",
            "A direct comparison between the slow way and the new system.",
            "Daniel centered between both sides.",
            "Split background, red old side and teal new side.",
            "X mark, checkmark, app badge.",
            {"curiosity": 8, "clarity": 9, "emotion": 8, "readability": 9},
        ),
        Concept(
            "It Actually Works",
            "IT WORKS",
            "A finished result screen with a big success badge.",
            "Daniel lower right, excited expression.",
            "Dark UI dashboard with a bright green success state.",
            "Progress bar, checkmark, document icon.",
            {"curiosity": 7, "clarity": 8, "emotion": 8, "readability": 9},
        ),
    ]


def write_concepts(path: Path, video_name: str, source: Path, concepts: list[Concept], recommended: Concept) -> None:
    lines = [
        f"# {video_name} Thumbnail Concepts",
        "",
        f"Source: `{source}`",
        f"Style reference: `{STYLE_REFERENCE}`",
        "",
        f"Recommended: **{recommended.name}** (`{recommended.hook}`)",
        "",
    ]
    for index, concept in enumerate(concepts, start=1):
        score = " / ".join(f"{k}: {v}" for k, v in concept.scores.items())
        lines.extend(
            [
                f"## {index}. {concept.name}",
                "",
                f"- Hook: `{concept.hook}`",
                f"- Visual metaphor: {concept.metaphor}",
                f"- Face placement: {concept.face}",
                f"- Background: {concept.background}",
                f"- Supporting elements: {concept.supporting}",
                f"- Scores: {score}",
                f"- Total: {concept.total}/40",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_concepts_if_needed(path: Path, video_name: str, source: Path, concepts: list[Concept], recommended: Concept, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    write_concepts(path, video_name, source, concepts, recommended)
    return True


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            pass
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_glow(base: Image.Image, box: tuple[int, int, int, int], radius: int, color: tuple[int, int, int], blur: int = 18) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, outline=color + (190,), width=5)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, min_size: int = 44) -> ImageFont.ImageFont:
    size = start_size
    while size >= min_size:
        f = font(size)
        bbox = draw.textbbox((0, 0), text, font=f, stroke_width=max(2, size // 22))
        if bbox[2] - bbox[0] <= max_width:
            return f
        size -= 4
    return font(min_size)


def paste_face(base: Image.Image, face_path: Path | None, allow_placeholder: bool) -> None:
    if face_path:
        src = ImageOps.exif_transpose(Image.open(face_path)).convert("RGB")
        src_w, src_h = src.size

        # Crop the center-top portrait area, keeping head and torso visible.
        crop_w = min(src_w, int(src_h * 0.72))
        left = max(0, (src_w - crop_w) // 2)
        top = 0
        crop = src.crop((left, top, left + crop_w, src_h))

        target = (420, 620)
        crop_ratio = crop.width / crop.height
        target_ratio = target[0] / target[1]
        if crop_ratio > target_ratio:
            new_w = int(crop.height * target_ratio)
            left = (crop.width - new_w) // 2
            crop = crop.crop((left, 0, left + new_w, crop.height))
        else:
            new_h = int(crop.width / target_ratio)
            top = max(0, int((crop.height - new_h) * 0.08))
            crop = crop.crop((0, top, crop.width, top + new_h))

        person = crop.resize(target, Image.Resampling.LANCZOS).convert("RGBA")
        person = ImageEnhance.Contrast(person).enhance(1.08)
        person = ImageEnhance.Color(person).enhance(1.06)

        mask = Image.new("L", target, 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((0, 0, target[0], target[1]), radius=44, fill=255)
        person.putalpha(mask)

        x = W - target[0] - 40
        y = 82
        draw_glow(base, (x - 10, y - 10, x + target[0] + 10, y + target[1] + 10), 50, (255, 112, 40), 24)
        frame = Image.new("RGBA", base.size, (0, 0, 0, 0))
        fd = ImageDraw.Draw(frame)
        fd.rounded_rectangle((x - 8, y - 8, x + target[0] + 8, y + target[1] + 8), radius=52, fill=(255, 112, 40, 255))
        fd.rounded_rectangle((x, y, x + target[0], y + target[1]), radius=44, fill=(0, 0, 0, 255))
        frame.alpha_composite(person, (x, y))
        base.alpha_composite(frame)
        return

    if not allow_placeholder:
        raise SystemExit("A face image is required for final thumbnail rendering. Use --concepts-only or --allow-placeholder for testing.")

    draw = ImageDraw.Draw(base)
    draw.ellipse((910, 95, 1170, 355), fill=(238, 238, 232), outline=(255, 120, 45), width=8)
    draw.rounded_rectangle((850, 320, 1235, 760), radius=80, fill=(28, 34, 36), outline=(0, 235, 215), width=8)
    draw.text((972, 180), "FACE", font=font(46), fill=(20, 20, 20))
    draw.text((936, 238), "PHOTO", font=font(36), fill=(20, 20, 20))


def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, fill: tuple[int, int, int]) -> None:
    rounded_rect(draw, (x, y, x + 166, y + 62), 16, fill + (255,), outline=(255, 255, 255, 80), width=2)
    draw.text((x + 20, y + 16), label, font=font(24), fill=(255, 255, 255))


def draw_base(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, W, H), fill=(8, 12, 14, 255))
    draw.ellipse((-260, -210, 860, 930), fill=(4, 56, 54, 255))
    draw.ellipse((660, -180, 1540, 900), fill=(20, 26, 30, 255))
    draw.ellipse((260, 260, 940, 920), fill=(7, 28, 31, 255))
    for x in range(0, W, 64):
        draw.line((x, 0, x, H), fill=(255, 255, 255, 18), width=1)
    for y in range(0, H, 64):
        draw.line((0, y, W, y), fill=(255, 255, 255, 14), width=1)


def draw_headline(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, max_width: int, primary=(255, 255, 255), accent=(255, 112, 40)) -> None:
    headline = text.upper()
    parts = headline.split()
    if len(parts) >= 3:
        line1 = " ".join(parts[: math.ceil(len(parts) / 2)])
        line2 = " ".join(parts[math.ceil(len(parts) / 2) :])
    else:
        line1, line2 = headline, ""
    f1 = fit_text(draw, line1, max_width, 102)
    stroke = 5
    draw.text((x, y), line1, font=f1, fill=primary, stroke_width=stroke, stroke_fill=(0, 0, 0))
    if line2:
        f2 = fit_text(draw, line2, max_width, 102)
        draw.text((x, y + 94), line2, font=f2, fill=accent, stroke_width=stroke, stroke_fill=(0, 0, 0))


def render_transcript_thumbnail(path: Path, concept: Concept) -> None:
    base = Image.new("RGBA", (W, H), (8, 12, 14, 255))
    draw = ImageDraw.Draw(base)
    draw_base(draw)

    draw_headline(draw, concept.hook, 62, 58, 650)

    terminal = (64, 292, 676, 628)
    draw_glow(base, terminal, 30, (0, 235, 215), 22)
    rounded_rect(draw, terminal, 30, (8, 31, 34, 248), outline=(0, 235, 215, 230), width=4)
    for i, color in enumerate([(255, 92, 92), (255, 192, 76), (64, 204, 108)]):
        draw.ellipse((94 + i * 36, 324, 112 + i * 36, 342), fill=color + (255,))
    draw.text((94, 372), "$ yt-dlp --write-auto-subs", font=font(30), fill=(225, 255, 252))
    draw.text((94, 418), "502 videos found", font=font(34), fill=(0, 235, 215))
    draw.text((94, 468), "clean transcripts exported", font=font(30), fill=(225, 255, 252))
    rounded_rect(draw, (94, 540, 640, 582), 12, (16, 163, 74, 255))
    draw.text((118, 548), "DONE IN UNDER 60 MIN", font=font(24), fill=(255, 255, 255))

    for i, (x, y) in enumerate([(745, 90), (858, 174), (716, 280), (890, 392)]):
        rounded_rect(draw, (x, y, x + 220, y + 130), 22, (250, 250, 250, 255), outline=(255, 112, 40, 255), width=5)
        draw.rectangle((x + 22, y + 22, x + 104, y + 80), fill=(220, 32, 32, 255))
        draw.polygon([(x + 54, y + 38), (x + 54, y + 66), (x + 78, y + 52)], fill=(255, 255, 255))
        draw.line((x + 122, y + 36, x + 195, y + 36), fill=(24, 24, 24), width=8)
        draw.line((x + 122, y + 60, x + 188, y + 60), fill=(96, 96, 96), width=6)
        draw.text((x + 22, y + 94), f"VIDEO {i + 1}", font=font(22), fill=(16, 16, 16))

    doc = (800, 520, 1168, 652)
    draw_glow(base, doc, 24, (255, 112, 40), 18)
    rounded_rect(draw, doc, 24, (247, 250, 246, 255), outline=(255, 112, 40, 255), width=5)
    draw.text((832, 548), "TRANSCRIPTS", font=font(38), fill=(12, 20, 20))
    draw.text((832, 598), "502 FILES", font=font(38), fill=(255, 112, 40))

    draw.line((684, 460, 800, 570), fill=(255, 112, 40), width=10)
    draw.polygon([(800, 570), (770, 562), (790, 540)], fill=(255, 112, 40))

    out = base.convert("RGB")
    out.save(path, quality=95)


def render_mobile_thumbnail(path: Path, concept: Concept) -> None:
    base = Image.new("RGBA", (W, H), (8, 12, 14, 255))
    draw = ImageDraw.Draw(base)
    draw_base(draw)

    draw_headline(draw, concept.hook, 62, 58, 600, accent=(0, 235, 215))

    phone = (720, 72, 1050, 662)
    draw_glow(base, phone, 56, (0, 235, 215), 26)
    rounded_rect(draw, phone, 56, (16, 18, 20, 255), outline=(255, 255, 255, 60), width=3)
    rounded_rect(draw, (746, 106, 1024, 628), 38, (242, 246, 246, 255), outline=(0, 0, 0, 255), width=2)
    draw.text((784, 144), "Codex Mobile", font=font(28), fill=(12, 18, 18))
    rounded_rect(draw, (782, 198, 988, 258), 18, (0, 184, 204, 255))
    draw.text((812, 214), "VOICE PROMPT", font=font(22), fill=(255, 255, 255))
    for y, label in [(304, "Message client"), (378, "Open library"), (452, "Schedule video")]:
        rounded_rect(draw, (782, y, 988, y + 48), 14, (230, 236, 236, 255), outline=(200, 208, 208, 255), width=2)
        draw.text((806, y + 12), label, font=font(19), fill=(22, 28, 28))
    draw.ellipse((875, 548, 929, 602), fill=(255, 112, 40, 255))
    draw.polygon([(894, 564), (894, 586), (914, 575)], fill=(255, 255, 255))

    window = (64, 304, 642, 620)
    draw_glow(base, window, 28, (255, 112, 40), 18)
    rounded_rect(draw, window, 28, (12, 25, 30, 248), outline=(255, 112, 40, 230), width=4)
    for i, color in enumerate([(255, 92, 92), (255, 192, 76), (64, 204, 108)]):
        draw.ellipse((94 + i * 34, 334, 112 + i * 34, 352), fill=color + (255,))
    draw.text((98, 386), "YouTube Studio", font=font(42), fill=(255, 255, 255))
    rounded_rect(draw, (98, 452, 334, 528), 18, (225, 30, 30, 255))
    draw.text((130, 470), "SCHEDULED", font=font(28), fill=(255, 255, 255))
    draw.text((372, 456), "No keyboard.", font=font(34), fill=(0, 235, 215))
    draw.text((372, 502), "No clicking.", font=font(34), fill=(0, 235, 215))

    draw.line((640, 456, 720, 360), fill=(255, 112, 40), width=10)
    draw.polygon([(720, 360), (690, 370), (710, 392)], fill=(255, 112, 40))

    rounded_rect(draw, (1080, 260, 1226, 418), 28, (255, 112, 40, 255))
    draw.text((1114, 292), "2", font=font(76), fill=(255, 255, 255))
    draw.text((1102, 370), "PROMPTS", font=font(24), fill=(255, 255, 255))

    out = base.convert("RGB")
    out.save(path, quality=95)


def render_thumbnail(path: Path, concept: Concept, face_path: Path | None, allow_placeholder: bool, no_face: bool = False) -> None:
    if no_face:
        if "PHONE" in concept.hook.upper() or "MOBILE" in concept.hook.upper():
            render_mobile_thumbnail(path, concept)
        else:
            render_transcript_thumbnail(path, concept)
        return

    base = Image.new("RGBA", (W, H), (8, 12, 14, 255))
    draw = ImageDraw.Draw(base)

    draw_base(draw)

    panel = (52, 102, 704, 608)
    draw_glow(base, panel, 34, (0, 235, 215), 22)
    rounded_rect(draw, panel, 34, (9, 41, 42, 224), outline=(0, 235, 215, 210), width=4)

    headline = concept.hook.upper()
    parts = headline.split()
    if len(parts) >= 3:
        line1 = " ".join(parts[: math.ceil(len(parts) / 2)])
        line2 = " ".join(parts[math.ceil(len(parts) / 2) :])
    else:
        line1, line2 = headline, ""
    f1 = fit_text(draw, line1, 590, 96)
    stroke = 5
    draw.text((86, 142), line1, font=f1, fill=(255, 255, 255), stroke_width=stroke, stroke_fill=(0, 0, 0))
    if line2:
        f2 = fit_text(draw, line2, 590, 96)
        draw.text((86, 232), line2, font=f2, fill=(255, 128, 41), stroke_width=stroke, stroke_fill=(0, 0, 0))

    node_y = 380
    labels = ["YOUTUBE", "CSV", "TRANSCRIPT"]
    xs = [92, 300, 508]
    for i, (x, label) in enumerate(zip(xs, labels)):
        rounded_rect(draw, (x, node_y, x + 152, node_y + 96), 22, (11, 26, 28, 255), outline=(0, 235, 215, 230), width=3)
        draw.text((x + 24, node_y + 34), label, font=font(22), fill=(235, 255, 253))
        if i < 2:
            draw.line((x + 162, node_y + 48, x + 198, node_y + 48), fill=(0, 235, 215), width=5)
            draw.polygon([(x + 198, node_y + 48), (x + 184, node_y + 37), (x + 184, node_y + 59)], fill=(0, 235, 215))

    draw_badge(draw, 84, 520, "AI", (255, 108, 35))
    draw_badge(draw, 272, 520, "TOOLS", (22, 156, 147))
    draw_badge(draw, 496, 520, "DATA", (255, 108, 35))

    paste_face(base, face_path, allow_placeholder)

    draw.rounded_rectangle((810, 38, 1226, 102), radius=18, fill=(255, 112, 40, 255))
    draw.text((842, 55), "DANIEL DANUT AI", font=font(28), fill=(255, 255, 255))

    out = base.convert("RGB")
    out.save(path, quality=95)


def ensure_writable(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}\nPass --overwrite to replace it.")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="Optional review folder/video name.")
    parser.add_argument("--review-root", type=Path, default=REVIEW_ROOT, help="Review root override for testing.")
    parser.add_argument("--scripts-root", type=Path, default=SCRIPTS_ROOT, help="Scripts root override for PDF fallback testing.")
    parser.add_argument("--face", type=Path, help="Path to Daniel face/photo reference for final thumbnail.")
    parser.add_argument("--concepts-only", action="store_true", help="Write concept markdown but skip final PNG rendering.")
    parser.add_argument("--allow-placeholder", action="store_true", help="Render a setup-test thumbnail without a real face photo.")
    parser.add_argument("--no-face", action="store_true", help="Render a no-face thumbnail for cases where no usable portrait is available.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument("--hook", type=str, default=None, help="Override the hook text used for rendering (bypasses auto-generated concepts).")
    parser.add_argument("--list", action="store_true", help="List review folders and exit.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    global REVIEW_ROOT, SCRIPTS_ROOT
    args = parse_args(argv)
    REVIEW_ROOT = args.review_root
    SCRIPTS_ROOT = args.scripts_root
    if args.list:
        for folder in sorted([p for p in REVIEW_ROOT.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True):
            print(folder.name)
        return 0

    folder = find_review_folder(args.target)
    video_name = folder.name
    if not is_project_id(video_name):
        raise SystemExit(f"Review folder must be a canonical project ID folder, got: {video_name}")
    source, text = read_source(folder)
    concepts = generate_concepts(text)
    recommended = max(concepts, key=lambda c: c.total)
    if args.hook:
        recommended = Concept(
            name="Custom Hook",
            hook=args.hook,
            metaphor="",
            face="right",
            background="dark",
            supporting="",
            scores={"curiosity": 9, "clarity": 9, "emotion": 9, "readability": 9},
        )

    concepts_path = folder / f"{video_name}_thumbnail_concepts.md"
    thumb_path = folder / f"{video_name}_thumbnail.png"

    if not args.concepts_only:
        ensure_writable(thumb_path, args.overwrite)

    wrote_concepts = write_concepts_if_needed(concepts_path, video_name, source, concepts, recommended, args.overwrite)
    if wrote_concepts:
        print(f"Wrote concepts: {concepts_path}")
    else:
        print(f"Kept existing concepts: {concepts_path}")

    if args.concepts_only:
        print("Skipped final thumbnail render (--concepts-only).")
        return 0

    if args.face and not args.face.exists():
        raise SystemExit(f"Face image not found: {args.face}")
    render_thumbnail(thumb_path, recommended, args.face, args.allow_placeholder, args.no_face)
    with Image.open(thumb_path) as check:
        if check.size != (W, H):
            raise SystemExit(f"Thumbnail rendered at wrong size: {check.size}")
    print(f"Wrote thumbnail: {thumb_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

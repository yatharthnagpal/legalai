"""
Clause Segmentation Service
Splits raw contract text into individual clauses using
heading detection, numbering patterns, and structural heuristics.
"""

import re
from typing import Optional, Pattern


# ─── Numbering Patterns ─────────────────────────────────

CLAUSE_PATTERNS: list[Pattern[str]] = [
    # "1." or "1.1" or "1.1.1"
    re.compile(r'^(\d+\.(?:\d+\.?)*)\s+', re.MULTILINE),
    # "(a)" or "(i)" or "(1)"
    re.compile(r'^\(([a-z]|[ivxlc]+|\d+)\)\s+', re.MULTILINE),
    # "ARTICLE I" or "Article 1"
    re.compile(r'^(ARTICLE|Article|SECTION|Section|CLAUSE|Clause)\s+[IVXLC\d]+[.:]?\s*', re.MULTILINE),
    # Roman numerals: "I.", "II.", "III."
    re.compile(r'^([IVXLC]+)\.\s+', re.MULTILINE),
    # Letter numbering: "a.", "b.", "A.", "B."
    re.compile(r'^([a-zA-Z])\.\s+', re.MULTILINE),
]

HEADING_KEYWORDS = [
    "WHEREAS", "NOW THEREFORE", "IN WITNESS WHEREOF",
    "DEFINITIONS", "TERM AND TERMINATION", "TERMINATION",
    "PAYMENT", "COMPENSATION", "FEES",
    "CONFIDENTIALITY", "NON-DISCLOSURE",
    "INTELLECTUAL PROPERTY", "IP RIGHTS",
    "INDEMNIFICATION", "INDEMNITY",
    "LIABILITY", "LIMITATION OF LIABILITY",
    "FORCE MAJEURE", "ACT OF GOD",
    "GOVERNING LAW", "JURISDICTION",
    "DISPUTE RESOLUTION", "ARBITRATION",
    "NON-COMPETE", "NON-SOLICITATION",
    "WARRANTY", "WARRANTIES", "REPRESENTATIONS",
    "INSURANCE", "DATA PROTECTION", "PRIVACY",
    "ASSIGNMENT", "NOTICE", "NOTICES",
    "AMENDMENT", "MODIFICATION",
    "SEVERABILITY", "ENTIRE AGREEMENT",
    "RENEWAL", "EXTENSION",
    "PENALTY", "LIQUIDATED DAMAGES",
    "SCOPE OF WORK", "SERVICES",
    "OBLIGATIONS", "RESPONSIBILITIES",
    "RECITALS", "BACKGROUND",
    "SCHEDULE", "ANNEXURE", "APPENDIX",
]


def _is_heading_line(line: str) -> bool:
    """Check if a line is a clause heading or section header."""
    stripped = line.strip()

    # ALL CAPS heading
    if len(stripped) > 3 and stripped == stripped.upper() and not stripped.isdigit():
        return True

    # Known heading keywords
    upper = stripped.upper()
    for keyword in HEADING_KEYWORDS:
        if upper.startswith(keyword):
            return True

    # Numbered heading
    for pattern in CLAUSE_PATTERNS[:3]:
        if pattern.match(stripped):
            return True

    return False


def segment_clauses(text: str) -> list[dict]:
    """
    Segment contract text into individual clauses.
    Returns a list of dicts: {index, heading, text}
    """
    lines = text.split('\n')
    clauses = []
    current_heading = ""
    current_text_lines = []
    clause_index = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_text_lines:
                current_text_lines.append("")
            continue

        if _is_heading_line(stripped):
            # Save previous clause
            if current_text_lines:
                clause_text = "\n".join(current_text_lines).strip()
                if len(clause_text) > 10:
                    clauses.append({
                        "index": clause_index,
                        "heading": current_heading,
                        "text": clause_text,
                    })
                    clause_index += 1

            current_heading = stripped
            current_text_lines = [stripped]
        else:
            current_text_lines.append(stripped)

    # Don't forget the last clause
    if current_text_lines:
        clause_text = "\n".join(current_text_lines).strip()
        if len(clause_text) > 10:
            clauses.append({
                "index": clause_index,
                "heading": current_heading,
                "text": clause_text,
            })

    # If segmentation found very few clauses, fall back to paragraph splitting
    if len(clauses) <= 1 and len(text) > 200:
        clauses = _fallback_paragraph_split(text)

    return clauses


def _fallback_paragraph_split(text: str) -> list[dict]:
    """Fallback: split by double newlines if heading-based segmentation fails."""
    paragraphs = re.split(r'\n\s*\n', text)
    clauses = []
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if len(para) > 20:
            # Try to extract a heading from the first line
            first_line = para.split('\n')[0].strip()
            heading = first_line if len(first_line) < 80 else ""
            clauses.append({
                "index": i,
                "heading": heading,
                "text": para,
            })
    return clauses

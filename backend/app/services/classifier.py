"""
Clause Classification Service
Classifies each clause into a legal category using keyword matching
and pattern-based heuristics. Designed to be swappable with a
LegalBERT model for production use.
"""

import re


# ─── Keyword-Based Classification Rules ──────────────────

CLAUSE_RULES = {
    "Payment": {
        "keywords": [
            "payment", "fee", "fees", "compensation", "remuneration",
            "invoice", "billing", "price", "cost", "charge", "salary",
            "wages", "consideration", "amount payable", "pay",
            "installment", "milestone payment", "advance payment",
            "due date", "net 30", "net 60",
        ],
        "patterns": [
            r"(?:shall|will|agrees?\s+to)\s+pay",
            r"(?:payment|fee|amount)\s+(?:of|shall be)",
            r"(?:INR|Rs\.?|₹)\s*[\d,]+",
            r"\bpayable\b.*\b(?:within|on|before)\b",
        ],
        "weight": 1.0,
    },
    "Termination": {
        "keywords": [
            "termination", "terminate", "expiry", "expiration",
            "cancellation", "cancel", "end of term", "notice period",
            "wind up", "dissolution",
        ],
        "patterns": [
            r"(?:may|shall|can)\s+terminate",
            r"termination\s+(?:of|for|by|upon)",
            r"notice\s+(?:of|period|for)\s+termination",
            r"(?:upon|after)\s+expiry",
        ],
        "weight": 1.0,
    },
    "Liability": {
        "keywords": [
            "liability", "liable", "limitation of liability",
            "cap on liability", "aggregate liability", "damages",
            "consequential damages", "direct damages", "indirect",
            "maximum liability", "no liability",
        ],
        "patterns": [
            r"(?:total|aggregate|maximum)\s+liability",
            r"(?:shall|will)\s+(?:not\s+)?be\s+liable",
            r"limitation\s+of\s+liability",
            r"in\s+no\s+event\s+shall.*liable",
        ],
        "weight": 1.0,
    },
    "Indemnity": {
        "keywords": [
            "indemnif", "indemnity", "indemnification", "hold harmless",
            "defend and indemnify", "indemnified party",
        ],
        "patterns": [
            r"(?:shall|agrees?\s+to)\s+indemnif",
            r"hold\s+harmless",
            r"indemnif(?:y|ied|ication)",
        ],
        "weight": 1.2,
    },
    "Confidentiality": {
        "keywords": [
            "confidential", "confidentiality", "non-disclosure",
            "proprietary", "trade secret", "sensitive information",
            "classified", "restricted information",
        ],
        "patterns": [
            r"confidential\s+information",
            r"(?:shall|will)\s+(?:not\s+)?disclose",
            r"non-disclosure",
            r"maintain\s+(?:the\s+)?confidentiality",
        ],
        "weight": 1.0,
    },
    "Intellectual Property": {
        "keywords": [
            "intellectual property", "ip rights", "copyright",
            "trademark", "patent", "trade mark", "proprietary rights",
            "ownership of ip", "work product", "moral rights",
            "license", "licensing",
        ],
        "patterns": [
            r"intellectual\s+property",
            r"(?:all|any)\s+(?:ip|intellectual\s+property)\s+rights",
            r"(?:copyright|patent|trademark)\s+(?:in|to|of)",
            r"(?:shall|will)\s+(?:own|vest|belong)",
        ],
        "weight": 1.0,
    },
    "Force Majeure": {
        "keywords": [
            "force majeure", "act of god", "unforeseeable",
            "beyond the control", "natural disaster", "pandemic",
            "epidemic", "war", "riot", "civil commotion",
            "government action", "embargo",
        ],
        "patterns": [
            r"force\s+majeure",
            r"act\s+of\s+god",
            r"beyond\s+(?:the\s+)?(?:reasonable\s+)?control",
            r"neither\s+party\s+shall\s+be\s+(?:liable|responsible)",
        ],
        "weight": 1.0,
    },
    "Governing Law": {
        "keywords": [
            "governing law", "applicable law", "governed by",
            "laws of india", "laws of the republic",
            "subject to the laws", "legal framework",
        ],
        "patterns": [
            r"govern(?:ed|ing)\s+(?:by\s+)?(?:the\s+)?law",
            r"(?:laws?|legislation)\s+of\s+(?:india|the\s+republic)",
            r"(?:subject|pursuant)\s+to\s+(?:the\s+)?(?:laws?|jurisdiction)",
        ],
        "weight": 1.0,
    },
    "Dispute Resolution": {
        "keywords": [
            "dispute", "arbitration", "mediation", "resolution",
            "arbitrator", "tribunal", "court", "litigation",
            "settlement", "conciliation",
        ],
        "patterns": [
            r"(?:dispute|disagreement)\s+(?:resolution|shall be)",
            r"(?:shall\s+be\s+)?(?:referred\s+to|resolved\s+(?:by|through))\s+(?:arbitration|mediation)",
            r"(?:courts?\s+(?:of|in|at))",
            r"arbitration\s+(?:act|proceedings|clause)",
        ],
        "weight": 1.0,
    },
    "Non-Compete": {
        "keywords": [
            "non-compete", "non compete", "restrictive covenant",
            "non-solicitation", "non solicitation",
            "restraint of trade", "compete",
        ],
        "patterns": [
            r"non[- ]?compet(?:e|ition)",
            r"non[- ]?solicitation",
            r"(?:shall|will)\s+not\s+(?:directly\s+or\s+indirectly\s+)?(?:engage|compete|solicit)",
            r"restraint\s+of\s+trade",
        ],
        "weight": 1.0,
    },
    "Data Protection": {
        "keywords": [
            "data protection", "personal data", "privacy",
            "gdpr", "data processing", "data controller",
            "data processor", "information technology act",
            "it act", "digital personal data",
        ],
        "patterns": [
            r"(?:personal|sensitive)\s+(?:data|information)",
            r"data\s+protection",
            r"(?:information\s+technology|it)\s+act",
            r"(?:process|processing)\s+(?:of\s+)?(?:personal\s+)?data",
        ],
        "weight": 1.0,
    },
    "Warranty": {
        "keywords": [
            "warranty", "warranties", "representation",
            "represents and warrants", "guarantee",
            "fitness for purpose", "merchantability",
        ],
        "patterns": [
            r"(?:represents?\s+and\s+)?warrants?",
            r"(?:no|without)\s+(?:warranty|warranties)",
            r"(?:as[- ]is|without\s+warranty)",
            r"representation\s+(?:and\s+)?warrant",
        ],
        "weight": 1.0,
    },
    "Renewal": {
        "keywords": [
            "renewal", "renew", "auto-renewal", "automatic renewal",
            "extension", "extend", "continuation",
        ],
        "patterns": [
            r"(?:auto(?:matic)?[- ]?)?renew(?:al|ed)?",
            r"(?:shall|will|may)\s+(?:be\s+)?(?:renewed|extended)",
            r"(?:unless|until)\s+(?:terminated|notice)",
        ],
        "weight": 1.0,
    },
    "Penalty": {
        "keywords": [
            "penalty", "penalties", "liquidated damages",
            "fine", "breach penalty", "late fee",
            "penal clause", "forfeiture",
        ],
        "patterns": [
            r"(?:penalty|penalties)\s+(?:of|for|shall)",
            r"liquidated\s+damages",
            r"(?:late|delay)\s+(?:fee|penalty|charge)",
            r"forfeit(?:ure|ed)?",
        ],
        "weight": 1.0,
    },
    "Notice": {
        "keywords": [
            "notice", "notices", "written notice",
            "notification", "serve notice",
        ],
        "patterns": [
            r"(?:written|prior)\s+notice",
            r"notice\s+(?:shall|must|should)\s+be\s+(?:given|sent|served)",
            r"(?:serve|give|send)\s+(?:a\s+)?notice",
        ],
        "weight": 0.8,
    },
    "Assignment": {
        "keywords": [
            "assignment", "assign", "transfer",
            "assignable", "subcontract", "delegate",
        ],
        "patterns": [
            r"(?:shall\s+)?(?:not\s+)?assign",
            r"(?:assignment|transfer)\s+(?:of|by|to)",
            r"(?:without\s+(?:prior\s+)?(?:written\s+)?consent)",
        ],
        "weight": 0.8,
    },
    "Severability": {
        "keywords": [
            "severability", "severable", "invalid provision",
            "unenforceable", "remaining provisions",
        ],
        "patterns": [
            r"(?:if\s+)?(?:any\s+)?provision.*(?:invalid|unenforceable)",
            r"severab(?:ility|le)",
            r"remaining\s+provisions.*(?:valid|enforceable|effect)",
        ],
        "weight": 0.7,
    },
    "Entire Agreement": {
        "keywords": [
            "entire agreement", "whole agreement",
            "supersedes", "prior agreements",
            "complete agreement", "full agreement",
        ],
        "patterns": [
            r"entire\s+agreement",
            r"(?:supersedes?|replaces?)\s+(?:all\s+)?(?:prior|previous)",
            r"(?:constitutes?\s+the\s+)?(?:entire|complete|whole)\s+agreement",
        ],
        "weight": 0.7,
    },
}


def classify_clause(clause_text: str) -> dict:
    """
    Classify a clause into a legal category.
    Returns: {type, confidence, matched_keywords}
    """
    text_lower = clause_text.lower()
    scores = {}

    for clause_type, rules in CLAUSE_RULES.items():
        score = 0.0
        matched_keywords = []

        # Keyword matching
        for keyword in rules["keywords"]:
            if keyword in text_lower:
                score += 1.0
                matched_keywords.append(keyword)

        # Pattern matching
        for pattern in rules["patterns"]:
            if re.search(pattern, text_lower):
                score += 2.0

        # Apply weight
        score *= rules["weight"]

        if score > 0:
            scores[clause_type] = {
                "score": score,
                "matched_keywords": matched_keywords,
            }

    if not scores:
        return {
            "type": "Other",
            "confidence": 0.3,
            "matched_keywords": [],
        }

    # Pick highest scoring type
    best_type = max(scores, key=lambda k: scores[k]["score"])
    max_score = scores[best_type]["score"]
    confidence = min(0.95, max_score / 10.0)

    return {
        "type": best_type,
        "confidence": round(confidence, 2),
        "matched_keywords": scores[best_type]["matched_keywords"],
    }


def classify_all_clauses(clauses: list[dict]) -> list[dict]:
    """
    Classify a list of segmented clauses.
    Returns each clause dict enriched with classification data.
    """
    results = []
    for clause in clauses:
        classification = classify_clause(clause["text"])
        results.append({
            **clause,
            "clause_type": classification["type"],
            "classification_confidence": classification["confidence"],
            "matched_keywords": classification["matched_keywords"],
        })
    return results

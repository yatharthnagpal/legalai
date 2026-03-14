"""
Obligation & Entity Extraction Service
Extracts parties, obligations, deadlines, and key terms from contracts
using regex patterns and heuristic NER.
"""

import re
from typing import Optional


# ─── Party Extraction Patterns ───────────────────────────

PARTY_PATTERNS = [
    # "between X (Party A) and Y (Party B)"
    re.compile(
        r'between\s+["\']?([A-Z][A-Za-z\s&.,]+?)(?:\s*\(["\']?(?:hereinafter|the)?\s*["\']?(?:first\s+party|party\s+(?:of\s+the\s+)?(?:a|1|first|one)|licensor|lessor|employer|client|company|vendor|seller)["\']?\s*\))',
        re.IGNORECASE
    ),
    re.compile(
        r'(?:and|&)\s+["\']?([A-Z][A-Za-z\s&.,]+?)(?:\s*\(["\']?(?:hereinafter|the)?\s*["\']?(?:second\s+party|party\s+(?:of\s+the\s+)?(?:b|2|second|two)|licensee|lessee|employee|service\s+provider|purchaser|buyer)["\']?\s*\))',
        re.IGNORECASE
    ),
    # "M/s. Company Name" or "Mr./Ms. Person Name"
    re.compile(r'(?:M/s\.?|Mr\.?|Ms\.?|Mrs\.?|Shri|Smt)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*,|\s+(?:having|with|residing|located))', re.IGNORECASE),
]

OBLIGATION_PATTERNS = [
    # "X shall/will/must/agrees to [verb]"
    re.compile(r'((?:party\s+[ab]|the\s+(?:company|client|vendor|employer|employee|licensor|licensee|service\s+provider|contractor|consultant))\s+(?:shall|will|must|agrees?\s+to|undertakes?\s+to|is\s+obligated\s+to)\s+.+?)(?:\.|;|$)', re.IGNORECASE),
    # General obligation
    re.compile(r'((?:shall|will|must)\s+(?:be\s+)?(?:responsible|liable|obligated|required)\s+(?:for|to)\s+.+?)(?:\.|;|$)', re.IGNORECASE),
    # "It is the duty/responsibility of X to"
    re.compile(r'(?:duty|responsibility|obligation)\s+of\s+(.+?)\s+to\s+(.+?)(?:\.|;|$)', re.IGNORECASE),
]

DEADLINE_PATTERNS = [
    # "within X days/months/years"
    re.compile(r'within\s+(\d+)\s+(days?|weeks?|months?|years?)', re.IGNORECASE),
    # "before/by [date]"
    re.compile(r'(?:before|by|on\s+or\s+before|no\s+later\s+than)\s+(\d{1,2}[\s/.-]\w+[\s/.-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', re.IGNORECASE),
    # "on the [date]"
    re.compile(r'(?:on|effective\s+from)\s+(\d{1,2}[\s/.-]\w+[\s/.-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', re.IGNORECASE),
]

DATE_PATTERNS = [
    re.compile(r'(?:dated?|effective\s+(?:date|from)|commence(?:s|ment)?(?:\s+date)?)\s*[:\-]?\s*(\d{1,2}[\s/.-]\w+[\s/.-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})', re.IGNORECASE),
    re.compile(r'(\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4})', re.IGNORECASE),
    re.compile(r'(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})'),
]

VALUE_PATTERNS = [
    re.compile(r'(?:INR|Rs\.?|₹)\s*([,\d]+(?:\.\d{2})?)\s*(?:(?:lakh|lac|crore|million|billion|thousand)s?)?', re.IGNORECASE),
    re.compile(r'(?:total\s+(?:value|amount|consideration|price|cost|fee))\s*(?:of|:)?\s*(?:INR|Rs\.?|₹)?\s*([,\d]+(?:\.\d{2})?)', re.IGNORECASE),
]


def extract_parties(text: str) -> list[dict]:
    """Extract party names and roles from contract text."""
    parties = []
    seen_names = set()

    for pattern in PARTY_PATTERNS:
        for match in pattern.finditer(text):
            name = match.group(1).strip().rstrip(',.')
            if name and len(name) > 2 and name.lower() not in seen_names:
                seen_names.add(name.lower())
                parties.append({
                    "name": name,
                    "role": _guess_party_role(text, name),
                    "aliases": [],
                })

    # If no parties found via patterns, try a simpler approach
    if not parties:
        # Look for "between [Name] and [Name]"
        between_match = re.search(
            r'between\s+(.+?)\s+(?:and|&)\s+(.+?)(?:\s*\.|\s+(?:for|regarding|in respect))',
            text[:2000], re.IGNORECASE
        )
        if between_match:
            for i, group in enumerate([between_match.group(1), between_match.group(2)]):
                name = group.strip().rstrip(',.')
                name = re.sub(r'\(.*?\)', '', name).strip()
                if name and len(name) > 2:
                    parties.append({
                        "name": name[:100],
                        "role": "Party A" if i == 0 else "Party B",
                        "aliases": [],
                    })

    return parties


def _guess_party_role(text: str, name: str) -> str:
    """Guess the role of a party based on context."""
    text_lower = text.lower()
    name_lower = name.lower()

    role_keywords = {
        "Employer": ["employer", "company"],
        "Employee": ["employee", "worker"],
        "Client": ["client", "customer", "buyer", "purchaser"],
        "Service Provider": ["service provider", "vendor", "contractor", "consultant", "seller"],
        "Licensor": ["licensor", "owner"],
        "Licensee": ["licensee"],
        "Lessor": ["lessor", "landlord", "owner"],
        "Lessee": ["lessee", "tenant"],
    }

    # Check if the party name is near any role keyword
    name_pos = text_lower.find(name_lower)
    if name_pos >= 0:
        context = text_lower[max(0, name_pos - 100):name_pos + len(name_lower) + 100]
        for role, keywords in role_keywords.items():
            for keyword in keywords:
                if keyword in context:
                    return role

    return "Party"


def extract_obligations(clauses: list[dict]) -> list[dict]:
    """Extract obligations from classified clauses."""
    obligations = []

    for clause in clauses:
        text = clause["text"]
        clause_idx = clause["index"]
        clause_type = clause.get("clause_type", "Other")

        for pattern in OBLIGATION_PATTERNS:
            for match in pattern.finditer(text):
                obligation_text = match.group(0).strip()
                if len(obligation_text) > 15:
                    # Try to find associated deadline
                    deadline = None
                    for dp in DEADLINE_PATTERNS:
                        dm = dp.search(text)
                        if dm:
                            deadline = dm.group(0)
                            break

                    # Try to identify the party
                    party = "Unknown"
                    party_match = re.match(
                        r'(party\s+[ab]|the\s+(?:company|client|vendor|employer|employee|service\s+provider|contractor))',
                        obligation_text, re.IGNORECASE
                    )
                    if party_match:
                        party = party_match.group(1).strip()

                    obligations.append({
                        "party": party,
                        "obligation": obligation_text[:300],
                        "deadline": deadline,
                        "clause_index": clause_idx,
                        "clause_type": clause_type,
                    })

    return obligations


def extract_dates(text: str) -> dict:
    """Extract key dates from contract text."""
    dates = {
        "effective_date": None,
        "expiry_date": None,
        "all_dates": [],
    }

    for pattern in DATE_PATTERNS:
        for match in pattern.finditer(text[:3000]):
            date_str = match.group(1) if match.lastindex else match.group(0)
            dates["all_dates"].append(date_str)

    # Try to identify effective date
    eff_match = re.search(
        r'(?:effective\s+(?:date|from)|commence(?:s|ment)?(?:\s+date)?)\s*[:\-]?\s*(\d{1,2}[\s/.-]\w+[\s/.-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})',
        text[:3000], re.IGNORECASE
    )
    if eff_match:
        dates["effective_date"] = eff_match.group(1)

    # Try to identify expiry date
    exp_match = re.search(
        r'(?:expir(?:y|ation|es?)|terminat(?:e|ion|es?)\s+(?:on|date)|end\s+date|valid\s+(?:until|till|through))\s*[:\-]?\s*(\d{1,2}[\s/.-]\w+[\s/.-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})',
        text[:5000], re.IGNORECASE
    )
    if exp_match:
        dates["expiry_date"] = exp_match.group(1)

    return dates


def extract_contract_value(text: str) -> Optional[str]:
    """Extract the contract's monetary value."""
    for pattern in VALUE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0).strip()
    return None


def extract_key_terms(text: str) -> list[str]:
    """Extract key terms defined in the contract."""
    terms = []

    # Look for defined terms: "Term" means...
    defined_pattern = re.compile(r'"([A-Z][A-Za-z\s]+?)"\s+(?:means?|shall\s+mean|refers?\s+to)', re.IGNORECASE)
    for match in defined_pattern.finditer(text):
        term = match.group(1).strip()
        if 2 < len(term) < 50:
            terms.append(term)

    return list(set(terms))

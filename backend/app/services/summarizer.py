"""
Contract Summarization Service
Generates structured, human-readable contract summaries.
Uses extractive summarization (heuristic-based).
Designed to be swappable with BART/T5 for production use.
"""

import re


def generate_summary(
    raw_text: str,
    classified_clauses: list[dict],
    parties: list[dict],
    obligations: list[dict],
    dates: dict,
    contract_value: str | None,
    key_terms: list[str],
    risk_report: dict,
    compliance_report: dict,
) -> dict:
    """
    Generate a comprehensive contract summary.
    """
    # Detect contract type
    contract_type = _detect_contract_type(raw_text, classified_clauses)

    # Build summary text
    summary_parts = []

    # Opening
    party_names = [p["name"] for p in parties]
    if len(party_names) >= 2:
        summary_parts.append(
            f"This is a **{contract_type}** between **{party_names[0]}** and **{party_names[1]}**."
        )
    elif len(party_names) == 1:
        summary_parts.append(f"This is a **{contract_type}** involving **{party_names[0]}**.")
    else:
        summary_parts.append(f"This is a **{contract_type}**.")

    # Dates
    if dates.get("effective_date"):
        summary_parts.append(f"**Effective Date:** {dates['effective_date']}")
    if dates.get("expiry_date"):
        summary_parts.append(f"**Expiry Date:** {dates['expiry_date']}")

    # Value
    if contract_value:
        summary_parts.append(f"**Contract Value:** {contract_value}")

    # Clause composition
    clause_types = {}
    for c in classified_clauses:
        ct = c.get("clause_type", "Other")
        clause_types[ct] = clause_types.get(ct, 0) + 1

    if clause_types:
        top_types = sorted(clause_types.items(), key=lambda x: x[1], reverse=True)[:5]
        types_str = ", ".join([f"{t[0]} ({t[1]})" for t in top_types])
        summary_parts.append(f"**Key Sections:** {types_str}")

    # Risk snapshot
    health = risk_report.get("health_score", 0)
    risk_level = risk_report.get("overall_risk_level", "low")
    if hasattr(risk_level, 'value'):
        risk_level = risk_level.value
    summary_parts.append(
        f"**Contract Health Score:** {health}/100 (Overall Risk: {risk_level.upper()})"
    )

    high_risk = risk_report.get("high_risk_clauses", 0)
    if high_risk > 0:
        summary_parts.append(f"⚠️ **{high_risk} high-risk clause(s)** detected that require review.")

    # Compliance snapshot
    if compliance_report.get("violations", 0) > 0:
        summary_parts.append(
            f"🚨 **{compliance_report['violations']} compliance violation(s)** found against Indian law."
        )
    elif compliance_report.get("warnings", 0) > 0:
        summary_parts.append(
            f"⚠️ **{compliance_report['warnings']} compliance warning(s)** — review recommended."
        )
    else:
        summary_parts.append("✅ No Indian law compliance violations detected.")

    # Key obligations
    if obligations:
        summary_parts.append("\n**Key Obligations:**")
        for i, obl in enumerate(obligations[:5]):
            party = obl.get("party", "Unknown")
            deadline = f" (Deadline: {obl['deadline']})" if obl.get("deadline") else ""
            summary_parts.append(f"  {i+1}. {party}: {obl['obligation'][:150]}{deadline}")

    # Key terms
    if key_terms:
        summary_parts.append(f"\n**Defined Terms:** {', '.join(key_terms[:10])}")

    summary_text = "\n".join(summary_parts)

    return {
        "contract_type": contract_type,
        "parties": parties,
        "effective_date": dates.get("effective_date"),
        "expiry_date": dates.get("expiry_date"),
        "contract_value": contract_value,
        "summary_text": summary_text,
        "key_terms": key_terms,
        "obligations": obligations[:10],
    }


def _detect_contract_type(text: str, clauses: list[dict]) -> str:
    """Detect the type of contract based on content analysis."""
    text_lower = text.lower()

    type_signals = {
        "Non-Disclosure Agreement": [
            "non-disclosure", "nda", "confidentiality agreement",
            "mutual non-disclosure", "confidential information",
        ],
        "Service Agreement": [
            "service agreement", "scope of work", "service level",
            "services agreement", "consulting agreement", "professional services",
        ],
        "Employment Contract": [
            "employment agreement", "employment contract",
            "terms of employment", "probation", "salary",
            "employee", "employer", "designation",
        ],
        "Freelancer Agreement": [
            "freelancer", "freelance", "independent contractor",
            "contractor agreement", "gig", "project-based",
        ],
        "Vendor Agreement": [
            "vendor agreement", "supplier agreement",
            "purchase order", "supply agreement",
        ],
        "Lease Agreement": [
            "lease agreement", "rental agreement", "rent",
            "lessor", "lessee", "tenancy", "premises",
        ],
        "Partnership Deed": [
            "partnership deed", "partnership agreement",
            "partner", "profit sharing", "partnership firm",
        ],
        "Sale Agreement": [
            "sale agreement", "sale deed", "purchase agreement",
            "buyer", "seller", "sale consideration",
        ],
        "License Agreement": [
            "license agreement", "licensing", "licensee",
            "licensor", "grant of license", "software license",
        ],
        "Loan Agreement": [
            "loan agreement", "lending", "borrower",
            "lender", "interest rate", "repayment",
        ],
    }

    scores = {}
    for contract_type, signals in type_signals.items():
        score = 0
        for signal in signals:
            count = text_lower.count(signal)
            score += count
        if score > 0:
            scores[contract_type] = score

    if scores:
        return max(scores, key=scores.get)
    return "General Contract"

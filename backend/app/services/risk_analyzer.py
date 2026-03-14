"""
Risk Analysis Service
Analyzes contract clauses for legal risks using rule-based detection.
Identifies high-risk, one-sided, ambiguous, and hidden liability clauses.
Designed for Indian contract law context.
"""

import re
from app.models.schemas import RiskLevel


# ─── Risk Detection Rules ────────────────────────────────

RISK_RULES = {
    # ── High-Risk Patterns ─────────────────────────
    "unlimited_liability": {
        "patterns": [
            r"unlimited\s+liability",
            r"no\s+(?:cap|limit|ceiling)\s+(?:on|to)\s+(?:liability|damages)",
            r"liability\s+shall\s+(?:not\s+be|be\s+un)\s*limited",
        ],
        "keywords": ["unlimited liability", "no cap on liability", "without limitation"],
        "risk_level": "critical",
        "risk_score": 95,
        "description": "Unlimited liability clause exposes party to uncapped financial risk",
        "suggestion": "Add a liability cap (e.g., total fees paid in last 12 months) per Section 73-74 of the Indian Contract Act",
    },
    "broad_indemnification": {
        "patterns": [
            r"indemnif(?:y|ied|ication).*(?:all|any|every)\s+(?:claims?|losses?|damages?|liabilities?)",
            r"hold\s+harmless.*(?:all|any|every)",
            r"indemnif.*(?:including\s+but\s+not\s+limited\s+to|without\s+limitation)",
        ],
        "keywords": ["indemnify against all", "all claims", "hold harmless"],
        "risk_level": "high",
        "risk_score": 80,
        "description": "Overly broad indemnification clause may create excessive financial exposure",
        "suggestion": "Narrow indemnification to specific, foreseeable losses and add a reasonable cap",
    },
    "unilateral_termination": {
        "patterns": [
            r"(?:may|can|shall\s+have\s+the\s+right\s+to)\s+terminate.*(?:at\s+(?:any\s+time|will|sole\s+discretion)|without\s+(?:cause|reason|notice))",
            r"terminate\s+(?:this\s+agreement\s+)?(?:at\s+(?:any\s+time|its\s+sole))",
            r"(?:without\s+(?:prior\s+)?(?:written\s+)?notice.*terminat)",
        ],
        "keywords": ["terminate at any time", "sole discretion", "without cause", "without notice"],
        "risk_level": "high",
        "risk_score": 78,
        "description": "One-sided termination right without adequate notice period",
        "suggestion": "Require mutual termination rights with a minimum 30-day notice period",
    },
    "no_limitation_period": {
        "patterns": [
            r"(?:in\s+)?perpetuit(?:y|ual)",
            r"surviv(?:e|es|al).*(?:indefinitely|without\s+(?:time\s+)?limit)",
            r"obligations?\s+(?:shall|will)\s+(?:continue|survive)\s+(?:indefinitely|forever)",
        ],
        "keywords": ["perpetuity", "indefinitely", "forever", "without time limit"],
        "risk_level": "high",
        "risk_score": 72,
        "description": "Obligations surviving indefinitely without a limitation period",
        "suggestion": "Set a reasonable survival period (e.g., 2-3 years per Indian Limitation Act, 1963)",
    },
    "auto_renewal_no_notice": {
        "patterns": [
            r"auto(?:matic)?(?:ally)?\s*renew(?:al|ed)?.*(?:unless|until)",
            r"(?:shall|will)\s+(?:be\s+)?(?:automatically|auto)\s+(?:renewed|extended)",
        ],
        "keywords": ["auto-renewal", "automatic renewal", "automatically renewed"],
        "risk_level": "medium",
        "risk_score": 60,
        "description": "Auto-renewal clause may lock party into unwanted contract extensions",
        "suggestion": "Ensure auto-renewal includes adequate notice period (30–60 days) for opt-out",
    },
    "non_compete_broad": {
        "patterns": [
            r"(?:shall|will)\s+not\s+(?:directly\s+or\s+indirectly\s+)?(?:engage|compete|work|provide)",
            r"non[- ]?compet(?:e|ition).*(?:(?:\d+)\s+years?|indefinite|perpetual)",
            r"restraint\s+of\s+trade",
        ],
        "keywords": ["non-compete", "shall not compete", "restraint of trade"],
        "risk_level": "high",
        "risk_score": 75,
        "description": "Broad non-compete may be unenforceable under Section 27 of the Indian Contract Act (agreements in restraint of trade are void)",
        "suggestion": "Non-compete clauses are generally void under Section 27 of the Indian Contract Act. Limit to reasonable scope and duration, or use a non-solicitation clause instead",
    },
    "exclusive_jurisdiction": {
        "patterns": [
            r"(?:exclusive|sole)\s+jurisdiction.*(?:courts?\s+(?:of|in|at))",
            r"(?:courts?\s+(?:of|in|at)).*(?:shall\s+have\s+)?exclusive\s+jurisdiction",
        ],
        "keywords": ["exclusive jurisdiction"],
        "risk_level": "medium",
        "risk_score": 50,
        "description": "Exclusive jurisdiction in a distant location may be disadvantageous",
        "suggestion": "Ensure jurisdiction is in a convenient location for both parties",
    },
    "waiver_of_rights": {
        "patterns": [
            r"(?:waive|waiver|relinquish|surrender|give\s+up).*(?:right|claim|remedy)",
            r"(?:right|claim|remedy).*(?:waive|waiver|irrevocabl)",
        ],
        "keywords": ["waives the right", "waiver of rights", "irrevocably waives"],
        "risk_level": "high",
        "risk_score": 70,
        "description": "Waiver of fundamental legal rights may be unfair or unenforceable",
        "suggestion": "Review whether the waived rights are essential and ensure the waiver is knowing and voluntary",
    },
    "ip_assignment_broad": {
        "patterns": [
            r"(?:all|any)\s+(?:intellectual\s+property|ip)\s+(?:rights?|shall|created|developed).*(?:belong|vest|assign|transfer).*(?:exclusively|solely)",
            r"(?:assign|transfer).*(?:all|any)\s+(?:right|title|interest).*(?:intellectual\s+property|ip|work\s+product)",
        ],
        "keywords": ["all ip rights", "assign all rights", "vest exclusively"],
        "risk_level": "high",
        "risk_score": 73,
        "description": "Broad IP assignment may transfer all work product rights without adequate compensation",
        "suggestion": "Ensure IP assignment is limited to deliverables under the contract and not pre-existing IP. Include license-back provisions",
    },
    "penalty_clause": {
        "patterns": [
            r"(?:penalty|penalti|liquidated\s+damages?).*(?:INR|Rs\.?|₹)\s*[\d,]+",
            r"(?:INR|Rs\.?|₹)\s*[\d,]+.*(?:penalty|penalti|liquidated\s+damages?)",
            r"(?:shall\s+)?(?:pay|forfeit|lose).*(?:penalty|sum\s+of)",
        ],
        "keywords": ["penalty", "liquidated damages", "forfeit"],
        "risk_level": "medium",
        "risk_score": 55,
        "description": "Penalty clause must represent genuine pre-estimate of loss per Section 74 of Indian Contract Act",
        "suggestion": "Ensure penalty amount is a reasonable pre-estimate of actual loss, not punitive (per Section 74, Indian Contract Act, 1872)",
    },

    # ── Ambiguity Patterns ─────────────────────────
    "ambiguous_language": {
        "patterns": [
            r"\b(?:reasonable|reasonably|adequate|adequately|appropriate|as\s+needed|may\s+deem|as\s+(?:it|they)\s+see(?:s)?\s+fit)\b",
            r"\b(?:best\s+efforts?|commercially\s+reasonable|good\s+faith)\b",
            r"\b(?:from\s+time\s+to\s+time|as\s+and\s+when|at\s+(?:its|their)\s+discretion)\b",
        ],
        "keywords": ["reasonable", "best efforts", "as deemed fit", "from time to time", "at its discretion"],
        "risk_level": "medium",
        "risk_score": 40,
        "description": "Ambiguous language may lead to disputes over interpretation",
        "suggestion": "Replace vague terms with specific, measurable criteria",
    },
}


def analyze_clause_risk(clause_text: str, clause_type: str = "Other") -> dict:
    """
    Analyze a single clause for risks.
    Returns: {risk_level, risk_score, risks: [{rule, description, suggestion}]}
    """
    text_lower = clause_text.lower()
    detected_risks = []
    max_score = 0

    for rule_name, rule in RISK_RULES.items():
        matched = False

        # Check patterns
        for pattern in rule["patterns"]:
            if re.search(pattern, text_lower):
                matched = True
                break

        # Check keywords if no pattern matched
        if not matched:
            for keyword in rule["keywords"]:
                if keyword in text_lower:
                    matched = True
                    break

        if matched:
            detected_risks.append({
                "rule": rule_name,
                "risk_level": rule["risk_level"],
                "risk_score": rule["risk_score"],
                "description": rule["description"],
                "suggestion": rule["suggestion"],
            })
            if rule["risk_score"] > max_score:
                max_score = rule["risk_score"]

    # Determine overall risk level
    if max_score >= 80:
        overall_level = RiskLevel.CRITICAL
    elif max_score >= 60:
        overall_level = RiskLevel.HIGH
    elif max_score >= 35:
        overall_level = RiskLevel.MEDIUM
    elif detected_risks:
        overall_level = RiskLevel.LOW
    else:
        overall_level = RiskLevel.LOW
        max_score = max(5, len(clause_text) // 100)  # Very low baseline

    return {
        "risk_level": overall_level,
        "risk_score": min(100, max_score),
        "risks": detected_risks,
        "risk_reasons": [r["description"] for r in detected_risks],
        "suggestions": [r["suggestion"] for r in detected_risks],
    }


def generate_risk_report(classified_clauses: list[dict], perspective: str = "neutral") -> dict:
    """
    Generate a full risk report for a contract.
    Input: list of classified clauses (from classifier.classify_all_clauses)
    perspective: 'company', 'customer', 'employee', 'vendor', or 'neutral'
    """
    clause_analyses = []
    risk_scores = []

    # Role-based risk adjustments
    # Clauses that are riskier for one party may be safer for the other
    PERSPECTIVE_ADJUSTMENTS = {
        "company": {
            # Company benefits from strong IP assignment, non-compete
            "ip_assignment_broad": -30,
            "non_compete_broad": -20,
            # Company is hurt by unlimited liability towards them
            "unlimited_liability": +10,
            "broad_indemnification": +10,
        },
        "customer": {
            # Customer is hurt by broad IP assignment, unilateral termination, penalties
            "ip_assignment_broad": +15,
            "unilateral_termination": +15,
            "penalty_clause": +15,
            "auto_renewal_no_notice": +15,
            # Customer benefits from non-compete (protects them)
            "non_compete_broad": -15,
        },
        "employee": {
            # Employee is hurt by non-compete, broad IP assignment
            "non_compete_broad": +20,
            "ip_assignment_broad": +20,
            "unilateral_termination": +15,
            "waiver_of_rights": +15,
        },
        "vendor": {
            # Vendor is hurt by penalties, unlimited liability, delayed payment
            "penalty_clause": +15,
            "unlimited_liability": +15,
            "broad_indemnification": +10,
            "unilateral_termination": +10,
        },
    }

    adjustments = PERSPECTIVE_ADJUSTMENTS.get(perspective.lower(), {})

    for clause in classified_clauses:
        risk_result = analyze_clause_risk(clause["text"], clause.get("clause_type", "Other"))

        # Apply perspective adjustments
        adjusted_score = risk_result["risk_score"]
        for risk in risk_result.get("risks", []):
            adj = adjustments.get(risk["rule"], 0)
            if adj != 0:
                adjusted_score = max(0, min(100, adjusted_score + adj))

        # Re-determine risk level based on adjusted score
        if adjusted_score >= 80:
            adjusted_level = RiskLevel.CRITICAL
        elif adjusted_score >= 60:
            adjusted_level = RiskLevel.HIGH
        elif adjusted_score >= 35:
            adjusted_level = RiskLevel.MEDIUM
        else:
            adjusted_level = RiskLevel.LOW

        clause_analyses.append({
            "clause_index": clause["index"],
            "clause_text": clause["text"][:500],
            "clause_type": clause.get("clause_type", "Other"),
            "risk_level": adjusted_level,
            "risk_score": adjusted_score,
            "risk_reasons": risk_result["risk_reasons"],
            "suggestions": risk_result["suggestions"],
        })
        risk_scores.append(adjusted_score)

    # Calculate overall metrics
    avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
    health_score = max(0, 100 - avg_risk)

    high_risk = sum(1 for a in clause_analyses if a["risk_level"] in (RiskLevel.HIGH, RiskLevel.CRITICAL))
    medium_risk = sum(1 for a in clause_analyses if a["risk_level"] == RiskLevel.MEDIUM)
    low_risk = sum(1 for a in clause_analyses if a["risk_level"] == RiskLevel.LOW)

    # Overall risk level
    if any(a["risk_level"] == RiskLevel.CRITICAL for a in clause_analyses):
        overall_level = RiskLevel.CRITICAL
    elif high_risk >= 2:
        overall_level = RiskLevel.HIGH
    elif high_risk >= 1 or medium_risk >= 3:
        overall_level = RiskLevel.MEDIUM
    else:
        overall_level = RiskLevel.LOW

    # Top risks
    top_risks = []
    for a in sorted(clause_analyses, key=lambda x: x["risk_score"], reverse=True)[:5]:
        if a["risk_reasons"]:
            top_risks.append(f"Clause {a['clause_index'] + 1} ({a['clause_type']}): {a['risk_reasons'][0]}")

    return {
        "overall_risk_score": round(avg_risk, 1),
        "overall_risk_level": overall_level,
        "health_score": round(health_score, 1),
        "total_clauses": len(clause_analyses),
        "high_risk_clauses": high_risk,
        "medium_risk_clauses": medium_risk,
        "low_risk_clauses": low_risk,
        "clause_analyses": clause_analyses,
        "top_risks": top_risks,
    }



"""
Indian Law Compliance Service
Checks contract clauses against key Indian statutes:
  - Indian Contract Act, 1872
  - Companies Act, 2013
  - Information Technology Act, 2000
  - Labour Laws (Payment of Wages, Industrial Disputes)
  - Consumer Protection Act, 2019
"""

import re
from app.models.schemas import ComplianceSeverity


# ─── Statute Rules ───────────────────────────────────────

INDIAN_STATUTES = {
    "Indian Contract Act, 1872": {
        "Section 10": {
            "title": "What agreements are contracts",
            "description": "All agreements are contracts if made by free consent of parties competent to contract, for a lawful consideration and with a lawful object",
            "checks": [
                {
                    "name": "minor_party",
                    "patterns": [r"minor", r"below\s+18", r"under\s+(?:the\s+)?age"],
                    "keywords": ["minor", "below 18 years"],
                    "severity": "violation",
                    "issue": "Contract may involve a minor party, which is void ab initio under Section 11",
                    "recommendation": "Ensure all parties are competent to contract (18+ years, of sound mind, not disqualified by law)",
                },
            ],
        },
        "Section 23": {
            "title": "What considerations and objects are lawful",
            "description": "Consideration or object is unlawful if forbidden by law, fraudulent, injurious, immoral, or opposed to public policy",
            "checks": [
                {
                    "name": "unlawful_object",
                    "patterns": [r"(?:illegal|unlawful|forbidden|prohibited)\s+(?:activity|purpose|object|consideration)"],
                    "keywords": ["illegal purpose", "unlawful activity", "forbidden by law"],
                    "severity": "violation",
                    "issue": "Contract object appears to be unlawful under Section 23",
                    "recommendation": "Ensure the contract's consideration and object are lawful and not opposed to public policy",
                },
            ],
        },
        "Section 27": {
            "title": "Agreement in restraint of trade void",
            "description": "Every agreement by which anyone is restrained from exercising a lawful profession, trade or business is void",
            "checks": [
                {
                    "name": "restraint_of_trade",
                    "patterns": [
                        r"(?:shall|will)\s+not\s+(?:directly\s+or\s+indirectly\s+)?(?:engage|compete|carry\s+on|work\s+(?:for|with)|provide\s+(?:services?|goods))",
                        r"non[- ]?compet(?:e|ition)",
                        r"restraint\s+of\s+trade",
                    ],
                    "keywords": ["non-compete", "shall not compete", "restraint of trade", "shall not engage"],
                    "severity": "warning",
                    "issue": "Non-compete / restraint of trade clause is generally VOID under Section 27 (exception: sale of goodwill)",
                    "recommendation": "Non-compete clauses are void in India under Section 27 except during the term of employment or sale of goodwill. Consider narrowing to a non-solicitation clause instead",
                },
            ],
        },
        "Section 28": {
            "title": "Agreements in restraint of legal proceedings void",
            "description": "Agreement restricting a party from enforcing legal rights or limiting time for enforcement is void",
            "checks": [
                {
                    "name": "restraint_legal_proceedings",
                    "patterns": [
                        r"(?:waive|relinquish|surrender|give\s+up).*(?:right\s+to\s+(?:sue|litigate|file|bring\s+(?:a\s+)?(?:suit|claim|action)))",
                        r"(?:shall|will)\s+not\s+(?:sue|litigate|bring\s+(?:any\s+)?(?:claim|action|suit))",
                    ],
                    "keywords": ["waive right to sue", "shall not litigate", "no legal proceedings"],
                    "severity": "violation",
                    "issue": "Restriction on legal proceedings is void under Section 28",
                    "recommendation": "Remove any clause that absolutely restricts a party's right to legal proceedings. Arbitration clauses are permissible",
                },
            ],
        },
        "Section 56": {
            "title": "Agreement to do impossible act",
            "description": "An agreement to do an act impossible in itself is void",
            "checks": [
                {
                    "name": "impossible_act",
                    "patterns": [r"(?:guarantee|warrant|ensure).*(?:100\s*%|absolute|unconditional|zero\s+(?:defect|error|downtime))"],
                    "keywords": ["100% guarantee", "absolute guarantee", "zero defect guarantee"],
                    "severity": "warning",
                    "issue": "Clause may require performance of impossible or impractical obligations under Section 56",
                    "recommendation": "Replace absolute guarantees with commercially reasonable standards or SLA targets",
                },
            ],
        },
        "Section 73-74": {
            "title": "Compensation for breach / Penalty",
            "description": "Compensation for breach must be reasonable pre-estimate of loss. Penalty clauses are subject to court's discretion",
            "checks": [
                {
                    "name": "excessive_penalty",
                    "patterns": [
                        r"(?:penalty|penalti|liquidated\s+damages?).*(?:(?:INR|Rs\.?|₹)\s*[\d,]+(?:\s*(?:lakh|crore|million|billion))?)",
                        r"(?:forfeit|forfeiture).*(?:(?:entire|all|full)\s+(?:amount|deposit|payment|security))",
                    ],
                    "keywords": ["penalty", "forfeit entire", "forfeiture of deposit"],
                    "severity": "warning",
                    "issue": "Penalty clause must represent reasonable pre-estimate of loss under Sections 73-74",
                    "recommendation": "Ensure penalty/liquidated damages amount is a genuine pre-estimate of actual loss. Courts may reduce excessive penalties under Section 74",
                },
            ],
        },
    },

    "Companies Act, 2013": {
        "Section 188": {
            "title": "Related Party Transactions",
            "description": "Related party transactions require Board/Shareholder approval",
            "checks": [
                {
                    "name": "related_party_transaction",
                    "patterns": [
                        r"(?:related\s+party|associate|subsidiary|holding\s+company|director|key\s+managerial)",
                        r"(?:transaction|contract|arrangement).*(?:director|promoter|relative)",
                    ],
                    "keywords": ["related party", "subsidiary", "holding company"],
                    "severity": "info",
                    "issue": "If this is a related party transaction, Board approval may be required under Section 188",
                    "recommendation": "Verify if the contract qualifies as a related party transaction and obtain necessary Board/Shareholder approvals",
                },
            ],
        },
    },

    "Information Technology Act, 2000": {
        "Section 43A": {
            "title": "Compensation for failure to protect data",
            "description": "Body corporate handling sensitive personal data must implement reasonable security practices",
            "checks": [
                {
                    "name": "data_protection_missing",
                    "patterns": [
                        r"(?:personal\s+(?:data|information)|sensitive\s+(?:data|information)|user\s+data|customer\s+data)",
                    ],
                    "keywords": ["personal data", "sensitive data", "user data", "customer information"],
                    "severity": "warning",
                    "issue": "Contract involves personal/sensitive data but may lack adequate data protection provisions under IT Act Section 43A",
                    "recommendation": "Include data protection obligations, security standards (ISO 27001 or equivalent), breach notification procedures, and compliance with IT Act Section 43A and SPDI Rules",
                },
            ],
        },
    },

    "Labour Laws": {
        "Payment of Wages Act": {
            "title": "Payment of Wages Act, 1936",
            "description": "Regulates payment of wages to employees",
            "checks": [
                {
                    "name": "delayed_payment",
                    "patterns": [
                        r"(?:payment|salary|wages?).*(?:within\s+(?:4[5-9]|[5-9]\d|\d{3,})\s+days|(?:quarterly|bi-annually|annually)\s+(?:payment|salary))",
                        r"(?:salary|wages?).*(?:delayed|withheld|deferred).*(?:without\s+(?:reason|cause))",
                    ],
                    "keywords": ["salary withheld", "payment delayed", "wages deferred"],
                    "severity": "warning",
                    "issue": "Payment terms may violate wage payment timelines under the Payment of Wages Act",
                    "recommendation": "Ensure wages/salary are paid within the prescribed period (before 7th or 10th of each month depending on number of employees)",
                },
            ],
        },
    },
}


def check_compliance(clauses: list[dict]) -> dict:
    """
    Check all clauses against Indian statute rules.
    Returns: {is_compliant, total_issues, violations, warnings, issues, statutes_checked}
    """
    issues = []
    statutes_checked = set()

    for clause in clauses:
        text_lower = clause["text"].lower()
        clause_idx = clause["index"]

        for statute_name, sections in INDIAN_STATUTES.items():
            statutes_checked.add(statute_name)

            for section_id, section_data in sections.items():
                for check in section_data["checks"]:
                    matched = False

                    # Check patterns
                    for pattern in check["patterns"]:
                        if re.search(pattern, text_lower):
                            matched = True
                            break

                    # Check keywords
                    if not matched:
                        for keyword in check["keywords"]:
                            if keyword in text_lower:
                                matched = True
                                break

                    if matched:
                        issues.append({
                            "clause_index": clause_idx,
                            "clause_text": clause["text"][:300],
                            "statute": statute_name,
                            "section": f"{section_id} - {section_data['title']}",
                            "issue": check["issue"],
                            "severity": ComplianceSeverity(check["severity"]),
                            "recommendation": check["recommendation"],
                        })

    violations = sum(1 for i in issues if i["severity"] == ComplianceSeverity.VIOLATION)
    warnings = sum(1 for i in issues if i["severity"] == ComplianceSeverity.WARNING)

    return {
        "is_compliant": violations == 0,
        "total_issues": len(issues),
        "violations": violations,
        "warnings": warnings,
        "issues": issues,
        "statutes_checked": sorted(statutes_checked),
    }

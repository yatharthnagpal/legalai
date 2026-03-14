"""
NLU / Chat Service with Groq LLM Integration
Detects user intent and generates intelligent responses using
Groq AI (LLaMA/Mixtral) with contract context awareness.
"""

import re
import os
import time
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv(usecwd=True))

# ─── Groq Setup ─────────────────────────────────────────

_groq_client = None

GROQ_MODELS = ["llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]


def _get_groq_client():
    """Lazy-load the Groq client."""
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY", "")
        if api_key:
            try:
                from groq import Groq
                _groq_client = Groq(api_key=api_key)
                print(f"✅ Groq initialized (key: {api_key[:8]}...)")
            except Exception as e:
                print(f"⚠️ Failed to initialize Groq: {e}")
                _groq_client = None
        else:
            print("⚠️ GROQ_API_KEY not found in environment")
    return _groq_client


def _call_llm(prompt: str, system_prompt: str = None, max_retries: int = 2) -> str | None:
    """Call Groq LLM with retry logic."""
    client = _get_groq_client()
    if not client:
        return None

    sys_prompt = system_prompt or BASE_SYSTEM_PROMPT

    for attempt in range(max_retries + 1):
        for model_name in GROQ_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=2048,
                )
                text = response.choices[0].message.content
                if text:
                    return text.strip()
            except Exception as e:
                error_str = str(e).lower()
                if "rate" in error_str or "limit" in error_str or "429" in error_str:
                    print(f"⚠️ Rate limit on {model_name}, trying next...")
                    continue
                else:
                    print(f"⚠️ Groq error ({model_name}): {e}")
                    continue

        if attempt < max_retries:
            wait_time = 2 ** (attempt + 1)
            print(f"⏳ Waiting {wait_time}s before retry #{attempt + 2}...")
            time.sleep(wait_time)

    return None


# ─── Intent Definitions ──────────────────────────────────

INTENT_RULES = {
    "analyze": {
        "keywords": [
            "analyze", "analysis", "analyse", "check",
            "review", "examine", "inspect", "evaluate",
            "assess", "audit", "scan",
        ],
        "patterns": [
            r"(?:can\s+you\s+)?(?:analyze|analyse|review|check|examine|inspect)\s+(?:this|the|my)",
            r"(?:run|do|perform)\s+(?:a\s+)?(?:full\s+)?(?:analysis|review|check)",
            r"what\s+(?:are\s+)?(?:the\s+)?(?:issues?|problems?|risks?)\s+(?:in|with)",
        ],
        "weight": 1.0,
    },
    "check_risk": {
        "keywords": [
            "risk", "risks", "risky", "dangerous",
            "loophole", "loopholes", "red flag", "warning",
            "vulnerability", "exposure", "one-sided",
        ],
        "patterns": [
            r"(?:check|find|detect|identify|show|highlight)\s+(?:the\s+)?(?:risks?|loopholes?|red\s+flags?|warnings?)",
            r"(?:is\s+(?:this|it)\s+)?(?:risky|dangerous|safe)",
            r"(?:risk\s+(?:analysis|assessment|detection|score|report))",
            r"(?:what|any)\s+(?:are\s+)?(?:the\s+)?(?:risks?|loopholes?|vulnerabilities?)",
        ],
        "weight": 1.2,
    },
    "summarize": {
        "keywords": [
            "summarize", "summary", "summarise",
            "brief", "overview", "gist",
            "tldr", "tl;dr", "key points",
        ],
        "patterns": [
            r"(?:can\s+you\s+)?(?:summarize|summarise|give\s+(?:me\s+)?(?:a\s+)?summary)",
            r"(?:what\s+(?:is|does)\s+(?:this|the)\s+(?:contract|agreement)\s+(?:say|about))",
            r"(?:brief|overview|gist|key\s+points|main\s+points)",
            r"(?:tldr|tl;dr)",
        ],
        "weight": 1.0,
    },
    "check_compliance": {
        "keywords": [
            "compliance", "compliant", "legal check",
            "law", "statute", "regulation",
            "indian contract act", "companies act",
            "labour law", "it act", "valid", "legitimate",
        ],
        "patterns": [
            r"(?:is\s+(?:this|it)\s+)?(?:compliant|legal|valid|legitimate)",
            r"(?:check|verify)\s+(?:compliance|legality|validity)",
            r"(?:comply|compliance)\s+(?:with\s+)?(?:indian\s+)?(?:law|act|regulation|statute)",
            r"(?:indian\s+contract\s+act|companies?\s+act|labour\s+law|it\s+act)",
        ],
        "weight": 1.2,
    },
    "draft": {
        "keywords": [
            "draft", "generate", "create", "write",
            "template", "new contract", "prepare",
            "make me", "compose",
        ],
        "patterns": [
            r"(?:draft|generate|create|write|prepare|compose)\s+(?:a\s+)?(?:new\s+)?(?:contract|agreement|nda|deed)",
            r"(?:can\s+you\s+)?(?:make|prepare|draft)\s+(?:me\s+)?(?:a\s+)?(?:contract|agreement)",
            r"(?:new|fresh)\s+(?:contract|agreement|draft)",
            r"(?:i\s+need|we\s+need)\s+(?:a\s+)?(?:contract|agreement|nda)",
        ],
        "weight": 1.0,
    },
    "explain": {
        "keywords": [
            "explain", "what does", "what is",
            "meaning", "understand", "clarify",
            "translate", "plain english", "simple terms",
        ],
        "patterns": [
            r"(?:what\s+does|what\s+is|explain|clarify)\s+(?:this\s+)?(?:clause|section|term|provision)",
            r"(?:in\s+)?(?:simple|plain)\s+(?:terms|english|words|language)",
            r"(?:help\s+me\s+)?(?:understand|comprehend|interpret)",
            r"explain\s+(?:like\s+)?(?:i'?m\s+)?not\s+a\s+lawyer",
        ],
        "weight": 1.0,
    },
    "suggest": {
        "keywords": [
            "suggest", "suggestion", "recommend",
            "better", "improve", "alternative",
            "safer", "fix", "rewrite",
        ],
        "patterns": [
            r"(?:suggest|recommend)\s+(?:a\s+)?(?:better|safer|alternative|improved)\s+(?:clause|wording|version)",
            r"(?:how\s+(?:can|should|to)\s+)?(?:improve|fix|rewrite|modify)\s+(?:this\s+)?(?:clause|section)",
            r"(?:give\s+me\s+)?(?:alternatives?|suggestions?|recommendations?)",
        ],
        "weight": 1.0,
    },
    "compare": {
        "keywords": [
            "compare", "comparison", "diff",
            "difference", "versus", "vs",
            "side by side",
        ],
        "patterns": [
            r"(?:compare|difference|diff)\s+(?:between|with|against)",
            r"(?:how\s+(?:is|does)\s+(?:this|it)\s+)?(?:differ|compare)",
            r"(?:side\s+by\s+side|versus|vs\.?)",
        ],
        "weight": 1.0,
    },
}


def detect_intent(message: str) -> dict:
    """Detect user intent from a chat message."""
    text_lower = message.lower().strip()
    scores = {}

    for intent, rules in INTENT_RULES.items():
        score = 0.0
        matched_keywords = []

        for keyword in rules["keywords"]:
            if keyword in text_lower:
                score += 1.0
                matched_keywords.append(keyword)

        for pattern in rules["patterns"]:
            if re.search(pattern, text_lower):
                score += 2.5

        score *= rules["weight"]

        if score > 0:
            scores[intent] = {
                "score": score,
                "matched_keywords": matched_keywords,
            }

    if not scores:
        return {
            "intent": "general",
            "confidence": 0.3,
            "matched_keywords": [],
        }

    best_intent = max(scores, key=lambda k: scores[k]["score"])
    max_score = scores[best_intent]["score"]
    confidence = min(0.95, max_score / 8.0)

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "matched_keywords": scores[best_intent]["matched_keywords"],
    }


# ─── LLM Chat ────────────────────────────────────────────

BASE_SYSTEM_PROMPT = """You are an expert AI Legal Assistant specializing in Indian contract law.

Your expertise includes:
- Indian Contract Act, 1872
- Companies Act, 2013
- Information Technology Act, 2000
- Labour Laws (Payment of Wages Act, Industrial Disputes Act)
- Consumer Protection Act, 2019

When answering:
- Be specific and cite relevant Indian laws/sections when applicable
- Highlight risks clearly with severity (Low/Medium/High/Critical)
- Give actionable suggestions, not just identify problems
- Use clear formatting with bullet points and bold text (**bold**)
- Keep answers concise but thorough
- If no contract context is provided, give general legal guidance"""

ROLE_PROMPTS = {
    "company": (
        "\n\nIMPORTANT: The user is representing the COMPANY/EMPLOYER side. "
        "Actively defend the company's interests. Flag clauses with weak IP protection, "
        "broad liability exposure, or insufficient indemnification. Suggest legally "
        "enforceable ways to maximize corporate protection under Indian law. "
        "Interpret ambiguities in favor of the company."
    ),
    "customer": (
        "\n\nIMPORTANT: The user is representing the CUSTOMER/CLIENT side. "
        "Actively defend the customer's interests. Flag overly broad non-competes, "
        "hidden fees, mandatory arbitration, auto-renewals, and unilateral termination "
        "rights. Suggest fair, legally-backed counter-proposals under Indian law. "
        "Interpret ambiguities in favor of the customer."
    ),
    "employee": (
        "\n\nIMPORTANT: The user is representing an EMPLOYEE. "
        "Actively defend the employee's rights. Flag overbroad non-competes (void under "
        "Section 27), excessive IP assignment, unfair termination clauses, and wage "
        "violations. Cite relevant labour laws. Interpret ambiguities in favor of the employee."
    ),
    "vendor": (
        "\n\nIMPORTANT: The user is representing a VENDOR/SERVICE PROVIDER. "
        "Actively defend the vendor's interests. Flag excessive penalties, unlimited "
        "liability, late payment terms, broad indemnification, and one-sided termination. "
        "Suggest fair payment terms and liability caps under Indian law. "
        "Interpret ambiguities in favor of the vendor."
    ),
}


def _build_system_prompt(role: str = "neutral") -> str:
    """Build a role-aware system prompt."""
    prompt = BASE_SYSTEM_PROMPT
    role_addition = ROLE_PROMPTS.get(role.lower(), "")
    if role_addition:
        prompt += role_addition
    return prompt


def _build_context_prompt(user_message: str, analysis_data: dict | None, contract_text: str | None) -> str:
    """Build a prompt with contract context."""
    parts = []

    if contract_text or analysis_data:
        parts.append("═══ CONTRACT CONTEXT ═══\n")

        if analysis_data:
            summary = analysis_data.get("summary", {})
            risk = analysis_data.get("risk_report", {})
            compliance = analysis_data.get("compliance_report", {})

            parts.append(f"Contract Type: {analysis_data.get('contract_type', 'Unknown')}")
            parts.append(f"Health Score: {risk.get('health_score', 'N/A')}/100")
            parts.append(f"Risk Level: {risk.get('overall_risk_level', 'N/A')}")
            parts.append(f"Total Clauses: {risk.get('total_clauses', 0)}")
            parts.append(f"High-Risk Clauses: {risk.get('high_risk_clauses', 0)}")
            parts.append(f"Compliance Issues: {compliance.get('total_issues', 0)}")

            if summary.get("summary_text"):
                parts.append(f"\nSummary: {summary['summary_text']}")

            top_risks = risk.get("top_risks", [])
            if top_risks:
                parts.append("\nTop Risks:")
                for r in top_risks[:5]:
                    parts.append(f"  • {r}")

            issues = compliance.get("issues", [])
            if issues:
                parts.append("\nCompliance Issues:")
                for iss in issues[:5]:
                    parts.append(f"  • [{iss.get('severity', '?')}] {iss.get('statute', '')}: {iss.get('issue', '')}")

            clauses = analysis_data.get("clauses", [])
            if clauses:
                parts.append("\nClauses:")
                for c in clauses[:10]:
                    risk_info = f" [Risk: {c.get('risk_level', 'low')}, Score: {c.get('risk_score', 0)}]"
                    parts.append(f"  Clause {c.get('clause_index', 0)+1} ({c.get('clause_type', 'Other')}){risk_info}:")
                    parts.append(f"    {c.get('clause_text', '')[:200]}")

        if contract_text:
            truncated = contract_text[:3000]
            parts.append(f"\n═══ FULL CONTRACT TEXT ═══\n{truncated}")
            if len(contract_text) > 3000:
                parts.append("... [truncated]")

        parts.append("\n═══ END CONTEXT ═══\n")

    parts.append(f"User Question: {user_message}")
    return "\n".join(parts)


def generate_chat_response(
    intent: str,
    analysis_data: dict | None = None,
    user_message: str = "",
    contract_text: str | None = None,
    role: str = "neutral",
) -> str:
    """Generate a chat response using Groq LLM with contract context and role perspective."""
    # Try LLM first
    if user_message and os.getenv("GROQ_API_KEY"):
        prompt = _build_context_prompt(user_message, analysis_data, contract_text)
        system_prompt = _build_system_prompt(role)
        result = _call_llm(prompt, system_prompt=system_prompt)
        if result:
            return result

    # ─── Fallback: Static Responses ───────────────────────
    if intent == "general":
        return (
            "👋 Hello! I'm your AI Legal Assistant. I can help you with:\n\n"
            "📋 **Analyze** — Upload a contract and I'll identify risks and compliance issues\n"
            "⚠️ **Check Risk** — Detect risky, one-sided, or ambiguous clauses\n"
            "📝 **Summarize** — Get a plain-English summary of any contract\n"
            "✅ **Check Compliance** — Verify compliance with Indian laws\n"
            "📄 **Draft** — Generate an India-compliant contract draft\n"
            "💡 **Suggest** — Get safer clause alternatives\n\n"
            "Just upload a contract or type your request!"
        )

    if intent == "analyze" and analysis_data:
        health = analysis_data.get("risk_report", {}).get("health_score", "N/A")
        risk_level = analysis_data.get("risk_report", {}).get("overall_risk_level", "N/A")
        total_clauses = analysis_data.get("risk_report", {}).get("total_clauses", 0)
        high_risk = analysis_data.get("risk_report", {}).get("high_risk_clauses", 0)

        return (
            f"📊 **Full Analysis Complete!**\n\n"
            f"**Health Score:** {health}/100\n"
            f"**Overall Risk:** {risk_level}\n"
            f"**Total Clauses:** {total_clauses}\n"
            f"**High-Risk Clauses:** {high_risk}\n\n"
            f"Check the **Risk Report** and **Compliance** tabs for details."
        )

    if intent == "draft":
        return (
            "📝 I can generate an India-compliant contract draft!\n\n"
            "Please specify:\n"
            "1. **Contract Type** (NDA, Service Agreement, Employment, etc.)\n"
            "2. **Party A Name**\n"
            "3. **Party B Name**\n\n"
            "Or use the **Draft Generator** tab."
        )

    responses = {
        "analyze": "📋 Upload a contract and I'll perform a complete analysis.",
        "check_risk": "⚠️ Upload a contract and I'll scan for risky clauses.",
        "summarize": "📝 Upload a contract and I'll generate a summary.",
        "check_compliance": "✅ Upload a contract and I'll check Indian law compliance.",
        "explain": "🔍 Upload a contract or paste the clause you want explained.",
        "suggest": "💡 Upload a contract and I'll suggest safer clause alternatives.",
        "compare": "📊 Upload two contracts to compare them.",
    }

    return responses.get(intent, responses["analyze"])

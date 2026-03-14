"""
API Routes for the AI Legal Assistant.
Handles file uploads, contract analysis, chat, and draft generation.
All routes are protected with JWT authentication and data is persisted to the database.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Contract, Analysis, ChatSession, ChatMessage, User
from app.models.schemas import (
    ChatRequest, ChatResponse, DraftRequest, DraftResponse,
    FullAnalysisResponse, RiskReport, ComplianceReport,
    ClauseAnalysis, RiskLevel, ComplianceSeverity,
    ContractSummary, PartyInfo, ObligationItem,
    ContractListItem, ChatSessionItem, ChatMessageItem,
)
from app.services.parser import extract_text, clean_text
from app.services.segmenter import segment_clauses
from app.services.classifier import classify_all_clauses
from app.services.risk_analyzer import generate_risk_report
from app.services.compliance import check_compliance
from app.services.extractor import (
    extract_parties, extract_obligations,
    extract_dates, extract_contract_value, extract_key_terms,
)
from app.services.summarizer import generate_summary
from app.services.nlu import detect_intent, generate_chat_response
from app.services.drafter import generate_draft
from app.services.auth import get_current_user


router = APIRouter()


# ─── Helper: Build analysis response ────────────────────

def _build_analysis_response(
    contract_id: str,
    filename: str,
    raw_text: str,
    role: str = "neutral",
) -> dict:
    """Run the full analysis pipeline and return the response dict."""
    # 1. Segment into clauses
    clauses = segment_clauses(raw_text)

    # 2. Classify clauses
    classified_clauses = classify_all_clauses(clauses)

    # 3. Risk analysis (with role perspective)
    risk_report_data = generate_risk_report(classified_clauses, perspective=role)

    # 4. Compliance check
    compliance_data = check_compliance(classified_clauses)

    # 5. Extract entities
    parties = extract_parties(raw_text)
    obligations = extract_obligations(classified_clauses)
    dates = extract_dates(raw_text)
    contract_value = extract_contract_value(raw_text)
    key_terms = extract_key_terms(raw_text)

    # 6. Generate summary
    summary_data = generate_summary(
        raw_text, classified_clauses, parties,
        obligations, dates, contract_value, key_terms,
        risk_report_data, compliance_data,
    )

    # Build clause analyses
    clause_analyses = [
        ClauseAnalysis(
            clause_index=ca["clause_index"],
            clause_text=ca["clause_text"],
            clause_type=ca["clause_type"],
            risk_level=ca["risk_level"],
            risk_score=ca["risk_score"],
            risk_reasons=ca["risk_reasons"],
            suggestions=ca["suggestions"],
        )
        for ca in risk_report_data["clause_analyses"]
    ]

    # Build compliance issues
    compliance_issues = [
        {
            "clause_index": issue["clause_index"],
            "clause_text": issue["clause_text"],
            "statute": issue["statute"],
            "section": issue["section"],
            "issue": issue["issue"],
            "severity": issue["severity"],
            "recommendation": issue["recommendation"],
        }
        for issue in compliance_data["issues"]
    ]

    # Build party infos
    party_infos = [
        PartyInfo(name=p["name"], role=p["role"], aliases=p.get("aliases", []))
        for p in parties
    ]

    # Build obligation items
    obligation_items = [
        ObligationItem(
            party=o["party"],
            obligation=o["obligation"],
            deadline=o.get("deadline"),
            clause_index=o["clause_index"],
            clause_type=o["clause_type"],
        )
        for o in obligations[:20]
    ]

    risk_report = RiskReport(
        overall_risk_score=risk_report_data["overall_risk_score"],
        overall_risk_level=risk_report_data["overall_risk_level"],
        health_score=risk_report_data["health_score"],
        total_clauses=risk_report_data["total_clauses"],
        high_risk_clauses=risk_report_data["high_risk_clauses"],
        medium_risk_clauses=risk_report_data["medium_risk_clauses"],
        low_risk_clauses=risk_report_data["low_risk_clauses"],
        clause_analyses=clause_analyses,
        top_risks=risk_report_data["top_risks"],
    )

    compliance_report = ComplianceReport(
        is_compliant=compliance_data["is_compliant"],
        total_issues=compliance_data["total_issues"],
        violations=compliance_data["violations"],
        warnings=compliance_data["warnings"],
        issues=compliance_issues,
        statutes_checked=compliance_data["statutes_checked"],
    )

    summary = ContractSummary(
        contract_type=summary_data["contract_type"],
        parties=party_infos,
        effective_date=summary_data.get("effective_date"),
        expiry_date=summary_data.get("expiry_date"),
        contract_value=summary_data.get("contract_value"),
        summary_text=summary_data["summary_text"],
        key_terms=summary_data.get("key_terms", []),
        obligations=obligation_items,
    )

    response = FullAnalysisResponse(
        contract_id=contract_id,
        filename=filename,
        contract_type=summary_data["contract_type"],
        summary=summary,
        risk_report=risk_report,
        compliance_report=compliance_report,
        clauses=clause_analyses,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return response


def _validate_file(file: UploadFile) -> str:
    """Validate file type and return extension."""
    allowed_extensions = {"pdf", "docx", "doc", "txt", "png", "jpg", "jpeg", "tiff", "bmp"}
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Allowed: {', '.join(allowed_extensions)}"
        )
    return ext


# ─── Contract Upload ────────────────────────────────────

@router.post("/upload", response_model=FullAnalysisResponse)
async def upload_contract(
    file: UploadFile = File(...),
    role: str = Form(default="neutral"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a contract file and get a full analysis. Results are saved to DB."""
    _validate_file(file)

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    try:
        # Extract and clean text
        raw_text = extract_text(file_bytes, file.filename)
        raw_text = clean_text(raw_text)

        if len(raw_text.strip()) < 20:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from the document")

        contract_uid = str(uuid.uuid4())

        # Run analysis pipeline
        response = _build_analysis_response(contract_uid, file.filename, raw_text, role)

        # Save to database
        db_contract = Contract(
            contract_uid=contract_uid,
            user_id=current_user.id,
            filename=file.filename,
            raw_text=raw_text,
            contract_type=response.contract_type,
            role_perspective=role,
        )
        db.add(db_contract)
        db.flush()  # Get the contract ID

        db_analysis = Analysis(
            contract_id=db_contract.id,
            analysis_json=json.dumps(response.model_dump(), default=str),
        )
        db.add(db_analysis)
        db.commit()

        return response

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ─── Chat ───────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Chat with the AI legal assistant. Messages are saved to DB."""
    intent_result = detect_intent(request.message)
    intent = intent_result["intent"]

    analysis_data = None
    contract_text = None
    role = "neutral"
    db_contract = None

    if request.contract_id:
        db_contract = db.query(Contract).filter(
            Contract.contract_uid == request.contract_id,
            Contract.user_id == current_user.id,
        ).first()

        if db_contract:
            role = db_contract.role_perspective or "neutral"
            contract_text = db_contract.raw_text

            if db_contract.analysis:
                try:
                    analysis_data = json.loads(db_contract.analysis.analysis_json)
                except json.JSONDecodeError:
                    pass

    # Generate response (with role perspective)
    response_text = generate_chat_response(
        intent=intent,
        analysis_data=analysis_data,
        user_message=request.message,
        contract_text=contract_text,
        role=role,
    )

    # Save messages to DB
    # Find or create chat session for this contract
    session = None
    if db_contract:
        session = db.query(ChatSession).filter(
            ChatSession.contract_id == db_contract.id,
            ChatSession.user_id == current_user.id,
        ).first()

    if not session:
        session = ChatSession(
            session_uid=str(uuid.uuid4()),
            contract_id=db_contract.id if db_contract else None,
            user_id=current_user.id,
            title=request.message[:100],
        )
        db.add(session)
        db.flush()

    # Save user message
    db.add(ChatMessage(
        session_id=session.id,
        role="user",
        content=request.message,
    ))
    # Save assistant response
    db.add(ChatMessage(
        session_id=session.id,
        role="assistant",
        content=response_text,
    ))
    db.commit()

    return ChatResponse(
        response=response_text,
        intent=intent,
        data={"confidence": intent_result["confidence"]},
    )


# ─── Chat Upload ────────────────────────────────────────

@router.post("/chat-upload")
async def chat_upload(
    file: UploadFile = File(...),
    message: Optional[str] = Form(default="Analyze this contract"),
    role: str = Form(default="neutral"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a contract within the chat context."""
    _validate_file(file)

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    try:
        raw_text = extract_text(file_bytes, file.filename)
        raw_text = clean_text(raw_text)

        if len(raw_text.strip()) < 20:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from the document")

        contract_uid = str(uuid.uuid4())

        # Run analysis
        analysis_response = _build_analysis_response(contract_uid, file.filename, raw_text, role)

        # Save to DB
        db_contract = Contract(
            contract_uid=contract_uid,
            user_id=current_user.id,
            filename=file.filename,
            raw_text=raw_text,
            contract_type=analysis_response.contract_type,
            role_perspective=role,
        )
        db.add(db_contract)
        db.flush()

        db_analysis = Analysis(
            contract_id=db_contract.id,
            analysis_json=json.dumps(analysis_response.model_dump(), default=str),
        )
        db.add(db_analysis)

        # Generate chat response
        intent_result = detect_intent(message)
        intent = intent_result["intent"]

        chat_summary = generate_chat_response(
            intent=intent,
            analysis_data=analysis_response.model_dump(),
            user_message=message,
            contract_text=raw_text,
            role=role,
        )

        # Save chat session + messages
        session = ChatSession(
            session_uid=str(uuid.uuid4()),
            contract_id=db_contract.id,
            user_id=current_user.id,
            title=f"Analysis: {file.filename}",
        )
        db.add(session)
        db.flush()

        db.add(ChatMessage(session_id=session.id, role="user", content=message))
        db.add(ChatMessage(session_id=session.id, role="assistant", content=chat_summary))
        db.commit()

        return {
            "response": chat_summary,
            "intent": "analyze",
            "data": {
                "contract_id": contract_uid,
                "analysis": analysis_response.model_dump(),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ─── Draft ──────────────────────────────────────────────

@router.post("/draft", response_model=DraftResponse)
async def create_draft(
    request: DraftRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate an India-compliant contract draft."""
    try:
        result = generate_draft(
            contract_type=request.contract_type.value,
            party_a=request.party_a,
            party_b=request.party_b,
            key_terms=request.key_terms,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions,
        )

        return DraftResponse(
            contract_type=result["contract_type"],
            draft_text=result["draft_text"],
            clauses_included=result["clauses_included"],
            compliance_notes=result["compliance_notes"],
            timestamp=result["timestamp"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Draft generation failed: {str(e)}")


# ─── Get Contract ───────────────────────────────────────

@router.get("/contracts/{contract_id}")
async def get_contract(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a previously analyzed contract (owned by current user)."""
    db_contract = db.query(Contract).filter(
        Contract.contract_uid == contract_id,
        Contract.user_id == current_user.id,
    ).first()

    if not db_contract or not db_contract.analysis:
        raise HTTPException(status_code=404, detail="Contract not found")

    return json.loads(db_contract.analysis.analysis_json)


# ─── List User Contracts ────────────────────────────────

@router.get("/contracts", response_model=list[ContractListItem])
async def list_contracts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all contracts uploaded by the current user."""
    contracts = db.query(Contract).filter(
        Contract.user_id == current_user.id,
    ).order_by(Contract.uploaded_at.desc()).all()

    return [
        ContractListItem(
            contract_id=c.contract_uid,
            filename=c.filename,
            contract_type=c.contract_type or "Other",
            uploaded_at=c.uploaded_at.isoformat() if c.uploaded_at else "",
            role_perspective=c.role_perspective or "neutral",
        )
        for c in contracts
    ]


# ─── Chat History ───────────────────────────────────────

@router.get("/chat/{contract_id}/history", response_model=list[ChatMessageItem])
async def get_chat_history(
    contract_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get chat history for a specific contract."""
    db_contract = db.query(Contract).filter(
        Contract.contract_uid == contract_id,
        Contract.user_id == current_user.id,
    ).first()

    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    session = db.query(ChatSession).filter(
        ChatSession.contract_id == db_contract.id,
        ChatSession.user_id == current_user.id,
    ).first()

    if not session:
        return []

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id,
    ).order_by(ChatMessage.created_at).all()

    return [
        ChatMessageItem(
            role=m.role,
            content=m.content,
            timestamp=m.created_at.isoformat() if m.created_at else "",
        )
        for m in messages
    ]


# ─── Chat Sessions ──────────────────────────────────────

@router.get("/sessions", response_model=list[ChatSessionItem])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all chat sessions for the current user."""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
    ).order_by(ChatSession.updated_at.desc()).all()

    results = []
    for s in sessions:
        msg_count = db.query(ChatMessage).filter(ChatMessage.session_id == s.id).count()
        contract_uid = None
        if s.contract:
            contract_uid = s.contract.contract_uid

        results.append(ChatSessionItem(
            session_id=s.session_uid,
            contract_id=contract_uid,
            title=s.title,
            created_at=s.created_at.isoformat() if s.created_at else "",
            message_count=msg_count,
        ))

    return results

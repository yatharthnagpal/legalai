"""
Pydantic schemas for the AI Legal Assistant API.
Defines all request/response models used across the application.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# ─── Enums ───────────────────────────────────────────────

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ClauseType(str, Enum):
    PAYMENT = "Payment"
    TERMINATION = "Termination"
    LIABILITY = "Liability"
    INDEMNITY = "Indemnity"
    CONFIDENTIALITY = "Confidentiality"
    INTELLECTUAL_PROPERTY = "Intellectual Property"
    FORCE_MAJEURE = "Force Majeure"
    GOVERNING_LAW = "Governing Law"
    DISPUTE_RESOLUTION = "Dispute Resolution"
    NON_COMPETE = "Non-Compete"
    DATA_PROTECTION = "Data Protection"
    WARRANTY = "Warranty"
    INSURANCE = "Insurance"
    ASSIGNMENT = "Assignment"
    NOTICE = "Notice"
    AMENDMENT = "Amendment"
    SEVERABILITY = "Severability"
    ENTIRE_AGREEMENT = "Entire Agreement"
    RENEWAL = "Renewal"
    PENALTY = "Penalty"
    OTHER = "Other"


class ContractType(str, Enum):
    NDA = "Non-Disclosure Agreement"
    SERVICE_AGREEMENT = "Service Agreement"
    EMPLOYMENT = "Employment Contract"
    FREELANCER = "Freelancer Agreement"
    VENDOR = "Vendor Agreement"
    LEASE = "Lease Agreement"
    PARTNERSHIP = "Partnership Deed"
    SALE = "Sale Agreement"
    LICENSE = "License Agreement"
    LOAN = "Loan Agreement"
    OTHER = "Other"


class UserIntent(str, Enum):
    ANALYZE = "analyze"
    SUMMARIZE = "summarize"
    DRAFT = "draft"
    CHECK_RISK = "check_risk"
    CHECK_COMPLIANCE = "check_compliance"
    EXPLAIN = "explain"
    SUGGEST = "suggest"
    COMPARE = "compare"
    GENERAL = "general"


class ComplianceSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    VIOLATION = "violation"


# ─── Request Models ──────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message to the assistant")
    contract_id: Optional[str] = Field(None, description="ID of an uploaded contract for context")


class DraftRequest(BaseModel):
    contract_type: ContractType = Field(..., description="Type of contract to generate")
    party_a: str = Field(..., description="Name of Party A")
    party_b: str = Field(..., description="Name of Party B")
    key_terms: Optional[dict] = Field(default_factory=dict, description="Key terms for the contract")
    jurisdiction: str = Field(default="India", description="Legal jurisdiction")
    additional_instructions: Optional[str] = Field(None, description="Any extra instructions")


# ─── Response Models ─────────────────────────────────────

class ClauseAnalysis(BaseModel):
    clause_index: int
    clause_text: str
    clause_type: str
    risk_level: RiskLevel
    risk_score: float = Field(..., ge=0, le=100)
    risk_reasons: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ComplianceIssue(BaseModel):
    clause_index: int
    clause_text: str
    statute: str
    section: str
    issue: str
    severity: ComplianceSeverity
    recommendation: str


class ObligationItem(BaseModel):
    party: str
    obligation: str
    deadline: Optional[str] = None
    clause_index: int
    clause_type: str


class PartyInfo(BaseModel):
    name: str
    role: str
    aliases: list[str] = Field(default_factory=list)


class ContractSummary(BaseModel):
    contract_type: str
    parties: list[PartyInfo]
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    contract_value: Optional[str] = None
    summary_text: str
    key_terms: list[str] = Field(default_factory=list)
    obligations: list[ObligationItem] = Field(default_factory=list)


class RiskReport(BaseModel):
    overall_risk_score: float = Field(..., ge=0, le=100)
    overall_risk_level: RiskLevel
    health_score: float = Field(..., ge=0, le=100)
    total_clauses: int
    high_risk_clauses: int
    medium_risk_clauses: int
    low_risk_clauses: int
    clause_analyses: list[ClauseAnalysis]
    top_risks: list[str] = Field(default_factory=list)


class ComplianceReport(BaseModel):
    is_compliant: bool
    total_issues: int
    violations: int
    warnings: int
    issues: list[ComplianceIssue]
    statutes_checked: list[str]


class FullAnalysisResponse(BaseModel):
    contract_id: str
    filename: str
    contract_type: str
    summary: ContractSummary
    risk_report: RiskReport
    compliance_report: ComplianceReport
    clauses: list[ClauseAnalysis]
    timestamp: str


class DraftResponse(BaseModel):
    contract_type: str
    draft_text: str
    clauses_included: list[str]
    compliance_notes: list[str]
    timestamp: str


class ChatResponse(BaseModel):
    response: str
    intent: str
    data: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    features: list[str]


# ─── Auth Models ─────────────────────────────────────────

class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    full_name: Optional[str] = Field(None, description="User's full name")


class UserLogin(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str = ""


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ContractListItem(BaseModel):
    contract_id: str
    filename: str
    contract_type: str
    uploaded_at: str
    role_perspective: str = "neutral"


class ChatSessionItem(BaseModel):
    session_id: str
    contract_id: Optional[str] = None
    title: str
    created_at: str
    message_count: int = 0


class ChatMessageItem(BaseModel):
    role: str
    content: str
    timestamp: str

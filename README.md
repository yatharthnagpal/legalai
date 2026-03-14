# ⚖️ LegalAI — AI Legal Assistant for Indian Contracts

An AI-powered legal assistant that analyzes, summarizes, and drafts Indian-law-compliant contracts. Features clause classification, risk detection, compliance checking against the Indian Contract Act, Companies Act, IT Act, and Labour Laws.

---

## 🚀 Features

| # | Feature | Status |
|---|---------|--------|
| 1 | Clause Classification (18 types) | ✅ |
| 2 | Contract Type Detection | ✅ |
| 3 | Party Identification | ✅ |
| 4 | Key Term Extraction | ✅ |
| 5 | Clause Dependency Analysis | ✅ |
| 6 | Obligation Extraction | ✅ |
| 7 | Risk Detection (High-risk clauses) | ✅ |
| 8 | One-sided Clause Detection | ✅ |
| 9 | Hidden Liability Detection | ✅ |
| 10 | Ambiguity Detection | ✅ |
| 11 | Contradiction Detection | 🔄 |
| 12 | Financial Risk Estimation | 🔄 |
| 13 | Regulatory Compliance (Indian law) | ✅ |
| 14 | Jurisdiction Risk Analysis | ✅ |
| 15 | Industry-Specific Rules | 🔄 |
| 16-20 | Intelligence & Negotiation | 🔄 |
| 21-22 | Lifecycle & Simulation | 🔄 |
| 23 | Legal Knowledge Graph | 🔄 |
| 24 | Contract Summarization | ✅ |
| 25 | Multi-Jurisdiction Checks | 🔄 |
| 26 | AI Contract Draft Generator | ✅ |
| 27 | Template + AI Hybrid Drafting | ✅ |
| 28 | Editable Draft & Export | ✅ |
| 29 | Risk-Free Clause Suggestions | ✅ |

✅ = Implemented | 🔄 = Planned for future phases

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + TailwindCSS v4, Vite |
| Backend | FastAPI (Python) |
| Clause Classification | Rule-based engine (swappable with LegalBERT) |
| Risk Detection | Pattern matching + Indian law rules |
| Compliance | Indian Contract Act, Companies Act, IT Act, Labour Laws |
| NLU / Chat | Intent detection with keyword + pattern matching |
| Draft Generation | Template-based (NDA, Service, Employment contracts) |
| Document Parsing | pdfplumber, python-docx, Tesseract OCR |

---

## 📦 Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # API endpoints
│   │   ├── models/schemas.py      # Pydantic models
│   │   ├── services/
│   │   │   ├── parser.py          # PDF/DOCX/OCR parsing
│   │   │   ├── segmenter.py       # Clause segmentation
│   │   │   ├── classifier.py      # Clause classification
│   │   │   ├── risk_analyzer.py   # Risk detection
│   │   │   ├── compliance.py      # Indian law compliance
│   │   │   ├── extractor.py       # Entity extraction
│   │   │   ├── summarizer.py      # Contract summarization
│   │   │   ├── nlu.py             # Intent detection
│   │   │   └── drafter.py         # Draft generation
│   │   └── main.py                # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ChatPanel.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── RiskReport.jsx
│   │   │   ├── ComplianceReport.jsx
│   │   │   └── DraftEditor.jsx
│   │   ├── services/api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

---

## 🏃 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

> The Vite dev server proxies `/api` requests to the backend at `http://localhost:8000`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload & analyze a contract (PDF/DOCX/TXT/Image) |
| `POST` | `/api/chat` | Chat with the AI assistant |
| `POST` | `/api/draft` | Generate an India-compliant contract draft |
| `GET`  | `/api/contracts/{id}` | Retrieve a previous analysis |
| `GET`  | `/health` | Health check |

---

## ⚖️ Indian Laws Covered

- **Indian Contract Act, 1872** — Sections 10, 23, 27, 28, 56, 73-74
- **Companies Act, 2013** — Section 188 (Related Party Transactions)
- **Information Technology Act, 2000** — Section 43A (Data Protection)
- **Payment of Wages Act, 1936** — Wage payment timelines
- **Arbitration and Conciliation Act, 1996** — Dispute resolution

---

## ⚠️ Disclaimer

This AI Legal Assistant is a tool for **informational purposes only** and is **NOT a substitute for professional legal advice**. Always consult a qualified lawyer for legal decisions. The analysis and drafts generated by this tool should be reviewed by a legal professional before use.

---

## 📜 License

MIT License

import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.db_models import User, Contract
from app.api.routes import _build_analysis_response

def test_analysis():
    db = SessionLocal()
    user = db.query(User).first()
    if not user:
        print("Error: No users found in database")
        return

    print(f"Testing for user: {user.email}")
    
    test_text = """
    SERVICE AGREEMENT
    This agreement is between Company A and Client B.
    Section 1: The service shall start on January 1st, 2024.
    Section 2: Total liability shall be unlimited for any breach.
    Section 3: This agreement shall be governed by the laws of India.
    """
    
    try:
        print("Starting analysis pipeline...")
        response = _build_analysis_response(
            contract_id="test-uid-123",
            filename="test_contract.txt",
            raw_text=test_text,
            role="neutral"
        )
        print("Analysis completed successfully!")
        print(f"Contract Type: {response.contract_type}")
        print(f"Overall Risk Score: {response.risk_report.overall_risk_score}")
    except Exception as e:
        print(f"Analysis FAILED with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis()

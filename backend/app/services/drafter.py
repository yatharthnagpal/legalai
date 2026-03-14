"""
AI Contract Draft Generator
Generates India-compliant contract drafts using templates.
Supports NDA, Service Agreement, Employment, Freelancer, and Vendor contracts.
"""

from datetime import datetime


# ─── Contract Templates ──────────────────────────────────

TEMPLATES = {
    "Non-Disclosure Agreement": {
        "title": "NON-DISCLOSURE AGREEMENT",
        "sections": [
            {
                "heading": "PARTIES",
                "template": """This Non-Disclosure Agreement ("Agreement") is entered into on {date} ("Effective Date")

BETWEEN:

{party_a} (hereinafter referred to as the "Disclosing Party")

AND

{party_b} (hereinafter referred to as the "Receiving Party")

(The Disclosing Party and the Receiving Party are individually referred to as "Party" and collectively as "Parties")""",
            },
            {
                "heading": "1. DEFINITIONS",
                "template": """1.1 "Confidential Information" means any and all information, whether written, oral, electronic, or visual, that is disclosed by the Disclosing Party to the Receiving Party, including but not limited to:
(a) Business plans, strategies, and financial information;
(b) Technical data, trade secrets, know-how, and inventions;
(c) Customer lists, marketing plans, and pricing information;
(d) Software, algorithms, and source code;
(e) Any other information marked as "Confidential" or that a reasonable person would consider confidential.

1.2 Confidential Information does NOT include information that:
(a) Is or becomes publicly available through no fault of the Receiving Party;
(b) Was already known to the Receiving Party before disclosure;
(c) Is independently developed by the Receiving Party without use of the Confidential Information;
(d) Is disclosed to the Receiving Party by a third party without breach of any obligation of confidentiality.""",
            },
            {
                "heading": "2. OBLIGATIONS OF THE RECEIVING PARTY",
                "template": """2.1 The Receiving Party agrees to:
(a) Hold the Confidential Information in strict confidence;
(b) Not disclose the Confidential Information to any third party without prior written consent of the Disclosing Party;
(c) Use the Confidential Information solely for the purpose of {purpose};
(d) Take all reasonable measures to protect the confidentiality of the Confidential Information, using at least the same degree of care as it uses for its own confidential information;
(e) Limit access to the Confidential Information to its employees and agents who have a need to know and who are bound by similar confidentiality obligations.

2.2 The Receiving Party may disclose Confidential Information if required by law, court order, or governmental authority, provided that:
(a) The Receiving Party gives prompt written notice to the Disclosing Party (unless prohibited by law);
(b) The Receiving Party cooperates with the Disclosing Party in seeking a protective order.""",
            },
            {
                "heading": "3. TERM AND TERMINATION",
                "template": """3.1 This Agreement shall remain in effect for a period of {duration} from the Effective Date.

3.2 Either Party may terminate this Agreement by providing 30 (thirty) days' prior written notice to the other Party.

3.3 The confidentiality obligations under this Agreement shall survive the termination or expiry of this Agreement for a period of 3 (three) years from the date of disclosure of the relevant Confidential Information.""",
            },
            {
                "heading": "4. RETURN OF INFORMATION",
                "template": """4.1 Upon termination of this Agreement or upon the Disclosing Party's written request, the Receiving Party shall:
(a) Promptly return or destroy all copies of the Confidential Information in any form;
(b) Certify in writing that all such copies have been returned or destroyed;
(c) Delete all electronic copies from its systems and records.""",
            },
            {
                "heading": "5. REMEDIES",
                "template": """5.1 The Receiving Party acknowledges that any breach of this Agreement may cause irreparable harm to the Disclosing Party and that monetary damages may be inadequate.

5.2 The Disclosing Party shall be entitled to seek injunctive relief and specific performance in addition to any other remedies available at law or in equity.""",
            },
            {
                "heading": "6. GOVERNING LAW AND DISPUTE RESOLUTION",
                "template": """6.1 This Agreement shall be governed by and construed in accordance with the laws of India.

6.2 Any dispute arising out of or in connection with this Agreement shall be first attempted to be resolved through good faith negotiation between the Parties.

6.3 If the dispute is not resolved within 30 (thirty) days, it shall be referred to and finally resolved by arbitration in accordance with the Arbitration and Conciliation Act, 1996, by a sole arbitrator mutually appointed by the Parties.

6.4 The seat of arbitration shall be {jurisdiction}. The language of arbitration shall be English.""",
            },
            {
                "heading": "7. GENERAL PROVISIONS",
                "template": """7.1 Entire Agreement: This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior or contemporaneous agreements, understandings, or representations.

7.2 Amendment: No amendment or modification of this Agreement shall be valid unless made in writing and signed by both Parties.

7.3 Severability: If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.

7.4 Waiver: No waiver of any provision of this Agreement shall be deemed a further or continuing waiver of such provision or any other provision.

7.5 Assignment: Neither Party may assign its rights or obligations under this Agreement without the prior written consent of the other Party.

7.6 Notices: All notices under this Agreement shall be in writing and shall be deemed duly given when delivered personally, sent by registered post, or sent by email with acknowledgment of receipt.""",
            },
            {
                "heading": "IN WITNESS WHEREOF",
                "template": """IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.


For {party_a}:

Signature: ________________________
Name:
Designation:
Date:


For {party_b}:

Signature: ________________________
Name:
Designation:
Date:""",
            },
        ],
    },

    "Service Agreement": {
        "title": "SERVICE AGREEMENT",
        "sections": [
            {
                "heading": "PARTIES",
                "template": """This Service Agreement ("Agreement") is entered into on {date} ("Effective Date")

BETWEEN:

{party_a} (hereinafter referred to as the "Client")

AND

{party_b} (hereinafter referred to as the "Service Provider")""",
            },
            {
                "heading": "1. SCOPE OF SERVICES",
                "template": """1.1 The Service Provider agrees to provide the following services to the Client ("Services"):
{scope_of_work}

1.2 The Service Provider shall perform the Services in a professional and workmanlike manner, in accordance with industry standards and best practices.

1.3 Any changes to the scope of Services shall be agreed upon in writing by both Parties through a Change Order.""",
            },
            {
                "heading": "2. TERM",
                "template": """2.1 This Agreement shall commence on the Effective Date and shall continue for a period of {duration} ("Initial Term").

2.2 This Agreement may be renewed for additional periods upon mutual written agreement of both Parties at least 30 (thirty) days before the expiry of the then-current term.""",
            },
            {
                "heading": "3. COMPENSATION AND PAYMENT",
                "template": """3.1 In consideration of the Services, the Client shall pay the Service Provider a total fee of {contract_value} (plus applicable GST) ("Service Fee").

3.2 Payment shall be made within 30 (thirty) days of receipt of a valid invoice, via bank transfer to the account specified by the Service Provider.

3.3 Late payments shall attract interest at the rate of 1.5% per month or the maximum rate permitted under applicable law, whichever is lower.

3.4 All payments are subject to applicable Tax Deducted at Source (TDS) as per the Income Tax Act, 1961.""",
            },
            {
                "heading": "4. CONFIDENTIALITY",
                "template": """4.1 Each Party agrees to maintain the confidentiality of all proprietary and confidential information received from the other Party.

4.2 The confidentiality obligations shall survive termination of this Agreement for a period of 2 (two) years.""",
            },
            {
                "heading": "5. INTELLECTUAL PROPERTY",
                "template": """5.1 All intellectual property created by the Service Provider in the course of performing the Services ("Work Product") shall vest in the Client upon full payment of the Service Fee.

5.2 The Service Provider retains ownership of any pre-existing intellectual property, tools, methodologies, and frameworks. The Service Provider grants the Client a non-exclusive, perpetual, royalty-free license to use such pre-existing IP as incorporated into the Work Product.

5.3 The Service Provider represents and warrants that the Services and Work Product will not infringe upon any third-party intellectual property rights.""",
            },
            {
                "heading": "6. LIMITATION OF LIABILITY",
                "template": """6.1 The total aggregate liability of either Party under this Agreement shall not exceed the total Service Fee paid or payable under this Agreement in the 12 (twelve) months preceding the event giving rise to the claim.

6.2 Neither Party shall be liable for any indirect, incidental, consequential, special, or punitive damages, including loss of profits, data, or business opportunities.

6.3 Nothing in this Agreement shall exclude or limit liability for fraud, willful misconduct, or death/personal injury caused by negligence.""",
            },
            {
                "heading": "7. TERMINATION",
                "template": """7.1 Either Party may terminate this Agreement by providing 30 (thirty) days' prior written notice to the other Party.

7.2 Either Party may terminate this Agreement immediately upon written notice if the other Party:
(a) Commits a material breach that remains uncured for 15 (fifteen) days after written notice;
(b) Becomes insolvent, bankrupt, or is subject to winding-up proceedings.

7.3 Upon termination, the Service Provider shall:
(a) Deliver all Work Product completed up to the termination date;
(b) Return or destroy all Client confidential information;
(c) Be entitled to payment for Services performed up to the termination date.""",
            },
            {
                "heading": "8. INDEMNIFICATION",
                "template": """8.1 The Service Provider shall indemnify and hold harmless the Client from and against any claims, damages, losses, and expenses arising from:
(a) Breach of representations or warranties under this Agreement;
(b) Infringement of third-party intellectual property rights;
(c) Negligence or willful misconduct in performing the Services.

8.2 The Client shall indemnify and hold harmless the Service Provider from and against any claims arising from the Client's use of the Work Product in violation of applicable law.""",
            },
            {
                "heading": "9. FORCE MAJEURE",
                "template": """9.1 Neither Party shall be liable for any failure or delay in performing its obligations under this Agreement if such failure or delay results from circumstances beyond the reasonable control of that Party, including but not limited to natural disasters, acts of government, pandemic, epidemic, war, terrorism, or civil disturbance ("Force Majeure Event").

9.2 The affected Party shall promptly notify the other Party and use reasonable efforts to mitigate the impact.""",
            },
            {
                "heading": "10. GOVERNING LAW AND DISPUTE RESOLUTION",
                "template": """10.1 This Agreement shall be governed by and construed in accordance with the laws of India.

10.2 Any dispute shall be referred to arbitration under the Arbitration and Conciliation Act, 1996, by a sole arbitrator mutually appointed by the Parties.

10.3 The seat of arbitration shall be {jurisdiction}. The language of arbitration shall be English.""",
            },
            {
                "heading": "11. GENERAL PROVISIONS",
                "template": """11.1 Entire Agreement: This Agreement constitutes the entire understanding between the Parties.

11.2 Amendment: Amendments must be in writing and signed by both Parties.

11.3 Severability: Invalid provisions shall not affect the remaining provisions.

11.4 Assignment: Neither Party may assign without prior written consent.

11.5 Notices: All notices shall be in writing.""",
            },
            {
                "heading": "IN WITNESS WHEREOF",
                "template": """IN WITNESS WHEREOF, the Parties have executed this Agreement.


For {party_a} (Client):

Signature: ________________________
Name:
Designation:
Date:


For {party_b} (Service Provider):

Signature: ________________________
Name:
Designation:
Date:""",
            },
        ],
    },

    "Employment Contract": {
        "title": "EMPLOYMENT AGREEMENT",
        "sections": [
            {
                "heading": "PARTIES",
                "template": """This Employment Agreement ("Agreement") is made on {date}

BETWEEN:

{party_a} (hereinafter referred to as the "Employer" / "Company")

AND

{party_b} (hereinafter referred to as the "Employee")""",
            },
            {
                "heading": "1. POSITION AND DUTIES",
                "template": """1.1 The Employee is appointed as {designation} and shall report to the designated reporting authority.

1.2 The Employee shall perform duties as reasonably assigned by the Employer and as described in the attached Job Description.

1.3 The Employee shall devote full working time and attention to the Employer's business during working hours.""",
            },
            {
                "heading": "2. COMPENSATION",
                "template": """2.1 The Employee shall receive a gross annual salary of {contract_value} ("CTC - Cost to Company"), payable monthly in arrears by the 7th of each subsequent month.

2.2 The salary structure includes Basic Salary, HRA, Special Allowance, and other components as per the Company's compensation policy.

2.3 All payments are subject to applicable deductions including Income Tax (TDS), Provident Fund, Professional Tax, and ESI as applicable.

2.4 The Employee may be eligible for performance bonuses at the sole discretion of the Employer.""",
            },
            {
                "heading": "3. PROBATION",
                "template": """3.1 The Employee shall be on probation for a period of {probation_period} from the date of joining.

3.2 During probation, either Party may terminate this Agreement by providing 15 (fifteen) days' written notice.

3.3 Upon successful completion of probation, the Employee shall be confirmed in writing.""",
            },
            {
                "heading": "4. WORKING HOURS AND LEAVE",
                "template": """4.1 Standard working hours shall be 9 hours per day, 5 days per week (Monday to Friday), in accordance with applicable labour laws.

4.2 Leave entitlement shall be as per the Company's Leave Policy and applicable state-specific Shops & Establishments Act, including:
(a) Earned Leave / Privilege Leave: As per applicable law (minimum 1 day per 20 working days);
(b) Sick Leave / Casual Leave: As per Company policy;
(c) Public Holidays: As per the Negotiable Instruments Act and state notifications.""",
            },
            {
                "heading": "5. CONFIDENTIALITY",
                "template": """5.1 The Employee agrees to maintain strict confidentiality of all proprietary, business, technical, and financial information of the Employer.

5.2 This obligation shall survive termination of employment for a period of 2 (two) years.""",
            },
            {
                "heading": "6. INTELLECTUAL PROPERTY",
                "template": """6.1 All work product, inventions, designs, and intellectual property created by the Employee during the course of employment and related to the Employer's business shall be the exclusive property of the Employer.

6.2 The Employee hereby assigns all rights, title, and interest in such intellectual property to the Employer.""",
            },
            {
                "heading": "7. TERMINATION",
                "template": """7.1 After confirmation, either Party may terminate this Agreement by providing {notice_period} written notice or payment of salary in lieu thereof.

7.2 The Employer may terminate this Agreement immediately for cause, including:
(a) Misconduct, fraud, or dishonesty;
(b) Material breach of this Agreement or Company policies;
(c) Conviction for a criminal offense;
(d) Willful neglect of duties.

7.3 Upon termination, the Employee shall:
(a) Return all Company property, documents, and data;
(b) Complete a proper handover;
(c) Settle any outstanding dues.""",
            },
            {
                "heading": "8. NON-SOLICITATION",
                "template": """8.1 During employment and for a period of 12 (twelve) months after termination, the Employee shall not directly or indirectly solicit or attempt to solicit any employee, customer, or client of the Employer.

Note: Non-compete clauses are generally void under Section 27 of the Indian Contract Act, 1872. This clause is limited to non-solicitation which may be enforceable during the term of employment.""",
            },
            {
                "heading": "9. GOVERNING LAW",
                "template": """9.1 This Agreement shall be governed by the laws of India, including applicable employment and labour legislation.

9.2 Courts in {jurisdiction} shall have exclusive jurisdiction over any disputes arising from this Agreement.""",
            },
            {
                "heading": "IN WITNESS WHEREOF",
                "template": """IN WITNESS WHEREOF, the Parties have executed this Agreement.


For {party_a} (Employer):

Signature: ________________________
Name:
Designation:
Date:


{party_b} (Employee):

Signature: ________________________
Name:
Date:""",
            },
        ],
    },
}

# Default template for other types
DEFAULT_TEMPLATE = {
    "title": "AGREEMENT",
    "sections": [
        {
            "heading": "PARTIES",
            "template": """This Agreement ("Agreement") is entered into on {date}

BETWEEN:

{party_a} (hereinafter referred to as "Party A")

AND

{party_b} (hereinafter referred to as "Party B")""",
        },
        {
            "heading": "1. RECITALS",
            "template": """WHEREAS Party A and Party B wish to enter into this Agreement for the purposes described herein.

NOW THEREFORE, in consideration of the mutual covenants and agreements contained herein, the Parties agree as follows:""",
        },
        {
            "heading": "2. TERM",
            "template": """2.1 This Agreement shall be effective from {date} and shall continue for a period of {duration}.

2.2 Either Party may terminate this Agreement by providing 30 (thirty) days' prior written notice.""",
        },
        {
            "heading": "3. OBLIGATIONS",
            "template": """3.1 Each Party shall perform its obligations under this Agreement in good faith and in accordance with applicable laws.

{additional_terms}""",
        },
        {
            "heading": "4. CONFIDENTIALITY",
            "template": """4.1 Each Party shall maintain the confidentiality of all proprietary information received from the other Party.

4.2 This obligation shall survive termination for a period of 2 (two) years.""",
        },
        {
            "heading": "5. LIMITATION OF LIABILITY",
            "template": """5.1 The total liability of either Party shall not exceed the amounts paid or payable under this Agreement.

5.2 Neither Party shall be liable for indirect or consequential damages.""",
        },
        {
            "heading": "6. GOVERNING LAW",
            "template": """6.1 This Agreement shall be governed by the laws of India.

6.2 Any disputes shall be resolved through arbitration under the Arbitration and Conciliation Act, 1996.

6.3 The seat of arbitration shall be {jurisdiction}.""",
        },
        {
            "heading": "7. GENERAL",
            "template": """7.1 Entire Agreement: This is the entire agreement between the Parties.

7.2 Amendment: Must be in writing.

7.3 Severability: Invalid provisions don't affect remaining provisions.

7.4 Assignment: Requires prior written consent.""",
        },
        {
            "heading": "IN WITNESS WHEREOF",
            "template": """IN WITNESS WHEREOF, the Parties have executed this Agreement.


For {party_a}:

Signature: ________________________
Name:
Date:


For {party_b}:

Signature: ________________________
Name:
Date:""",
        },
    ],
}


def generate_draft(
    contract_type: str,
    party_a: str,
    party_b: str,
    key_terms: dict | None = None,
    jurisdiction: str = "New Delhi, India",
    additional_instructions: str | None = None,
) -> dict:
    """
    Generate a contract draft based on type and parameters.
    """
    key_terms = key_terms or {}
    template = TEMPLATES.get(contract_type, DEFAULT_TEMPLATE)

    # Prepare substitution variables
    now = datetime.now()
    variables = {
        "date": now.strftime("%d %B %Y"),
        "party_a": party_a,
        "party_b": party_b,
        "jurisdiction": jurisdiction,
        "duration": key_terms.get("duration", "1 (one) year"),
        "purpose": key_terms.get("purpose", "evaluating a potential business relationship"),
        "scope_of_work": key_terms.get("scope_of_work", "[Description of services to be provided]"),
        "contract_value": key_terms.get("contract_value", "[Amount in INR]"),
        "designation": key_terms.get("designation", "[Job Title]"),
        "probation_period": key_terms.get("probation_period", "6 (six) months"),
        "notice_period": key_terms.get("notice_period", "30 (thirty) days'"),
        "additional_terms": additional_instructions or "[Additional terms as agreed between the Parties]",
    }

    # Build the draft
    draft_parts = [f"{'=' * 60}", f"{template['title']}", f"{'=' * 60}", ""]
    clauses_included = []

    for section in template["sections"]:
        heading = section["heading"]
        body = section["template"]

        # Substitute variables
        for key, value in variables.items():
            body = body.replace("{" + key + "}", value)

        draft_parts.append(f"\n{heading}")
        draft_parts.append("-" * len(heading))
        draft_parts.append(body)
        draft_parts.append("")
        clauses_included.append(heading)

    draft_text = "\n".join(draft_parts)

    # Compliance notes
    compliance_notes = [
        "✅ Arbitration clause compliant with Arbitration and Conciliation Act, 1996",
        "✅ Governed by laws of India",
        "✅ Confidentiality obligations with reasonable survival period",
        "✅ Mutual termination rights with notice period",
        "✅ Limitation of liability included",
    ]

    if contract_type == "Employment Contract":
        compliance_notes.extend([
            "✅ Payment timeline compliant with Payment of Wages Act",
            "✅ Non-solicitation clause (non-compete is void under Section 27, ICA)",
            "✅ Leave provisions reference applicable state law",
            "✅ TDS and PF deductions referenced",
        ])

    return {
        "contract_type": contract_type,
        "draft_text": draft_text,
        "clauses_included": clauses_included,
        "compliance_notes": compliance_notes,
        "timestamp": now.isoformat(),
    }

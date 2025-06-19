from typing import Dict, List, Any
from datetime import datetime

def generate_death_notification_letter(platform: str, deceased_name: str, executor_name: str, relationship: str) -> Dict[str, str]:
    """Generate platform-specific death notification letter.
    
    Args:
        platform: Platform name (e.g., 'google.com', 'facebook.com')
        deceased_name: Full name of deceased person
        executor_name: Name of executor/family member
        relationship: Relationship to deceased
        
    Returns:
        dict: Generated letter content and instructions
    """
    
    platform_specific_info = {
        "google.com": {
            "address": "Google LLC\nInactive Account Manager\n1600 Amphitheatre Parkway\nMountain View, CA 94043",
            "subject": "Request for Access to Deceased User Account",
            "special_instructions": "Submit through Google's official deceased user form online",
            "form_url": "https://support.google.com/accounts/contact/deceased"
        },
        "facebook.com": {
            "address": "Meta Platforms, Inc.\nDeceased User Requests\n1 Meta Way\nMenlo Park, CA 94025",
            "subject": "Deceased User Account - Request for Access",
            "special_instructions": "Use Facebook's memorialization request form",
            "form_url": "https://www.facebook.com/help/contact/228813257197480"
        },
        "apple.com": {
            "address": "Apple Inc.\nPrivacy Team\nOne Apple Park Way\nCupertino, CA 95014",
            "subject": "Digital Legacy Contact Request",
            "special_instructions": "Court order typically required for Apple ID access",
            "form_url": "Contact Apple Support directly"
        }
    }
    
    platform_info = platform_specific_info.get(platform, {
        "address": f"{platform.title()} Support Team",
        "subject": "Deceased User Account Access Request",
        "special_instructions": "Contact customer support for specific procedures",
        "form_url": "Check platform's help documentation"
    })
    
    letter_template = f"""
{platform_info['address']}

Date: {datetime.now().strftime('%B %d, %Y')}

Subject: {platform_info['subject']}

Dear {platform.split('.')[0].title()} Support Team,

I am writing to notify you of the death of {deceased_name}, who passed away on [DATE_OF_DEATH]. I am the {relationship} of the deceased and have been appointed as the executor of their estate.

I am requesting access to the deceased's account(s) on your platform to:
1. Preserve important family memories and documents
2. Close the account in accordance with your policies
3. Retrieve any important personal or business information
4. Address any ongoing services or subscriptions

Account Information:
- Account Holder: {deceased_name}
- Relationship to Deceased: {relationship}
- Executor/Requester: {executor_name}

I have attached the following required documentation:
□ Certified Death Certificate
□ Copy of my government-issued identification
□ Proof of relationship to the deceased
□ Legal documentation establishing my authority as executor

Please advise me on any additional steps required to process this request. I understand that this process may take several weeks and appreciate your assistance during this difficult time.

I can be reached at [YOUR_EMAIL] or [YOUR_PHONE] if you need any additional information.

Thank you for your prompt attention to this matter.

Sincerely,

{executor_name}
Executor of the Estate of {deceased_name}

---
INSTRUCTIONS:
1. Fill in the bracketed information: [DATE_OF_DEATH], [YOUR_EMAIL], [YOUR_PHONE]
2. Gather all required documents before submission
3. {platform_info['special_instructions']}
4. Submission method: {platform_info['form_url']}
"""
    
    return {
        "status": "success",
        "platform": platform,
        "letter_content": letter_template.strip(),
        "required_documents": [
            "Certified Death Certificate",
            "Government-issued ID of executor",
            "Proof of relationship to deceased",
            "Legal documentation of executor authority"
        ],
        "submission_url": platform_info['form_url'],
        "estimated_processing_time": "30-90 days depending on platform"
    }

def generate_probate_petition_outline(state: str, deceased_name: str, executor_name: str, assets_summary: str) -> Dict[str, str]:
    """Generate probate court petition outline.
    
    Args:
        state: State where probate will be filed
        deceased_name: Full name of deceased person
        executor_name: Name of proposed executor
        assets_summary: Summary of digital assets discovered
        
    Returns:
        dict: Probate petition outline and filing instructions
    """
    
    petition_outline = f"""
PROBATE COURT PETITION OUTLINE
State: {state}
Case: Estate of {deceased_name}

I. PETITION FOR APPOINTMENT OF PERSONAL REPRESENTATIVE
   A. Petitioner Information
      - Name: {executor_name}
      - Relationship to Deceased: [RELATIONSHIP]
      - Address: [EXECUTOR_ADDRESS]
   
   B. Deceased Information
      - Full Name: {deceased_name}
      - Date of Death: [DATE_OF_DEATH]
      - Date of Birth: [DATE_OF_BIRTH]
      - Last Address: [DECEASED_ADDRESS]
   
   C. Estate Information
      - Estimated Value: [ESTATE_VALUE]
      - Will Status: [WITH_WILL or INTESTATE]
      - Digital Assets Summary: {assets_summary}

II. DIGITAL ASSET MANAGEMENT AUTHORITY
   A. Request for Authority to Access Digital Assets
      - Email accounts containing important communications
      - Cloud storage with family photos and documents
      - Financial accounts and cryptocurrency
      - Business accounts and intellectual property
      - Social media accounts for memorialization
   
   B. Compliance with State Digital Asset Laws
      - Reference to Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA)
      - Authority to act as fiduciary for digital assets
      - Powers to manage, access, and distribute digital property

III. REQUIRED ATTACHMENTS
   □ Death Certificate (certified copy)
   □ Will (if available)
   □ Digital Asset Inventory
   □ Waiver of Notice (if applicable)
   □ Bond (if required by court)
   □ Acceptance of Appointment

IV. RELIEF SOUGHT
   The Court is respectfully requested to:
   1. Appoint {executor_name} as Personal Representative
   2. Grant authority to access and manage digital assets
   3. Issue Letters Testamentary/Letters of Administration
   4. Authorize communication with digital service providers
   5. Grant such other relief as the Court deems proper

V. STATE-SPECIFIC REQUIREMENTS FOR {state.upper()}
   [This section would include state-specific legal requirements]

NEXT STEPS:
1. Complete all bracketed information
2. Gather required attachments
3. File with appropriate probate court
4. Pay required filing fees
5. Serve notice to interested parties as required by law

ESTIMATED TIMELINE: 4-8 weeks for court approval
ESTIMATED COST: $500-2,000 in court fees and legal costs
"""
    
    return {
        "status": "success",
        "state": state,
        "petition_outline": petition_outline.strip(),
        "filing_requirements": [
            f"File with {state} Probate Court",
            "Pay required filing fees",
            "Serve notice to heirs and beneficiaries",
            "Attend court hearing if required"
        ],
        "estimated_timeline": "4-8 weeks for court approval",
        "recommendation": "Consult with a local probate attorney for state-specific requirements"
    }

def check_state_digital_asset_laws(state: str) -> Dict[str, Any]:
    """Check state-specific digital asset inheritance laws.
    
    Args:
        state: State to check laws for
        
    Returns:
        dict: State digital asset law information
    """
    
    # Sample state laws (in production, this would be a comprehensive database)
    state_laws = {
        "california": {
            "law_name": "California Revised Uniform Fiduciary Access to Digital Assets Act",
            "code_section": "Probate Code Section 850-859",
            "key_provisions": [
                "Fiduciaries can access digital assets unless prohibited by will",
                "Service providers must comply with lawful requests",
                "Privacy protections for electronic communications"
            ],
            "executor_powers": "Broad authority to manage digital assets",
            "court_order_required": False
        },
        "new_york": {
            "law_name": "New York RUFADAA",
            "code_section": "EPTL Section 13-A",
            "key_provisions": [
                "Executor has authority over digital assets",
                "Terms of service cannot override state law",
                "Separate procedures for electronic communications"
            ],
            "executor_powers": "Full authority with proper documentation",
            "court_order_required": False
        },
        "texas": {
            "law_name": "Texas Estates Code Chapter 2001",
            "code_section": "Texas Estates Code Sec. 2001.001-2001.004",
            "key_provisions": [
                "Independent administration preferred",
                "Digital assets treated as personal property",
                "Court supervision may be required for some assets"
            ],
            "executor_powers": "Authority depends on will provisions",
            "court_order_required": "Sometimes"
        }
    }
    
    state_info = state_laws.get(state.lower(), {
        "law_name": f"{state} Digital Asset Laws",
        "code_section": "Consult state statutes",
        "key_provisions": ["Check state-specific RUFADAA adoption"],
        "executor_powers": "Varies by state",
        "court_order_required": "Possibly"
    })
    
    return {
        "status": "success",
        "state": state,
        "digital_asset_law": state_info,
        "recommendation": "Consult with local estate attorney for current law interpretation",
        "compliance_checklist": [
            "Verify current state law status",
            "Review will for digital asset provisions",
            "Prepare proper executor documentation",
            "Follow state-specific procedures"
        ]
    }
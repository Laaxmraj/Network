from typing import Dict, List, Any
from datetime import datetime
import math

def find_nearby_lawyers(zipcode: str, radius_miles: int = 25, specialty: str = "probate") -> Dict[str, Any]:
    """Find nearby lawyers specializing in probate/estate law based on zipcode.
    
    Args:
        zipcode: 5-digit US zipcode
        radius_miles: Search radius in miles (default 25)
        specialty: Legal specialty to search for (default "probate")
        
    Returns:
        dict: List of nearby lawyers with contact information
    """
    
    # Simulated lawyer database (in production, this would connect to a real API or database)
    # Key: zipcode prefix, Value: list of lawyers in that area
    lawyer_database = {
        "021": [  # Boston area
            {
                "name": "Sarah J. Mitchell, Esq.",
                "firm": "Mitchell & Associates Estate Law",
                "specialties": ["probate", "estate planning", "digital assets"],
                "address": "100 Federal Street, Suite 1900, Boston, MA 02110",
                "phone": "(617) 555-0123",
                "email": "smitchell@mitchellestatelaw.com",
                "website": "www.mitchellestatelaw.com",
                "years_experience": 15,
                "rating": 4.8,
                "consultation_fee": "$350",
                "distance_miles": 2.3,
                "notable": "Certified specialist in digital asset inheritance"
            },
            {
                "name": "Robert Chen, JD, LLM",
                "firm": "Chen Legal Group",
                "specialties": ["probate", "trust administration", "tax law"],
                "address": "1 Boston Place, Suite 2700, Boston, MA 02108",
                "phone": "(617) 555-0456",
                "email": "rchen@chenlegal.com",
                "website": "www.chenlegal.com",
                "years_experience": 22,
                "rating": 4.9,
                "consultation_fee": "Free initial consultation",
                "distance_miles": 3.1,
                "notable": "Former probate court judge"
            },
            {
                "name": "Maria Rodriguez, Esq.",
                "firm": "Rodriguez & Partners LLP",
                "specialties": ["probate", "estate planning", "elder law"],
                "address": "200 State Street, Boston, MA 02109",
                "phone": "(617) 555-0789",
                "email": "mrodriguez@rodriguezlaw.com",
                "website": "www.rodriguezlaw.com",
                "years_experience": 18,
                "rating": 4.7,
                "consultation_fee": "$250",
                "distance_miles": 4.5,
                "notable": "Bilingual services (English/Spanish)"
            }
        ],
        "100": [  # New York area
            {
                "name": "James Harrison, Esq.",
                "firm": "Harrison & Stone Estate Attorneys",
                "specialties": ["probate", "estate litigation", "digital assets"],
                "address": "445 Park Avenue, 9th Floor, New York, NY 10022",
                "phone": "(212) 555-0111",
                "email": "jharrison@hsestatelaw.com",
                "website": "www.hsestatelaw.com",
                "years_experience": 25,
                "rating": 4.9,
                "consultation_fee": "$500",
                "distance_miles": 1.8,
                "notable": "Published author on digital estate planning"
            },
            {
                "name": "Dr. Lisa Wang, JD, PhD",
                "firm": "Wang International Estate Law",
                "specialties": ["probate", "international estates", "cryptocurrency"],
                "address": "1 Wall Street, Suite 1500, New York, NY 10005",
                "phone": "(212) 555-0222",
                "email": "lwang@wangestatelaw.com",
                "website": "www.wangestatelaw.com",
                "years_experience": 12,
                "rating": 4.8,
                "consultation_fee": "$450",
                "distance_miles": 5.2,
                "notable": "Expert in cryptocurrency inheritance"
            }
        ],
        "900": [  # Los Angeles area
            {
                "name": "Michael Thompson, Esq.",
                "firm": "Thompson Probate Law Center",
                "specialties": ["probate", "trust administration", "conservatorship"],
                "address": "333 South Grand Avenue, Suite 3600, Los Angeles, CA 90071",
                "phone": "(213) 555-0333",
                "email": "mthompson@thompsonprobate.com",
                "website": "www.thompsonprobate.com",
                "years_experience": 20,
                "rating": 4.7,
                "consultation_fee": "$400",
                "distance_miles": 3.4,
                "notable": "24/7 emergency probate services"
            },
            {
                "name": "Amanda Foster, JD",
                "firm": "Foster & Associates",
                "specialties": ["probate", "estate planning", "entertainment law"],
                "address": "10100 Santa Monica Blvd, Suite 2200, Los Angeles, CA 90067",
                "phone": "(310) 555-0444",
                "email": "afoster@fosterlaw.com",
                "website": "www.fosterlaw.com",
                "years_experience": 16,
                "rating": 4.8,
                "consultation_fee": "Free 30-minute consultation",
                "distance_miles": 8.7,
                "notable": "Specializes in entertainment industry estates"
            }
        ],
        "750": [  # Austin/Texas area
            {
                "name": "David Martinez, Esq.",
                "firm": "Martinez Estate Law Group",
                "specialties": ["probate", "estate planning", "business succession"],
                "address": "401 Congress Avenue, Suite 2100, Austin, TX 78701",
                "phone": "(512) 555-0555",
                "email": "dmartinez@martinezestatelaw.com",
                "website": "www.martinezestatelaw.com",
                "years_experience": 19,
                "rating": 4.9,
                "consultation_fee": "$300",
                "distance_miles": 2.1,
                "notable": "Board certified in estate planning"
            }
        ],
        "600": [  # Chicago area
            {
                "name": "Patricia O'Brien, JD, CPA",
                "firm": "O'Brien Tax & Estate Law",
                "specialties": ["probate", "estate tax", "trust administration"],
                "address": "233 S Wacker Drive, Suite 8400, Chicago, IL 60606",
                "phone": "(312) 555-0666",
                "email": "pobrien@obrienlaw.com",
                "website": "www.obrienlaw.com",
                "years_experience": 23,
                "rating": 4.8,
                "consultation_fee": "$375",
                "distance_miles": 4.2,
                "notable": "Dual licensed attorney and CPA"
            }
        ]
    }
    
    # Extract zipcode prefix
    zip_prefix = zipcode[:3] if len(zipcode) >= 3 else ""
    
    # Get lawyers for the area
    area_lawyers = lawyer_database.get(zip_prefix, [])
    
    # If no lawyers found in exact area, search nearby areas
    if not area_lawyers:
        # Try to find lawyers in nearby zipcodes
        nearby_prefixes = {
            "022": "021",  # Cambridge to Boston
            "024": "021",  # Quincy to Boston
            "101": "100",  # Manhattan adjacent
            "902": "900",  # LA adjacent
            "787": "750",  # Austin adjacent
            "606": "600"   # Chicago adjacent
        }
        
        alternate_prefix = nearby_prefixes.get(zip_prefix)
        if alternate_prefix:
            area_lawyers = lawyer_database.get(alternate_prefix, [])
            # Increase distance for lawyers from adjacent areas
            for lawyer in area_lawyers:
                lawyer["distance_miles"] += 10
    
    # Filter by radius
    filtered_lawyers = [
        lawyer for lawyer in area_lawyers 
        if lawyer["distance_miles"] <= radius_miles
    ]
    
    # Sort by rating and distance
    filtered_lawyers.sort(
        key=lambda x: (x["rating"], -x["distance_miles"]), 
        reverse=True
    )
    
    # Add additional helpful information
    for lawyer in filtered_lawyers:
        # Calculate estimated response time
        if lawyer["rating"] >= 4.8:
            lawyer["typical_response_time"] = "Same day"
        elif lawyer["rating"] >= 4.5:
            lawyer["typical_response_time"] = "1-2 business days"
        else:
            lawyer["typical_response_time"] = "2-3 business days"
        
        # Add availability info
        lawyer["emergency_available"] = lawyer["years_experience"] > 15
        
        # Add digital estate expertise level
        if "digital assets" in lawyer["specialties"] or "cryptocurrency" in lawyer["specialties"]:
            lawyer["digital_estate_expertise"] = "Expert"
        elif lawyer["years_experience"] > 20:
            lawyer["digital_estate_expertise"] = "Experienced"
        else:
            lawyer["digital_estate_expertise"] = "Familiar"
    
    return {
        "status": "success",
        "zipcode": zipcode,
        "search_radius_miles": radius_miles,
        "lawyers_found": len(filtered_lawyers),
        "lawyers": filtered_lawyers[:5],  # Return top 5 lawyers
        "search_tips": [
            "Contact 2-3 lawyers for consultations to find the best fit",
            "Ask about experience with digital asset recovery",
            "Inquire about flat fee vs hourly billing options",
            "Verify state bar membership and any specializations"
        ],
        "questions_to_ask": [
            "What is your experience with digital estate recovery?",
            "Do you handle platform-specific recovery requests?",
            "What are your fees for probate administration?",
            "Can you assist with out-of-state digital assets?",
            "What is your typical timeline for probate completion?"
        ],
        "average_consultation_fee": _calculate_average_fee(filtered_lawyers),
        "disclaimer": "This is a simulated list. In production, verify all lawyer credentials through state bar associations."
    }

def _calculate_average_fee(lawyers: List[Dict]) -> str:
    """Calculate average consultation fee from lawyer list."""
    fees = []
    for lawyer in lawyers:
        fee = lawyer.get("consultation_fee", "")
        if "$" in fee and "Free" not in fee:
            try:
                amount = int(fee.replace("$", "").split()[0])
                fees.append(amount)
            except:
                pass
    
    if fees:
        avg = sum(fees) / len(fees)
        return f"${int(avg)}"
    return "Varies"

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
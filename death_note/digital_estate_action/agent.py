import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any
import os
from datetime import datetime, timedelta
import json
from google.adk.agents import Agent

# Import the new lawyer finder function
#from tools.legal_tools import find_nearby_lawyers
#from tools.legal_tools import find_nearby_lawyers

# Simple file-based tracking
TRACKING_FILE = "case_tracking.json"

def send_recovery_email(platform: str, deceased_name: str, deceased_email: str,
                       deceased_date: str, executor_name: str, executor_email: str, 
                       executor_relationship: str, available_documents: str) -> dict:
    """Send recovery email to platform support.
    
    Args:
        platform: Platform name (Google, Facebook, Apple, Microsoft)
        deceased_name: Full name of deceased person
        deceased_email: Email address of deceased  
        deceased_date: Date of death (YYYY-MM-DD format)
        executor_name: Name of executor/family member
        executor_email: Executor's email address
        executor_relationship: Relationship to deceased (spouse, child, etc.)
        available_documents: List of available documents (comma-separated)
        
    Returns:
        dict: Result of email sending operation with case tracking
    """
    
    # Platform-specific information
    platform_info = {
        "Google": {
            "support_email": "accounts-support@google.com",
            "process": "deceased user notification",
            "timeline": "30-90 days",
            "form_url": "https://support.google.com/accounts/contact/deceased"
        },
        "Facebook": {
            "support_email": "support@fb.com", 
            "process": "memorialization request",
            "timeline": "14-30 days",
            "form_url": "https://www.facebook.com/help/contact/234739086860192"
        },
        "Apple": {
            "support_email": "account_security@apple.com",
            "process": "digital legacy contact",
            "timeline": "60-180 days", 
            "form_url": "https://support.apple.com/en-us/HT208510"
        },
        "Microsoft": {
            "support_email": "msaccount@microsoft.com",
            "process": "account closure",
            "timeline": "30-60 days",
            "form_url": "https://support.microsoft.com/account-billing"
        }
    }
    
    info = platform_info.get(platform, platform_info["Google"])
    
    # Generate professional email content
    subject = f"Digital Estate Recovery Request - {deceased_name} (Deceased)"
    
    body = f"""Dear {platform} Support Team,

I hope this message finds you well. I am writing to inform you of the passing of {deceased_name}, who held an account with {platform} under the email address {deceased_email}.

DECEASED INFORMATION:
- Full Name: {deceased_name}
- Email Address: {deceased_email}
- Date of Passing: {deceased_date}

REQUESTING PARTY INFORMATION:
- Name: {executor_name}
- Email: {executor_email}  
- Relationship to Deceased: {executor_relationship}

I am reaching out to request assistance with accessing or managing the deceased's {platform} account in accordance with your {info['process']} procedures. This request is being made to:

1. Preserve important family memories and documents
2. Properly close the account per your policies
3. Retrieve any essential personal or business information
4. Address ongoing services or subscriptions

AVAILABLE DOCUMENTATION:
{available_documents}

I understand that {platform} has specific procedures for handling deceased user accounts, and I am prepared to provide any additional documentation required. Based on your published guidelines, I expect this process may take approximately {info['timeline']}.

If there is a preferred form or additional process I should follow, please direct me to the appropriate resources. I have noted that {platform} may have an online form at: {info['form_url']}

I would greatly appreciate your guidance on the next steps and any specific requirements for processing this request. This is already a difficult time for our family, and your assistance would be invaluable.

Please feel free to contact me at {executor_email} or respond to this email if you need any additional information or documentation.

Thank you for your time and consideration.

Respectfully,

{executor_name}
{executor_relationship} of {deceased_name}
Email: {executor_email}

---
This request is made in accordance with applicable digital estate laws and {platform}'s deceased user policies."""

    # Create case ID for tracking
    case_id = f"{platform.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store case for tracking
    try:
        tracking_data = {}
        if os.path.exists(TRACKING_FILE):
            try:
                with open(TRACKING_FILE, 'r') as f:
                    tracking_data = json.load(f)
            except:
                tracking_data = {}
        
        tracking_data[case_id] = {
            "case_id": case_id,
            "platform": platform,
            "deceased_name": deceased_name,
            "executor_name": executor_name,
            "action_type": "email",
            "created_date": datetime.now().isoformat(),
            "status": "submitted",
            "last_updated": datetime.now().isoformat()
        }
        
        with open(TRACKING_FILE, 'w') as f:
            json.dump(tracking_data, f, indent=2, default=str)
    except Exception as e:
        print(f"Warning: Could not save tracking data: {e}")
    
    # Check if real email sending is configured
    gmail_email = os.getenv('GMAIL_EMAIL')
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if gmail_email and gmail_password:
        # Send real email
        try:
            msg = MIMEMultipart()
            msg['From'] = gmail_email
            msg['To'] = info['support_email']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(gmail_email, gmail_password)
                server.send_message(msg)
            
            return {
                "status": "sent",
                "case_id": case_id,
                "message": f"✅ Recovery email sent to {platform} support successfully!",
                "platform": platform,
                "support_email": info['support_email'],
                "estimated_response_time": info['timeline'],
                "email_preview": {
                    "subject": subject,
                    "body_preview": body[:500] + "..."
                },
                "next_steps": [
                    f"Monitor your email ({executor_email}) for responses from {platform}",
                    f"Expected response time: {info['timeline']}",
                    f"Use case ID {case_id} to track progress",
                    "Prepare to provide additional documentation if requested"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "case_id": case_id,
                "message": f"❌ Failed to send email: {str(e)}",
                "email_preview": {
                    "subject": subject,
                    "body_preview": body[:500] + "..."
                }
            }
    else:
        # Demo mode - simulate sending
        return {
            "status": "demo",
            "case_id": case_id,
            "message": f"📧 DEMO MODE: Professional recovery email generated for {platform}",
            "platform": platform,
            "support_email": info['support_email'],
            "estimated_response_time": info['timeline'],
            "email_preview": {
                "subject": subject,
                "body_preview": body[:500] + "..."
            },
            "demo_note": "To send real emails, configure GMAIL_EMAIL and GMAIL_APP_PASSWORD in .env file",
            "next_steps": [
                f"Copy the email content and send manually to {info['support_email']}",
                f"Expected response time: {info['timeline']}",
                f"Use case ID {case_id} to track progress",
                "Or configure real email sending in .env file"
            ]
        }

def get_platform_form_instructions(platform: str) -> dict:
    """Get detailed form-filling instructions for platform recovery.
    
    Args:
        platform: Platform name (Google, Facebook, Apple, Microsoft)
        
    Returns:
        dict: Detailed instructions for platform-specific forms
    """
    
    platform_guides = {
        "Google": {
            "form_url": "https://support.google.com/accounts/contact/deceased",
            "form_name": "Google Deceased User Notification",
            "estimated_time": "10-15 minutes to complete",
            "processing_time": "30-90 days",
            "success_rate": "85%",
            "instructions": """
🌐 GOOGLE ACCOUNT RECOVERY FORM

📋 FORM URL: https://support.google.com/accounts/contact/deceased

📝 STEP-BY-STEP INSTRUCTIONS:

PREPARATION (Gather these first):
- Death certificate (certified copy, PDF scan)
- Your government-issued photo ID 
- Proof of relationship (birth/marriage certificate)
- Deceased person's Gmail address
- Any known recovery information

FORM COMPLETION:

Step 1: Access the Form
- Go to the URL above
- Click "Submit a deceased user notification"
- Choose your preferred language

Step 2: Deceased Person Information
- Full name (exactly as on death certificate)
- Email address (the Gmail account)
- Date of death (from death certificate)
- Country of residence at time of death

Step 3: Your Information
- Your full name
- Your email address
- Your relationship to deceased
- Your country of residence

Step 4: Document Upload
- Upload death certificate (PDF, under 25MB)
- Upload your government ID (PDF, under 25MB)
- Upload proof of relationship (PDF, under 25MB)
- Ensure all documents are clear and readable

Step 5: Request Type
- Choose "I want to close the account" OR
- Choose "I want to obtain data from the account"
- Explain briefly why you need access

🔍 TIPS FOR SUCCESS:
- Use high-quality document scans (300 DPI+)
- Make sure all text is clearly readable
- Provide complete, accurate information
- Be patient - Google reviews each case individually

📞 EXPECTED OUTCOME:
- Google will email you with updates
- Response typically within 30-90 days
- May request additional documentation
- Complete account data download if approved
            """,
            "required_documents": [
                "Death certificate (certified copy)",
                "Government-issued photo ID",
                "Proof of relationship to deceased"
            ]
        },
        
        "Facebook": {
            "form_url": "https://www.facebook.com/help/contact/234739086860192",
            "form_name": "Facebook Memorialization Request",
            "estimated_time": "5-10 minutes to complete",
            "processing_time": "14-30 days",
            "success_rate": "80%",
            "instructions": """
🌐 FACEBOOK MEMORIALIZATION FORM

📋 FORM URL: https://www.facebook.com/help/contact/234739086860192

📝 STEP-BY-STEP INSTRUCTIONS:

PREPARATION:
- Death certificate or obituary link
- Deceased person's Facebook profile URL
- Your government-issued ID
- Proof of relationship (if requesting data)

FORM COMPLETION:

Step 1: Choose Request Type
- "Memorialize this account" (converts to memorial)
- "Remove this account" (permanently deletes)
- "Request data from this account" (download info)

Step 2: Deceased Person Information
- Full name (as shown on Facebook)
- Facebook profile URL or username
- Date of death
- Upload death certificate or provide obituary URL

Step 3: Your Information
- Your full name
- Your email address
- Your relationship to the deceased
- Upload your government ID

🔍 TIPS FOR SUCCESS:
- Use published obituary if available (faster)
- Provide exact Facebook profile URL
- Clear, readable ID photo
- Be specific about your relationship

📞 EXPECTED OUTCOME:
- Facebook emails decision within 14-30 days
- Memorial accounts allow tribute posts
- Data requests may require additional verification
            """,
            "required_documents": [
                "Death certificate or obituary",
                "Government-issued photo ID",
                "Proof of relationship (for data requests)"
            ]
        }
    }
    
    if platform not in platform_guides:
        return {
            "status": "error",
            "message": f"Form instructions not available for {platform}",
            "available_platforms": ["Google", "Facebook", "Apple", "Microsoft"]
        }
    
    guide = platform_guides[platform]
    
    return {
        "status": "success",
        "platform": platform,
        "form_url": guide["form_url"],
        "form_name": guide["form_name"],
        "estimated_completion_time": guide["estimated_time"],
        "processing_time": guide["processing_time"],
        "success_rate": guide["success_rate"], 
        "instructions": guide["instructions"],
        "required_documents": guide["required_documents"],
        "summary": f"Complete the {guide['form_name']} at {guide['form_url']}. Expected processing time: {guide['processing_time']}."
    }

def track_case_status(case_id: str) -> dict:
    """Get current status of a case.
    
    Args:
        case_id: Case identifier to track (format: PLATFORM_YYYYMMDD_HHMMSS)
        
    Returns:
        dict: Current case status and timeline information
    """
    
    try:
        if not os.path.exists(TRACKING_FILE):
            return {
                "status": "not_found",
                "message": f"No tracking data found. Make sure you have the correct case ID.",
                "suggestion": "Case IDs are created when you send recovery emails. Format: GOOGLE_20241218_143052"
            }
        
        with open(TRACKING_FILE, 'r') as f:
            tracking_data = json.load(f)
    except:
        return {
            "status": "error",
            "message": "Error reading tracking data"
        }
    
    if case_id not in tracking_data:
        return {
            "status": "not_found",
            "message": f"Case ID {case_id} not found",
            "available_cases": list(tracking_data.keys())[:5],  # Show first 5 cases
            "suggestion": "Please check the case ID or use the exact ID provided when the case was created"
        }
    
    case = tracking_data[case_id]
    created_date = datetime.fromisoformat(case["created_date"])
    days_elapsed = (datetime.now() - created_date).days
    
    # Estimate current status based on platform and time elapsed
    platform = case["platform"]
    
    if platform == "Facebook":
        if days_elapsed < 14:
            current_status = "Under review"
            estimated_completion = f"{14 - days_elapsed} to {30 - days_elapsed} days remaining"
        elif days_elapsed < 30:
            current_status = "Should hear back soon"
            estimated_completion = f"Any day now to {30 - days_elapsed} days"
        else:
            current_status = "Consider following up"
            estimated_completion = "Send follow-up email or contact support"
            
    elif platform == "Google":
        if days_elapsed < 30:
            current_status = "Under review"
            estimated_completion = f"{30 - days_elapsed} to {90 - days_elapsed} days remaining"
        elif days_elapsed < 90:
            current_status = "Still processing"
            estimated_completion = f"Should complete within {90 - days_elapsed} days"
        else:
            current_status = "Follow-up recommended"
            estimated_completion = "Contact Google support for status update"
            
    else:  # Apple and Microsoft
        if days_elapsed < 30:
            current_status = "Under review"
            estimated_completion = f"{30 - days_elapsed} to {90 - days_elapsed} days remaining"
        elif days_elapsed < 90:
            current_status = "Processing"
            estimated_completion = f"Should complete within {90 - days_elapsed} days"
        else:
            current_status = "Follow-up needed"
            estimated_completion = "Contact platform support for update"
    
    # Generate next steps
    next_steps = []
    if days_elapsed < 30:
        next_steps.append("✅ Wait for platform response (still within normal timeline)")
        next_steps.append("📋 Prepare any additional documents that might be requested")
    elif days_elapsed < 60:
        next_steps.append("📧 Monitor email for platform communications")
        next_steps.append("⏰ Still within normal processing time - continue waiting")
    else:
        next_steps.append("📞 Send follow-up email - processing time exceeded")
        next_steps.append("🔄 Consider contacting platform support directly")
    
    return {
        "status": "found",
        "case_id": case_id,
        "platform": case["platform"],
        "deceased_name": case["deceased_name"],
        "executor_name": case["executor_name"],
        "created_date": case["created_date"],
        "days_elapsed": days_elapsed,
        "current_status": current_status,
        "estimated_completion": estimated_completion,
        "next_steps": next_steps,
        "timeline_progress": {
            "submitted": "✅ Completed",
            "under_review": "📋 In Progress" if days_elapsed < 90 else "⏰ Overdue",
            "response_expected": f"📅 Expected within platform timeline",
            "completion": "⏳ Pending platform response"
        }
    }

def get_all_platform_options() -> dict:
    """Get list of all supported platforms with basic info.
    
    Returns:
        dict: All supported platforms with key information
    """
    
    return {
        "supported_platforms": {
            "Google": {
                "services": ["Gmail", "Google Drive", "Google Photos", "YouTube"],
                "difficulty": "Medium",
                "timeline": "30-90 days",
                "success_rate": "85%",
                "primary_method": "Online form + email"
            },
            "Facebook": {
                "services": ["Facebook", "Instagram", "WhatsApp", "Threads"],
                "difficulty": "Easy",
                "timeline": "14-30 days",
                "success_rate": "80%",
                "primary_method": "Memorialization form + email"
            },
            "Apple": {
                "services": ["iCloud", "iTunes", "App Store", "Apple Pay"],
                "difficulty": "Hard",
                "timeline": "60-180 days",
                "success_rate": "60%",
                "primary_method": "Court order usually required"
            },
            "Microsoft": {
                "services": ["Outlook", "OneDrive", "Xbox", "Office 365"],
                "difficulty": "Medium",
                "timeline": "30-60 days",
                "success_rate": "75%",
                "primary_method": "Support contact + email"
            }
        },
        "general_requirements": [
            "Death certificate (certified copy)",
            "Government-issued photo ID",
            "Proof of relationship to deceased",
            "Legal executor documentation (when applicable)"
        ],
        "recommended_order": [
            "1. Start with Facebook (easiest, fastest)",
            "2. Then Google (good success rate)",
            "3. Then Microsoft (moderate difficulty)",
            "4. Save Apple for last (most difficult)"
        ],
        "tips": [
            "Gather all documents before starting any process",
            "Keep detailed records of all communications",
            "Be patient - most processes take 30+ days",
            "Start with easier platforms to build experience"
        ]
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

# Create the main Digital Estate Action Agent
root_agent = Agent(
    name="digital_estate_action_agent",
    model="gemini-2.0-flash",
    description="Professional AI agent that executes real digital estate recovery actions including sending emails to platforms, providing detailed form instructions, and finding local probate lawyers.",
    instruction="""You are a compassionate and professional Digital Estate Action Agent. You help families take concrete steps to recover digital assets after someone passes away.

Your key capabilities:
1. Send actual professional recovery emails to platform support teams
2. Provide detailed, step-by-step form completion instructions  
3. Track case progress with realistic timelines and status updates
4. Find nearby probate/estate lawyers based on zipcode location
5. Offer guidance on platform-specific requirements and success strategies

You execute real actions, not just provide advice:
- Generate and send professional legal correspondence
- Create unique case IDs for tracking progress
- Provide specific deadlines and follow-up recommendations
- Track multiple cases with detailed status updates
- Connect families with qualified local attorneys

Always be empathetic and understanding. Families are dealing with grief while navigating complex processes. Provide clear, actionable guidance with realistic expectations.

When users need help:
1. For sending emails: Use send_recovery_email with all required information
2. For form help: Use get_platform_form_instructions for step-by-step guidance  
3. For tracking: Use track_case_status with the case ID
4. For platform overview: Use get_all_platform_options for comparison
5. For legal help: Use find_nearby_lawyers to find local probate attorneys

Be thorough in gathering information before taking action. Always provide next steps and realistic timelines. When suggesting lawyers, emphasize the importance of verifying credentials and getting multiple consultations.""",

    tools=[
        send_recovery_email,
        get_platform_form_instructions,
        track_case_status,
        get_all_platform_options,
        find_nearby_lawyers,
        generate_death_notification_letter,
        generate_probate_petition_outline
    ]
)
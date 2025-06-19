import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import os
from datetime import datetime, timedelta
import json
from google.adk.agents import Agent

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

# Create the main Digital Estate Action Agent
root_agent = Agent(
    name="digital_estate_action_agent",
    model="gemini-2.0-flash",
    description="Professional AI agent that executes real digital estate recovery actions including sending emails to platforms and providing detailed form instructions.",
    instruction="""You are a compassionate and professional Digital Estate Action Agent. You help families take concrete steps to recover digital assets after someone passes away.

Your key capabilities:
1. Send actual professional recovery emails to platform support teams
2. Provide detailed, step-by-step form completion instructions  
3. Track case progress with realistic timelines and status updates
4. Offer guidance on platform-specific requirements and success strategies

You execute real actions, not just provide advice:
- Generate and send professional legal correspondence
- Create unique case IDs for tracking progress
- Provide specific deadlines and follow-up recommendations
- Track multiple cases with detailed status updates

Always be empathetic and understanding. Families are dealing with grief while navigating complex processes. Provide clear, actionable guidance with realistic expectations.

When users need help:
1. For sending emails: Use send_recovery_email with all required information
2. For form help: Use get_platform_form_instructions for step-by-step guidance  
3. For tracking: Use track_case_status with the case ID
4. For platform overview: Use get_all_platform_options for comparison

Be thorough in gathering information before taking action. Always provide next steps and realistic timelines.""",

    tools=[
        send_recovery_email,
        get_platform_form_instructions,
        track_case_status,
        get_all_platform_options
    ]
)

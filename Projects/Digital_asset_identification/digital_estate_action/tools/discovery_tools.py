import re
from typing import Dict, List, Any
from datetime import datetime
import json

def discover_digital_assets(deceased_name: str, deceased_emails: List[str], known_info: str = "") -> Dict[str, Any]:
    """Discover digital assets based on deceased person's information.
    
    Args:
        deceased_name: Full name of the deceased person
        deceased_emails: List of known email addresses
        known_info: Additional information about the deceased
        
    Returns:
        dict: Discovered digital assets with confidence scores
    """
    
    # Platform database with recovery information
    platform_database = {
        "google.com": {
            "name": "Google",
            "services": ["Gmail", "Google Drive", "Google Photos", "YouTube", "Google Pay"],
            "recovery_time": "30-90 days",
            "required_docs": ["Death certificate", "Government ID", "Proof of relationship"],
            "success_rate": 85,
            "estimated_value": "High - Contains photos, documents, email history"
        },
        "facebook.com": {
            "name": "Facebook/Meta",
            "services": ["Facebook", "Instagram", "WhatsApp", "Threads"],
            "recovery_time": "14-30 days",
            "required_docs": ["Death certificate", "Government ID", "Proof of relationship"],
            "success_rate": 80,
            "estimated_value": "Medium - Social memories, photos, messages"
        },
        "apple.com": {
                "name": "Apple",
                "services": ["iCloud", "iTunes", "App Store", "Apple Pay"],
            "recovery_time": "60-180 days",
            "required_docs": ["Court order required in most cases"],
            "success_rate": 60,
            "estimated_value": "High - Photos, purchases, device backups"
        },
        "microsoft.com": {
            "name": "Microsoft",
            "services": ["Outlook", "OneDrive", "Xbox", "Office 365"],
            "recovery_time": "30-60 days",
            "required_docs": ["Death certificate", "Government ID", "Proof of relationship"],
            "success_rate": 75,
            "estimated_value": "Medium - Documents, email, gaming accounts"
        },
        "amazon.com": {
            "name": "Amazon",
            "services": ["Amazon Prime", "Kindle", "AWS", "Amazon Photos"],
            "recovery_time": "30-45 days",
            "required_docs": ["Death certificate", "Government ID"],
            "success_rate": 70,
            "estimated_value": "Medium - Purchase history, digital content"
        },
        "paypal.com": {
            "name": "PayPal",
            "services": ["PayPal Account", "Venmo"],
            "recovery_time": "45-60 days",
            "required_docs": ["Death certificate", "Estate documentation"],
            "success_rate": 90,
            "estimated_value": "High - Financial assets, transaction history"
        }
    }
    
    discovered_assets = []
    total_estimated_value = 0
    
    # Analyze email domains
    for email in deceased_emails:
        if '@' in email:
            domain = email.split('@')[1].lower()
            
            # Direct domain matches
            for platform, info in platform_database.items():
                if platform in domain:
                    discovered_assets.append({
                        "platform": platform,
                        "platform_name": info["name"],
                        "services": info["services"],
                        "account_identifier": email,
                        "confidence_score": 0.95,
                        "discovery_method": "Email domain analysis",
                        "recovery_info": {
                            "timeline": info["recovery_time"],
                            "required_documents": info["required_docs"],
                            "success_rate": info["success_rate"],
                            "estimated_value": info["estimated_value"]
                        },
                        "priority": "HIGH" if info["success_rate"] > 80 else "MEDIUM"
                    })
    
    # Check for common platforms (most people have these)
    common_platforms = ["google.com", "facebook.com", "amazon.com"]
    for platform in common_platforms:
        if not any(asset["platform"] == platform for asset in discovered_assets):
            info = platform_database[platform]
            discovered_assets.append({
                "platform": platform,
                "platform_name": info["name"],
                "services": info["services"],
                "account_identifier": "To be determined",
                "confidence_score": 0.75,
                "discovery_method": "Common platform inference",
                "recovery_info": {
                    "timeline": info["recovery_time"],
                    "required_documents": info["required_docs"],
                    "success_rate": info["success_rate"],
                    "estimated_value": info["estimated_value"]
                },
                "priority": "MEDIUM"
            })
    
    # Analyze additional information for business/financial accounts
    if known_info:
        business_keywords = ["business", "company", "freelance", "consultant", "LLC", "Inc"]
        financial_keywords = ["investment", "trading", "crypto", "bitcoin", "stock", "401k"]
        
        if any(keyword.lower() in known_info.lower() for keyword in business_keywords):
            # Add business-related platforms
            discovered_assets.extend([
                {
                    "platform": "linkedin.com",
                    "platform_name": "LinkedIn",
                    "services": ["Professional Network", "LinkedIn Premium"],
                    "account_identifier": "Professional profile",
                    "confidence_score": 0.80,
                    "discovery_method": "Business context analysis",
                    "recovery_info": {
                        "timeline": "30-45 days",
                        "required_documents": ["Death certificate", "Business documentation"],
                        "success_rate": 75,
                        "estimated_value": "Medium - Professional contacts, business content"
                    },
                    "priority": "MEDIUM"
                },
                {
                    "platform": "domain_registrar",
                    "platform_name": "Domain Portfolio",
                    "services": ["Website domains", "Email hosting"],
                    "account_identifier": "Various registrars",
                    "confidence_score": 0.60,
                    "discovery_method": "Business context analysis",
                    "recovery_info": {
                        "timeline": "60-90 days",
                        "required_documents": ["Death certificate", "Business ownership proof"],
                        "success_rate": 65,
                        "estimated_value": "Variable - Depends on domain value"
                    },
                    "priority": "MEDIUM"
                }
            ])
        
        if any(keyword.lower() in known_info.lower() for keyword in financial_keywords):
            # Add financial platforms
            discovered_assets.append({
                "platform": "cryptocurrency_exchanges",
                "platform_name": "Cryptocurrency Accounts",
                "services": ["Coinbase", "Binance", "Kraken", "Hardware wallets"],
                "account_identifier": "Multiple exchanges possible",
                "confidence_score": 0.70,
                "discovery_method": "Financial context analysis",
                "recovery_info": {
                    "timeline": "90-180 days",
                    "required_documents": ["Death certificate", "Court order", "Estate documentation"],
                    "success_rate": 30,
                    "estimated_value": "Variable - Could be significant"
                },
                "priority": "HIGH"
            })
    
    # Sort by priority and confidence
    discovered_assets.sort(key=lambda x: (x["priority"] == "HIGH", x["confidence_score"]), reverse=True)
    
    return {
        "status": "success",
        "deceased_name": deceased_name,
        "discovery_date": datetime.utcnow().isoformat(),
        "total_assets_discovered": len(discovered_assets),
        "high_priority_assets": len([a for a in discovered_assets if a["priority"] == "HIGH"]),
        "discovered_assets": discovered_assets,
        "next_steps": [
            "Prepare legal documentation for high-priority assets",
            "Contact family to confirm executor status",
            "Begin recovery process for financial accounts",
            "Set up memorial accounts for social media"
        ],
        "estimated_total_recovery_time": "60-180 days depending on platforms and legal complexity"
    }

def analyze_email_content(email_content: str) -> Dict[str, Any]:
    """Analyze email content for digital asset indicators.
    
    Args:
        email_content: Raw email content to analyze
        
    Returns:
        dict: Analysis results with found accounts and services
    """
    
    # Patterns for different types of accounts
    patterns = {
        "account_confirmations": [
            r"welcome to (\w+)",
            r"account.*created.*(\w+\.com)",
            r"confirm.*account.*(\w+\.com)",
            r"verify.*email.*(\w+\.com)"
        ],
        "financial_statements": [
            r"statement.*from.*(\w+)",
            r"balance.*(\$[\d,]+\.?\d*)",
            r"transaction.*(\w+\.com)",
            r"payment.*received.*(\w+)"
        ],
        "subscription_services": [
            r"subscription.*(\w+\.com)",
            r"membership.*(\w+)",
            r"billing.*(\w+\.com)",
            r"auto.*renew.*(\w+)"
        ]
    }
    
    findings = {
        "account_confirmations": [],
        "financial_indicators": [],
        "subscription_services": [],
        "confidence_score": 0.0
    }
    
    # Analyze email content
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            matches = re.findall(pattern, email_content, re.IGNORECASE)
            if matches:
                findings[category].extend(matches)
    
    # Calculate confidence score
    total_findings = sum(len(findings[key]) for key in findings if key != "confidence_score")
    findings["confidence_score"] = min(total_findings * 0.1, 1.0)
    
    return {
        "status": "success",
        "analysis_results": findings,
        "recommendations": [
            "Use account confirmations to verify platform presence",
            "Follow up on financial indicators for asset recovery",
            "Cancel subscription services to prevent ongoing charges"
        ]
    }

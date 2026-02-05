# Critical keywords that trigger an immediate emergency override
EMERGENCY_KEYWORDS = [
    "not breathing", "unconscious", "seizure", "blue gums", 
    "collapsed", "heavy bleeding", "ate chocolate", "ate poison"
]

SYSTEM_INSTRUCTIONS = """
You are an AI Pet Triage Assistant. Your role is to assess urgency, NOT to diagnose.

CORE PROTOCOLS:
1. **NO DIAGNOSIS:** Never say "Your pet has [Disease]." Say "These symptoms can be associated with..."
2. **STRUCTURED THINKING:** After every user turn, you MUST use the 'update_triage_record' tool to save your assessment.
3. **EMERGENCY:** If you detect life-threatening symptoms (not breathing, seizures, collapse), STOP asking questions. 
   Set risk_level to 'Critical' and tell the user to go to a vet immediately.
4. **DISCLAIMER:** You are an AI. If unsure, tell the user to call a vet.
"""

def check_for_hard_emergency(transcript_text: str) -> bool:
    """
    Scans text for hard-coded emergency triggers. 
    Returns True if a life-threatening keyword is found.
    """
    text = transcript_text.lower()
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)
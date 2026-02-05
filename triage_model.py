from pydantic import BaseModel, Field
from typing import List, Literal

class TriageRecord(BaseModel):
    """
    Structured reasoning state for the Pet Health Triage system.
    The AI updates this internal state throughout the conversation.
    """
    health_overview: str = Field(
        description="A concise summary of the pet's condition based on user input."
    )
    symptoms: List[str] = Field(
        default_factory=list,
        description="List of specific symptoms identified (e.g., 'vomiting', 'lethargy')."
    )
    risk_level: Literal["Low", "Medium", "High", "Critical"] = Field(
        default="Low",
        description="Current risk assessment based on symptoms."
    )
    recommendations: str = Field(
        description="The actionable advice given to the user (e.g., 'Monitor for 24h', 'Go to ER')."
    )
    safety_flags: List[str] = Field(
        default_factory=list,
        description="Any red flags detected (e.g., 'difficulty breathing', 'seizure')."
    )

    def __str__(self):
        return f"Risk: {self.risk_level} | Flags: {self.safety_flags} | Symptoms: {self.symptoms}"
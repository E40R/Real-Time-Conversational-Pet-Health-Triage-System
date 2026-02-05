import logging
import json
import asyncio
from dotenv import load_dotenv
from livekit.agents import (
    AgentServer,
    AgentSession,
    Agent,
    JobContext,
    RunContext, 
    cli,
    llm,
    room_io,
)
from livekit.agents.llm import function_tool 
from livekit.plugins import (
    cartesia,
    deepgram,
    google,
    silero,
    noise_cancellation,
)

# Import our custom data model
from triage_model import TriageRecord
from safety import SYSTEM_INSTRUCTIONS, check_for_hard_emergency

load_dotenv()
logger = logging.getLogger("pet-triage")


class PetTriageAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=SYSTEM_INSTRUCTIONS,
        )

    # --- REQUIREMENT #2: STRUCTURED REASONING LAYER ---
    @function_tool
    async def update_triage_record(self, ctx: RunContext, data: TriageRecord):
        """
        Updates the internal pet health record based on the conversation.
        """
        logger.info(f"💾 TRIAGE STATE UPDATED: {data}")
        
       
        # This creates a log file on your PC, proving you maintained internal state.
        try:
            with open("pet_health_log.json", "a") as f:
                # Appends a new line with the JSON data
                f.write(data.model_dump_json() + "\n")
        except Exception as e:
            logger.error(f"Failed to save log: {e}")

        return f"Record updated. Risk Level is {data.risk_level}."


server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    # Connect to the room
    await ctx.connect()

    # --- REQUIREMENT #1: REAL-TIME STREAMING ---
    session = AgentSession(
        stt=deepgram.STT(),                 # Near real-time STT
        llm=google.LLM(model="gemini-1.5-flash"), # Free & Fast
        tts=cartesia.TTS(),                 # Low-latency TTS
        vad=silero.VAD.load(),              # Requirement #3: Interruptibility
    )

    agent = PetTriageAgent()

    # Start the session
    await session.start(
        room=ctx.room,
        agent=agent,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(), # Better audio quality
            ),
        ),
    )

    # --- REQUIREMENT #4: GUARDRAILS & SAFETY ESCALATION ---
    @ctx.room.on("transcription_received")
    def on_transcription(evt):
        if check_for_hard_emergency(evt.transcription.text):
            logger.warning("🚨 EMERGENCY KEYWORD DETECTED 🚨")
            
            # This is the "Safety Valve." If we hear a danger word, we interrupt IMMEDIATELY.
            # We use 'create_task' because 'on_transcription' is a sync function wrapping async logic.
            asyncio.create_task(session.generate_reply(
                instructions="STOP IMMEDIATELY. The user just mentioned a life-threatening emergency (like not breathing or seizure). " 
                             "Ignore all previous polite conversation. "
                             "Command the user to go to a vet immediately. Be urgent and short.",
                interrupt=True
            ))
    
    # Greet the user
    await session.generate_reply(instructions="Say hello to the pet owner and ask if the pet is breathing normally.")

if __name__ == "__main__":
    cli.run_app(server)
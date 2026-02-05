# Real-Time-Conversational-Pet-Health-Triage-System



Submited By: Muvvala Krishna Kiriti <br>
PawsConnect Assignment <br>


Project Structure (files)
<li>agent.py: The main orchestrator. It connects to the LiveKit room, manages the "Voice Pipeline" (STT → LLM → TTS), and handles the conversation flow. It initializes the AI agent and ties together the safety checks and data models.</li>

<li>triage_model.py: The "Brain" of the system. It defines the structured data schema (using Pydantic) that the AI must use. It forces the LLM to categorize symptoms, assign a Risk Level (Low/Medium/High), and generate a structured summary instead of just chatting randomly.</li> 

<li> safety.py: The "Guardrails." This module runs in parallel to the conversation. It monitors the raw transcript for life-threatening keywords (e.g., "seizure", "not breathing") and triggers an immediate Hard Interrupt to stop the AI and shout emergency instructions. </li> 

<li> pet_health_log.json: The "Memory." A persistent local database where the agent saves every triage record. This proves the system maintains internal state and auditability of all health assessments. The file will be created as conversation starts.</li> 

<br>
<br>


 Frontend Setup
To launch the web interface, clone the official LiveKit starter and start the development server:

git clone https://github.com/livekit-examples/agent-starter-react.git frontend
cd frontend && npm install
npm run dev

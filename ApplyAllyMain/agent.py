import asyncio
import re # Add this import for regex
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import ToolContext
from google.genai import types # For creating message Content/Parts
from dotenv import load_dotenv
# Assuming shared_data and sub_agents imports are correct
from shared_data import env_variables
from google.adk.artifacts import InMemoryArtifactService
import prompt # This 'prompt' is your agent's instruction
from ApplyAllyMain.sub_agents.search_agent.agent import search_agent
from ApplyAllyMain.sub_agents.job_extraction_agent.agent import job_extraction_agent
from google.adk.events import Event
import tkinter as tk
from tkinter import filedialog
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from io import BytesIO

load_dotenv()


def extract_text_from_pdf():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        print("No file selected.")
        return None

    with open(file_path, 'rb') as f:
        pdf_bytes = f.read()

    # Load bytes into PyPDF2
    pdf_reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    print(f"Extracted {len(text)} characters from the PDF.")

    from openai import OpenAI
    client = OpenAI(
        api_key=env_variables.OPENAI_CLIENTKEY
    )

    if text:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text[:4000]}]  # Trim if large
        )
        message_content = response.choices[0].message.content

    if message_content:
        return message_content
    else:
        print("Please retry.")



resume_agent_team = Agent(
        name="resume_agent", # Give it a new version name
        model=env_variables.GOOGLE_MODEL,
        description="The main coordinator agent. You handle the initial interaction with the user, obtaining relevant information, and passing to specialized sub-agents.",
        instruction=prompt.ROOT_PROMPT,
        sub_agents=[search_agent(), job_extraction_agent()],
        tools=[extract_text_from_pdf]
)


APP_NAME = "resume_agent_system"
USER_ID = "user_1"
SESSION_ID = "session_001"

### WE'LL HAVE TO FIGURE OUT IF WE NEED TO ADJUST THE AWAIT BULLSHIT

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


runner = Runner(
    agent=resume_agent_team,
    app_name=APP_NAME,
    session_service=session_service,
    artifact_service=artifact_service
)

### NOTE THAT THIS ASYNC FUNCTION IS RUNNING AND RETURN THE EVENTS AFTER THEY OCCUR, SO AGENT DOES SOMETHING AND THE RUNNER
### PICKS IT UP AFTER, CHECKS IF IT'S THE FINAL RESPONSE (IN A TURN) AND IF IT IS RETURNS IT. IF WE WANT THE AGENT
### TO DO SOMETHING ON ITS TURN, WE CAN'T ADD FORCED ACTIONS HERE, THEY WOULDN'T HAPPEN WHEN THE AGENT IS ACTING
### BECAUSE IT WOULDN'T KNOW UNTIL AFTER ITS TURN. SO HAS TO BE PART OF THE AGENT DECLARATION
async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query and a file to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_response_text = part.text
                    elif part.file_data:
                        print(f"Agent returned a file: {part.file_data.display_name} ({part.file_data.mime_type})")
            break
        elif event.actions and event.actions.escalate:
            final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    print(f"<<< Agent Response: {final_response_text}")


if __name__ == "__main__":
    async def main():

        user_resume = extract_text_from_pdf()

        initial_state = {
            'user_resume_raw': user_resume
        }

        # Create the session, providing the initial state
        session = await session_service.create_session(
            app_name=APP_NAME,  # Use the consistent app name
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_state,  # <<< Initialize state during creation
        )

        await call_agent_async(query="I need help refining my resume for the following job: https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4240406175",
                               runner=runner,
                               user_id=USER_ID,
                               session_id=SESSION_ID,
                               )


    asyncio.run(main())
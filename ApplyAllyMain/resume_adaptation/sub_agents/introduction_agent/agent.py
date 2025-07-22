import warnings

from google.adk.agents.llm_agent import Agent

from ...shared_data import env_variables
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)


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


job_extraction_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="job_extraction_agent",
        description="You will extract the job role and company from the stored png."
                    "And you will extract 5 relevant qualifications from the stored text description of the job.",
        instruction=prompt.JOB_EXTRACTION_PROMPT
    )




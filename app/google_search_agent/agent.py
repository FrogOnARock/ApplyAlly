# ingestion_agent.py

from google.adk import Agent, Tool
from typing import Dict, Any
import pypdf  # Or another PDF parsing library like pdfminer.six, PyMuPDF, etc.
import io


# --- Define the PDF Processing Tool ---
# This tool will encapsulate the logic for extracting text from a PDF.
class PdfTextExtractorTool(AgentTool):
    """
   A tool to extract plain text from a PDF file.
   """

    def __init__(self):
        super().__init__(
            name="pdf_text_extractor",
            description="Extracts plain text content from a PDF file."
        )

    def invoke(self, pdf_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
      Invokes the tool to extract text from PDF bytes.

      Args:
          pdf_bytes: The raw bytes of the PDF file.
          filename: The name of the PDF file (for context/metadata).

      Returns:
          A dictionary containing the extracted text and potentially other metadata.
      """
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n"  # Add newline for separation

            return {
                "success": True,
                "extracted_text": text_content,
                "filename": filename,
                "num_pages": len(reader.pages)
            }
        except Exception as e:
            # Handle various PDF parsing errors (e.g., corrupted, encrypted)
            return {
                "success": False,
                "error": f"Failed to extract text from PDF: {e}",
                "filename": filename
            }


# --- Define the Ingestion Agent ---
class IngestionAgent(Agent):
    """
   The agent responsible for ingesting PDF files and extracting their content.
   """

    def __init__(self, next_agent: Agent):  # Pass the next agent for hand-off
        super().__init__(
            name="ingestion_agent",
            description="Ingests PDF documents, extracts text, and prepares for further processing.",
            tools=[PdfTextExtractorTool()],  # Register the tool with the agent
            instruction="You are a PDF ingestion specialist. Your primary task is to receive PDF files, extract all readable text, and pass it to the next stage of the document processing pipeline."
        )
        self.next_agent = next_agent

    async def _handle_pdf_ingestion(self, pdf_data: bytes, file_name: str):
        """
      Internal method to handle the ingestion process.
      This would be triggered by an incoming event (e.g., API call, GCS event).
      """
        print(f"Ingestion Agent received PDF: {file_name}")

        # The agent decides to use its tool based on its instruction and input
        # In a real scenario, you might have an LLMAgent that calls the tool
        # but for direct ingestion, we can call it explicitly for clarity.
        extraction_result = await self.tools["pdf_text_extractor"].invoke(pdf_data, file_name)

        if extraction_result["success"]:
            print(f"Successfully extracted text from {file_name}. Passing to Chunking Agent.")
            # Hand-off to the next agent. In ADK, this could be:
            # 1. Directly invoking the next agent's method (if it's a Python object)
            # 2. Sending a message via ADK's messaging capabilities (more robust for distributed systems)
            # 3. Updating shared state for a Workflow Agent to pick up

            # Example: Directly invoking the next agent (conceptual)
            await self.next_agent.process_document_content(
                text_content=extraction_result["extracted_text"],
                filename=extraction_result["filename"],
                metadata={"num_pages": extraction_result["num_pages"]}
            )
        else:
            print(f"Error processing {file_name}: {extraction_result['error']}")
            # Implement error notification or logging here

    # For demonstration, a simple method to simulate receiving a PDF
    async def ingest_pdf_from_path(self, file_path: str):
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        file_name = file_path.split("/")[-1]  # Simple filename extraction
        await self._handle_pdf_ingestion(pdf_bytes, file_name)


# Example usage (within your main ADK application)
if __name__ == "__main__":
    # Dummy Chunking Agent for demonstration
    class DummyChunkingAgent(Agent):
        def __init__(self):
            super().__init__(name="chunking_agent", description="Chunks text.")

        async def process_document_content(self, text_content: str, filename: str, metadata: Dict):
            print(f"\nChunking Agent received text for {filename} (Pages: {metadata['num_pages']}):")
            print(f"First 200 chars: {text_content[:200]}...")
            print("Would now proceed to chunk and embed this text.")


    chunking_agent = DummyChunkingAgent()
    ingestion_agent = IngestionAgent(next_agent=chunking_agent)

    # Simulate ingesting a PDF (you'd replace this with real input)
    # Make sure you have a dummy.pdf file in your current directory for this to run
    print("Attempting to ingest dummy.pdf...")
    import os

    # Create a dummy PDF file for testing if it doesn't exist
    if not os.path.exists("dummy.pdf"):
        # This is a very basic way to create a PDF and might not work for all systems or pypdf versions.
        # It's better to provide a real PDF or mock the file read.
        try:
            from reportlab.pdfgen import canvas

            c = canvas.Canvas("dummy.pdf")
            c.drawString(100, 750, "This is a dummy PDF for testing.")
            c.drawString(100, 730, "It contains some sample text across multiple lines.")
            c.save()
            print("Created a dummy.pdf for testing.")
        except ImportError:
            print(
                "reportlab not found. Please create a dummy.pdf manually or install reportlab for this example to work.")
            print("You can try: pip install reportlab")
            exit()

    ingestion_agent.ingest_pdf_from_path("dummy.pdf")

    # In a full ADK application, you'd integrate this agent into an ADKApp
    # and use ADK's runner or web UI to trigger it.
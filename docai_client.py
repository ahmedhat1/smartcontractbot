import os
from dotenv import load_dotenv
from google.cloud import documentai_v1 as documentai

load_dotenv()  # This loads values from .env

# Now set the credentials
creds_path = os.getenv("GOOGLE_CREDS_PATH")
if not creds_path:
    raise ValueError("GOOGLE_CREDS_PATH not found in .env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

def extract_clauses_from_contract(file_path: str) -> str:
    """
    Uses Google Document AI to extract text from a PDF contract.
    Returns the extracted raw text as a string.
    """
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION", "us")
    processor_id = os.getenv("PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError("PROJECT_ID or PROCESSOR_ID missing in .env")
    
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as file:
        content = file.read()

    raw_document = documentai.RawDocument(content=content, mime_type="application/pdf")

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    result = client.process_document(request=request)
    document_text = result.document.text

    return document_text
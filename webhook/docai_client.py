import os
from google.cloud import documentai_v1beta3 as documentai
from dotenv import load_dotenv
import re

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_CREDS_PATH")

def extract_text_from_doc(clause_type="termination"):
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    processor_id = os.getenv("PROCESSOR_ID")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "sample_contract.pdf")

    with open(file_path, "rb") as f:
        document = {"content": f.read(), "mime_type": "application/pdf"}

        client = documentai.DocumentProcessorServiceClient()
        name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        request = {"name": name, "raw_document": document}
        result = client.process_document(request=request)

        text = result.document.text.lower()
        
        if clause_type == "termination":
            match = re.search(r"(termination[^\.]*\.)", text)
        elif clause_type == "payment":
            match = re.search(r"(payment[^\.]*\.)", text)
        elif clause_type == "confidentiality":
            match = re.search(r"(confidentiality[^\.]*\.)", text)
        else:
            match = None

        if match:
            return f"Found clause: {match.group(1)}"
        else:
            return f"No clause of type '{clause_type}' found."
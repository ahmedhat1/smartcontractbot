from vertexai.preview.generative_models import GenerativeModel, Tool, FunctionDeclaration
from vertexai import init
from docai_client import extract_clauses_from_contract
from functions import extract_clauses

init(project="smartcontractbot", location="us-central1")
model = GenerativeModel("gemini-2.5-flash")


extract_clauses_decl = FunctionDeclaration.from_func(extract_clauses)
tools = Tool(function_declarations=[extract_clauses_decl])

def generate_contract_advice(prompt: str):
    return model.generate_content(prompt, tools=[tools])

__all__ = ["generate_contract_advice", "model", "tool"]
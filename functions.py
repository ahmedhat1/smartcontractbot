import re

def extract_clauses(contract_text: str, clause_type: str) -> str:
    """
    Extracts a clause from the contract text based on a keyword.

    Args:
        contract_text (str): The full text of the contract.
        clause_type (str): The type of clause to extract (e.g., "termination", "liability").

    Returns:
        str: The extracted clause or a message if not found.
    
    """

    pattern = re.compile(rf"(?:\n|^).*?{clause_type}.*?(?:\n|$)", re.IGNORECASE)
    matches = pattern.findall(contract_text)

    return "\n".join(matches) if matches else f"No clause found for '{clause_type}'."

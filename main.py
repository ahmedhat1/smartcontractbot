import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from docai_client import extract_clauses_from_contract
from vertexai import init

init(project="smartcontractbot", location="us-central1")
model = GenerativeModel("gemini-2.5-flash")

#Streamlit UI
st.title("SmartContractBot")
st.write("Ask me any question about your contract.")

user_input = st.text_input("Your question:")
pdf_file = st.file_uploader("Upload a contract PDF (optional)", type=["pdf"])

if st.button("Submit") and user_input:
    contract_text = ""
    if pdf_file:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.read())
        contract_text = extract_clauses_from_contract("temp.pdf")
        
    prompt = user_input
    if contract_text:
        prompt += f"\n\n Here is the contract:n{contract_text}"
    response = model.generate_content(prompt)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Extracted Contract")
        st.text_area("Contract Text", contract_text, height=400)

    with col2:
        st.subheader("💡 Gemini Answer")
        st.markdown(response.text)

        if hasattr(response, "text") and response.text:
            st.markdown(response.text)
        else:
            # fallback: dig into the structure manually
            content = response.candidates[0].content.parts[0].text
            st.markdown(content)

import streamlit as st
import json
from agent_utils import generate_contract_advice, tool
from docai_client import extract_clauses_from_contract
from functions import extract_clauses

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
    with st.spinner("Analyzing the contract..."):
        response = generate_contract_advice(prompt)

    print("Response: ", response)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Extracted Contract")
        st.text_area("Contract Text", contract_text, height=400)

    with col2:
        st.subheader("💡 Gemini Answer")
        
        parts= response.candidates[0].content.parts[0]
        
        if hasattr(parts, "function_call"):
            fn_name= parts.function_call.name
            args = dict(parts.function_call.args)
            
            if fn_name == "extract_clauses":
                result = extract_clauses(**args)
                st.markdown(f"**Function:** `{fn_name}`")
                if result:
                    clause_type = args.get('clause_type', '').capitalize()
                    clause_text = result.strip()

                    if clause_text.lower().startswith(clause_type.lower()):
                        display_text = clause_text
                    else:
                        display_text = f"{clause_type} Clause: {clause_text}"

                    st.markdown("### 📌 Extracted Advice")
                    st.success(display_text)

            elif hasattr(response, "text") and response.text:
                st.markdown(response.text)

            else:
                # fallback: dig into the structure manually
                content = response.candidates[0].content.parts[0].text
                st.markdown(content)

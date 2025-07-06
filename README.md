# SmartContractBot

SmartContractBot is a web-based AI agent that allows users to upload a contract and ask questions about its contents. It uses Google Document AI to extract the full text from the PDF, and Google Gemini models via Vertex AI to generate a detailed response. The application is built using Streamlit for a simple and interactive interface.

## Features

- Upload a PDF contract file
- Extract full contract text using Document AI
- Ask any custom question about the contract
- Get clear, structured answers from Gemini
- Responses formatted in readable markdown style

## Technologies Used

- Python 3.11+
- Streamlit
- Google Vertex AI (Gemini 1.5)
- Google Document AI
- python-dotenv for environment variable handling
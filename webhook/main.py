from flask import Flask, request, jsonify
from docai_client import extract_text_from_doc

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get("fulfillmentInfo", {}).get("tag")

    try:
        if intent == "AskClause":
            response_text = extract_text_from_doc(clause_type="termination")
        else:
            response_text = "I'm not sure how to handle that yet."

        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [response_text]}}
                ]
            }
        })
    
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"Error: {str(e)}"]}}
                ]
            }
        }), 500
if __name__ == '__main__':
    app.run(debug=True)

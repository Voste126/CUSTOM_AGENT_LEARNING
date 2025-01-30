import requests
import streamlit as st
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# API Configurations
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv("LANGFLOW_ID", "").strip()
FLOW_ID = os.getenv("FLOW_ID", "").strip()
APPLICATION_TOKEN = os.getenv("APP_TOKEN", "").strip()
ENDPOINT = "customer"  # The endpoint name of the flow

# Validate environment variables
if not LANGFLOW_ID or not APPLICATION_TOKEN:
    st.error("Missing environment variables: Please check LANGFLOW_ID and APP_TOKEN.")
    st.stop()

def run_flow(message: str) -> dict:
    """Sends a message to the Langflow API and returns the response."""
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}?stream=false"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatOutput-SNVSp": {},
            "ChatInput-bqPPa": {},
            "Prompt-ToZGf": {},
            "Agent-REFuX": {},
            "AstraDB-ESgTx": {},
            "ParseData-oj0EM": {},
            "File-xaSvO": {},
            "SplitText-Awh1z": {},
            "AstraDB-GCmkd": {},
            "Agent-T8EbC": {},
            "Agent-2jlQc": {},
            "AstraDBToolComponent-s3AGY": {},
            "AstraDBToolComponent-UG8h3": {}
        }
    }

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Check if request was successful
        if response.status_code != 200:
            st.error(f"API Error {response.status_code}: {response.text}")
            return {}

        response_json = response.json()
        
        # Debugging: Print API response
        # print("API Response:", json.dumps(response_json, indent=2))

        return response_json

    except requests.RequestException as e:
        st.error(f"Request failed: {str(e)}")
        return {}

def main():
    st.title("Chat Interface")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)

            # Extract and display the AI response safely
            try:
                response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response received.")
                st.markdown(response_text)
            except (IndexError, KeyError, TypeError):
                st.error("Unexpected response format. Please check API response.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

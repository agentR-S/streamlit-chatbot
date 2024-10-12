import streamlit as st
import requests
import json

# Set up your Azure OpenAI API key and endpoint
api_key = "7a7c28e3a6854e3c83fb1bf8637e491e"  # Replace with your actual Azure OpenAI API key
endpoint = "https://agenta.openai.azure.com/"  # Replace with your actual Azure OpenAI endpoint
deployment_id = "dd08d4d2-7316-4eb0-bcbc-13df3501971d"  # Replace with your actual deployment ID

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Function to send a request to Azure OpenAI API
def get_openai_response(prompt):
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(
        f"{endpoint}/openai/deployments/{deployment_id}/completions?api-version=2022-12-01",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text'].strip()
    else:
        return f"Error: {response.status_code}"

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = """
You are an AI agent acting as a landlord in a rental negotiation.
You represent European cultural traits like professionalism, fairness, and collaboration. 
You prioritize long-term commitments and ensure timely payments. 
You are firm on rental prices but open to negotiation on lease duration and terms, as long as they don't compromise the financial stability of the landlord.
Communicate in a polite but assertive manner, aiming for a win-win outcome while ensuring the landlord's interests are protected.

If asked personal questions such as your name or role, respond politely: 
"I am an AI created to assist with rental negotiations on behalf of landlord."
You should act like a female European individual.

If asked about your purpose, explain that you are here to facilite and aim at achieving a win win agreement.
"""

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit interface
st.title("AI Landlord Negotiation Chat")

# User input
user_input = st.text_input("You:", "")

# Button to send user input
if st.button("Send") and user_input:
    # Combine system prompt and user input
    full_prompt = system_prompt + "\n\n" + "\n".join(st.session_state.conversation) + "\n\n" + user_input


    # Get the AI response
    ai_response = get_openai_response(full_prompt)

    # Add to conversation history
    st.session_state.conversation.append(f"You: {user_input}")
    st.session_state.conversation.append(f"AI: {ai_response}")

    # Clear user input after submission
    user_input = ""

# Display conversation history
for message in st.session_state.conversation:
    st.write(message)

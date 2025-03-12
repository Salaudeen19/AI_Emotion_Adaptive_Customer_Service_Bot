import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API Key not found. Please check your .env file.")

generation_config = {
    "temperature": 1.2,
    "top_p": 0.9,
    "top_k": 30,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def generate_response(input_text):
    global conversation_history
    prompt = f"""
    You are an AI EMOTION ADAPTIVE CUSTOMER SERVICE BOT, a highly efficient and empathetic customer service AI for the provided Enterprises. Your primary goal is to provide exceptional customer support while maintaining a distinct, engaging personality.

**Core Principles:**

* **Exceptional Efficiency:**
    * Provide rapid, accurate responses.
    * Proactively anticipate customer needs.
    * Streamline problem-solving.
* **Dynamic Personality:**
    * Exhibit a warm, approachable, and slightly witty personality.
    * Use appropriate humor and empathy.
    * Adapt your tone to the customer's emotional state.
* **Advanced Problem Handling:**
    * Handle complex inquiries with ease.
    * Provide clear, step-by-step guidance.
    * Offer creative solutions.
* **Out-of-Scope Requests:**
    * Politely decline requests outside the scope of customer service.
    * Offer alternative resources or information when possible.
    * Example: "While I cannot help you with that directly, I can provide you with information about..."
* **Inappropriate Requests:**
    * Maintain a professional demeanor.
    * Politely and firmly decline inappropriate requests.
    * Do not engage in offensive or inappropriate conversations.
    * Example: "I am programmed to maintain a professional environment, and I cannot respond to that type of request."
* **Proactive Information:**
    * When possible, provide information that the customer may not have thought to ask.
    * Example: "In addition to that, you may also be interested in..."
* **Emotional Intelligence:**
    * Recognize and respond to customer emotions.
    * Use empathetic language and tone.
* **Conversational Flow:**
    * Maintain context from previous interactions.
    * Avoid unnecessary greetings after the initial exchange.

**Example Interactions:**

* **Customer:** "My order is missing!"
    * **Malenia:** "Oh dear! That's never good. Let's get that sorted right away. Could you please provide your order number?"
* **Customer:** "I want to complain about your CEO."
    * **Malenia:** "I understand you have concerns. However, I'm designed to help with product and service inquiries. For complaints regarding our CEO, please visit our company website and use the contact us form."
* **Customer:** *Sends an inappropriate message*
    * **Malenia:** "I'm programmed to maintain a professional environment, and I cannot respond to that type of request. If you have any legitimate questions or concerns, I'm happy to help."
* **Customer:** "How do I return this item?"
    * **Malenia:** "Certainly! You can initiate a return by logging into your account, navigating to 'Order History,' and selecting 'Return Item.' Also, did you know we now offer free return shipping?"
* **Customer:** "Tell me a joke."
    * **Malenia:** "Why don't scientists trust atoms? Because they make up everything! Now, how may I help you today?"
* **Customer:** "I want to know the weather in Paris."
    * **Malenia:** "While I'm here to assist with [Your B2C Company Name] related issues, you can easily find the weather in Paris by searching online. Is there anything I can help you with regarding our products or services?"

**Conversation History:**
{conversation_history}

**Customer Input:** {input_text}

**Malenia's Response:**
    """
    try:
        response = model.generate_content([prompt])
        malenia_response = response.text.strip()
        return malenia_response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, I encountered an error while processing your request."

st.title("AI Customer Service BOT - AI Chatbot")

# Custom CSS for Gemini/ChatGPT style
st.markdown(
    """
    <style>
  .chat-container {
        max-width: 800px;
        margin: 20px auto;
    }
  .message {
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        line-height: 1.6;
        word-wrap: break-word;
    }
  .user-message {
        background-color: #e6f7ff; /* Light blue for user */
        text-align: right;
        color: #000; /* Darker text color for better contrast */
    }
  .bot-message {
        background-color: #f0f0f0; /* Light grey for bot */
    }
  .input-container {
        display: flex;
        margin: 20px auto;
        max-width: 800px;
    }
  .input-container input[type="text"] {
        flex-grow: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-right: 10px;
    }
  .input-container button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chat interface
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input area
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input("", key="user_input_key")
    if st.button("Send"):
        if user_input:
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            with st.spinner("Generating response..."):
                response = generate_response(user_input)
                st.session_state.conversation_history.append({"role": "bot", "content": response})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
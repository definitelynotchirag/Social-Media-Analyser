# import streamlit as st
# import requests
# import json

# import os
# from dotenv import load_dotenv

# # Load the .env file
# load_dotenv(".env")

# BASE_API_URL = os.getenv("BASE_API_URL")
# LANGFLOW_ID = os.getenv("LANGFLOW_ID")
# FLOW_ID = os.getenv("FLOW_ID")
# APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
# ENDPOINT = ""


# # Constants
# TWEAKS = {
#     "ChatInput-JNsU0": {},
#     "Agent-IFmd7": {},
#     "ChatOutput-az21R": {},
#     "AstraDB-eMAF7": {},
#     "CSVtoData-CVwUC": {},
#     "Prompt-YAaiq": {},
#     "MistalAIEmbeddings-WDkfv": {},
#     "AstraDBToolComponent-im9Zs": {}
# }

# # Helper function to call Langflow API
# def run_flow(message: str, endpoint: str = FLOW_ID, tweaks: dict = None):
#     api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
#     payload = {
#         "input_value": message,
#         "output_type": "chat",
#         "input_type": "chat",
#     }
#     if tweaks:
#         payload["tweaks"] = tweaks
#     headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
#     try:
#         response = requests.post(api_url, json=payload, headers=headers)
#         if response.status_code != 200:
#             st.error(f"API returned an error: {response.status_code} - {response.text}")
#             return None
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Request failed: {e}")
#         return None
#     except json.JSONDecodeError:
#         st.error("Invalid response format received from the API.")
#         st.write(f"Raw Response: {response.text}")
#         return None

# # Streamlit app
# st.title("Social Media Analytics")
# st.sidebar.header("Settings")
# endpoint = st.sidebar.text_input("Endpoint (Optional)", ENDPOINT or FLOW_ID)
# message = st.text_area("Input Message", placeholder="Enter your message here...")

# if st.button("Run Flow"):
#     if not message.strip():
#         st.error("Please enter a message to proceed.")
#     else:
#         with st.spinner("Processing..."):
#             try:
#                 tweaks_json = TWEAKS  # Adjust tweaks if needed
#                 response = run_flow(message, endpoint=endpoint, tweaks=tweaks_json)
#                 st.success("Response received:")
#                 st.write(response["outputs"][0]["outputs"][0]["results"]["message"]["text"])
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")


import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load the .env file
load_dotenv(".env")

# Custom CSS for styling

hide_decoration_bar_style = ''' <style> header {visibility: hidden;} </style> ''' 
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True) 

st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Custom title styling */
    # .custom-title {
    #     background: linear-gradient(45deg,rgb(11, 9, 15),rgb(11, 11, 19));
    #     padding: 0.2rem;
    #     border-radius: 10px;
    #     color: white;
    #     text-align: center;
    #     # margin-bottom: 2rem;
    # }
    
    /* Chat message container */
    .stChatMessage {
        background-color:rgb(17, 17, 17);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        border: 2px solid #2193b0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f7f7f7;
    }
    
    /* Custom button styling */
    # .stButton>button {
    #     border-radius: 20px;
    #     background: linear-gradient(45deg, #2193b0, #6dd5ed);
    #     color: white;
    #     border: none;
    #     padding: 0.5rem 2rem;
    #     transition: all 0.3s ease;
    # }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Custom spinner */
    .stSpinner > div {
        border-top-color: #2193b0 !important;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Environment variables
BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = ""

# Constants
TWEAKS = {
    "ChatInput-JNsU0": {},
    "Agent-IFmd7": {},
    "ChatOutput-az21R": {},
    "AstraDB-eMAF7": {},
    "CSVtoData-CVwUC": {},
    "Prompt-YAaiq": {},
    "MistalAIEmbeddings-WDkfv": {},
    "AstraDBToolComponent-im9Zs": {}
}


def run_flow(message: str, endpoint: str = FLOW_ID, tweaks: dict = None):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks
    
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code != 200:
            st.error(f"API returned an error: {response.status_code} - {response.text}")
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Invalid response format received from the API.")
        st.write(f"Raw Response: {response.text}")
        return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# App layout
st.markdown('<div class="custom-title"><h1>Social Media Analytics Assistant</h1></div>', unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    endpoint = st.text_input("🔌 Endpoint", ENDPOINT or FLOW_ID)
    
    # Add time and date display
    st.markdown("### 📅 Session Info")
    st.write(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.rerun()

# Welcome message
if not st.session_state.chat_started:
    st.markdown("""
    ### Welcome to Social Media Analytics! 👋
    
    I can help you analyze:
    - 📊 Social media metrics
    - 📈 Engagement trends
    - 🎯 Audience insights
    - 💡 Content performance
    
    Just type your question below to get started!
    """)
    st.session_state.chat_started = True

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your social media analytics..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing your request..."):
            try:
                response = run_flow(prompt, endpoint=endpoint, tweaks=TWEAKS)
                if response and "outputs" in response:
                    assistant_response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    # Add typing effect
                    message_placeholder = st.empty()
                    for i in range(len(assistant_response) + 1):
                        message_placeholder.markdown(assistant_response[:i] + "▌")
                        time.sleep(0.01)
                    message_placeholder.markdown(assistant_response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    st.error("😕 I couldn't process your request. Please try again.")
            except Exception as e:
                st.error(f"🚫 An error occurred: {str(e)}")

# Footer
# st.markdown("""
# <div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: #f0f2f6; padding: 1rem; text-align: center; font-size: 0.8rem;'>
#     Made with ❤️ by Your Analytics Team
# </div>
# """, unsafe_allow_html=True)







# import streamlit as st
# import requests
# import json
# import os
# from dotenv import load_dotenv
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd

# # Load environment variables
# load_dotenv(".env")
# BASE_API_URL = os.getenv("BASE_API_URL")
# LANGFLOW_ID = os.getenv("LANGFLOW_ID")
# FLOW_ID = os.getenv("FLOW_ID")
# APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
# ENDPOINT = ""

# # Constants
# TWEAKS = {
#     "ChatInput-JNsU0": {},
#     "Agent-IFmd7": {},
#     "ChatOutput-az21R": {},
#     "AstraDB-eMAF7": {},
#     "CSVtoData-CVwUC": {},
#     "Prompt-YAaiq": {},
#     "MistalAIEmbeddings-WDkfv": {},
#     "AstraDBToolComponent-im9Zs": {}
# }

# def parse_metrics(text):
#     """Parse metrics from the text response"""
#     metrics = {}
    
#     if "METRICS_START" in text and "METRICS_END" in text:
#         # Extract metrics section
#         metrics_text = text.split("METRICS_START")[1].split("METRICS_END")[0]
        
#         # Parse Bar Graph Metrics
#         if "Bar Graph Metrics:" in metrics_text:
#             bar_data = metrics_text.split("Bar Graph Metrics:")[1].split("\n")[1]
#             title, data = bar_data.split("|")
#             data_pairs = [pair.split(":") for pair in data.split(",")]
#             metrics['bar'] = {
#                 'title': title,
#                 'labels': [pair[0] for pair in data_pairs],
#                 'values': [float(pair[1]) for pair in data_pairs]
#             }
        
#         # Parse Line Graph Metrics
#         if "Line Graph Metrics:" in metrics_text:
#             line_data = metrics_text.split("Line Graph Metrics:")[1].split("\n")[1]
#             title, data = line_data.split("|")
#             data_pairs = [pair.split(":") for pair in data.split(",")]
#             metrics['line'] = {
#                 'title': title,
#                 'labels': [pair[0] for pair in data_pairs],
#                 'values': [float(pair[1]) for pair in data_pairs]
#             }
        
#         # Parse Pie Chart Metrics
#         if "Pie Chart Metrics:" in metrics_text:
#             pie_data = metrics_text.split("Pie Chart Metrics:")[1].split("\n")[1]
#             title, data = pie_data.split("|")
#             data_pairs = [pair.split(":") for pair in data.split(",")]
#             metrics['pie'] = {
#                 'title': title,
#                 'labels': [pair[0] for pair in data_pairs],
#                 'values': [float(pair[1]) for pair in data_pairs]
#             }
    
#     return metrics

# def create_visualizations(metrics):
#     """Create Plotly visualizations from parsed metrics"""
#     figs = {}
    
#     # Create Bar Chart
#     if 'bar' in metrics:
#         fig_bar = px.bar(
#             x=metrics['bar']['labels'],
#             y=metrics['bar']['values'],
#             title=metrics['bar']['title'],
#             labels={'x': 'Categories', 'y': 'Value'}
#         )
#         figs['bar'] = fig_bar
    
#     # Create Line Chart
#     if 'line' in metrics:
#         fig_line = px.line(
#             x=metrics['line']['labels'],
#             y=metrics['line']['values'],
#             title=metrics['line']['title'],
#             labels={'x': 'Time Period', 'y': 'Value'}
#         )
#         figs['line'] = fig_line
    
#     # Create Pie Chart
#     if 'pie' in metrics:
#         fig_pie = px.pie(
#             values=metrics['pie']['values'],
#             names=metrics['pie']['labels'],
#             title=metrics['pie']['title']
#         )
#         figs['pie'] = fig_pie
    
#     return figs

# def run_flow(message: str, endpoint: str = FLOW_ID, tweaks: dict = None):
#     api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
#     payload = {
#         "input_value": message,
#         "output_type": "chat",
#         "input_type": "chat",
#     }
#     if tweaks:
#         payload["tweaks"] = tweaks
    
#     headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
#     try:
#         response = requests.post(api_url, json=payload, headers=headers)
#         if response.status_code != 200:
#             st.error(f"API returned an error: {response.status_code} - {response.text}")
#             return None
#         return response.json()
#     except Exception as e:
#         st.error(f"Request failed: {e}")
#         return None

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # App layout
# st.title("Social Media Analytics Dashboard")

# # Create two columns
# col1, col2 = st.columns([0.4, 0.6])

# with col1:
#     st.subheader("Chat")
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
            
#             # If it's an assistant message, try to create visualizations
#             if message["role"] == "assistant":
#                 metrics = parse_metrics(message["content"])
#                 if metrics:
#                     st.session_state.latest_metrics = metrics

#     # Chat input
#     if prompt := st.chat_input("What would you like to analyze?"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             with st.spinner("Analyzing..."):
#                 try:
#                     response = run_flow(prompt, endpoint=ENDPOINT, tweaks=TWEAKS)
#                     if response and "outputs" in response:
#                         assistant_response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
#                         st.markdown(assistant_response)
#                         st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                        
#                         # Generate new visualizations
#                         metrics = parse_metrics(assistant_response)
#                         if metrics:
#                             st.session_state.latest_metrics = metrics
                            
#                 except Exception as e:
#                     st.error(f"An error occurred: {str(e)}")

# with col2:
#     st.subheader("Visualizations")
    
#     if hasattr(st.session_state, 'latest_metrics'):
#         figs = create_visualizations(st.session_state.latest_metrics)
        
#         # Display visualizations
#         for chart_type, fig in figs.items():
#             st.plotly_chart(fig, use_container_width=True)

# # Sidebar
# with st.sidebar:
#     st.header("Settings")
#     endpoint = st.text_input("Endpoint (Optional)", ENDPOINT or FLOW_ID)
    
#     if st.button("Clear Chat History"):
#         st.session_state.messages = []
#         if hasattr(st.session_state, 'latest_metrics'):
#             del st.session_state.latest_metrics
#         st.rerun()
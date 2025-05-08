import streamlit as st
import base64
from datetime import datetime
import time
import sys
import logging
import requests
import json
import subprocess
import shlex
import os
import psutil

from mental_health_utils import (
    get_random_affirmation,
    get_coping_strategies,
    get_random_mood_booster,
    get_mindfulness_exercise,
    generate_mental_health_prompt,
    CRISIS_RESOURCES
)
from ui_components import (
    apply_custom_css,
    display_chat_message,
    display_resource_card,
    display_support_card,
    create_sidebar
)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths and environment
USERPROFILE = os.path.expanduser('~')
OLLAMA_PATH = os.path.join(USERPROFILE, "AppData", "Local", "Programs", "Ollama", "ollama.exe")
OLLAMA_ENV = {
    "PATH": os.environ["PATH"],
    "USERPROFILE": USERPROFILE,
    "HOME": USERPROFILE,
    "APPDATA": os.path.join(USERPROFILE, "AppData", "Roaming"),
    "LOCALAPPDATA": os.path.join(USERPROFILE, "AppData", "Local"),
    "TEMP": os.environ.get("TEMP", os.path.join(USERPROFILE, "AppData", "Local", "Temp")),
    "TMP": os.environ.get("TMP", os.path.join(USERPROFILE, "AppData", "Local", "Temp"))
}

def is_ollama_running():
    """Check if Ollama process is running"""
    for proc in psutil.process_iter(['name']):
        try:
            if 'ollama' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def check_ollama_api():
    """Check if Ollama API is responding"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else response.text
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Ollama API"
    except Exception as e:
        return False, str(e)

def get_ai_response(user_input, conversation_history):
    """Get AI response using Ollama API"""
    try:
        # Prepare the request
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.1:8b",
            "prompt": user_input,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500,
                "top_k": 40,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        logger.info(f"Attempting to get AI response...")
        logger.info(f"Sending request to Ollama: {json.dumps(payload, indent=2)}")
        
        # Make the request with a shorter timeout
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if 'response' in result:
                    logger.info("Successfully received response from Ollama")
                    return result['response'], None
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return None, "Invalid response format from Ollama"
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                logger.error(f"Raw response: {response.text}")
                return None, "Error parsing AI response"
        else:
            logger.error(f"API request failed: {response.status_code} - {response.text}")
            return None, f"API request failed: {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error("Request timed out after 15 seconds")
        return None, "The response took too long. Please try again with a shorter message."
    except requests.exceptions.ConnectionError:
        logger.error("Connection error - Ollama API not reachable")
        return None, "Could not connect to Ollama API. Please make sure Ollama is running."
    except Exception as e:
        logger.error(f"Unexpected error in get_ai_response: {str(e)}")
        return None, f"Error: {str(e)}"

# Page configuration
st.set_page_config(
    page_title="Mental Health Support Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []
if 'mindfulness_sessions' not in st.session_state:
    st.session_state.mindfulness_sessions = 0
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# Create sidebar
create_sidebar()

# Main content
st.title("Mental Health Support Chat")

# Check Ollama status
ollama_process = is_ollama_running()
api_status, api_response = check_ollama_api()

if ollama_process:
    st.success("✓ Ollama process is running")
else:
    st.error("✗ Ollama process is not running")
    st.markdown("""
    Please start Ollama:
    1. Open a new terminal
    2. Run `ollama serve`
    3. Wait for it to start
    4. Refresh this page
    """)
    st.stop()

if api_status:
    st.success("✓ Ollama API is responding")
else:
    st.error("✗ Ollama API is not responding")
    st.markdown("""
    The Ollama process is running but the API is not responding. Please:
    1. Close any running Ollama processes
    2. Open a new terminal
    3. Run `ollama serve`
    4. Wait for it to start
    5. Refresh this page
    """)
    st.stop()

st.markdown("Welcome to CalmConnect! I'm here to provide support and guidance for your mental wellbeing. Remember, I'm here to listen and help, but I'm not a replacement for professional mental health care.")

# Display random mood booster
st.info(get_random_mood_booster())

# Chat interface
user_message = st.text_input(
    "How can I help you today?",
    key="user_input",
    help="Share your thoughts, feelings, or concerns. I'm here to listen and support you.",
    placeholder="Express yourself freely... I'm here to listen"
)

# Process user input
if user_message:
    try:
        with st.spinner("Processing your message... (this may take up to 15 seconds)"):
            # Get AI response
            ai_response, error = get_ai_response(user_message, st.session_state.conversation_history)
            
            if error:
                st.error(f"Error: {error}")
                st.markdown("""
                If you're seeing this error repeatedly, please:
                1. Make sure Ollama is running (`ollama serve`)
                2. Try sending a shorter message
                3. Refresh the page and try again
                """)
            else:
                # Update conversation history
                st.session_state.conversation_history.append({"role": "user", "content": user_message})
                st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
                st.rerun()
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        logger.error(f"Error in message processing: {str(e)}")

# Display conversation
if st.session_state.conversation_history:
    st.markdown("### Our Conversation")
    for msg in st.session_state.conversation_history:
        display_chat_message(msg['role'], msg['content'])

# Wellness Tools Section
st.markdown("### Wellness Tools")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Get a Positive Affirmation"):
        affirmation = get_random_affirmation()
        display_support_card("Daily Affirmation", affirmation)

with col2:
    if st.button("Try a Mindfulness Exercise"):
        exercise = get_mindfulness_exercise()
        display_support_card(
            f"{exercise['name']} ({exercise['duration']})",
            exercise['instructions']
        )
        st.session_state.mindfulness_sessions += 1

with col3:
    if st.button("Coping Strategies"):
        strategies = get_coping_strategies('stress')
        display_support_card(
            "Helpful Coping Strategies",
            "\n".join(f"• {strategy}" for strategy in strategies)
        )

# Progress Tracking
if st.session_state.mindfulness_sessions > 0:
    st.markdown("### Your Wellness Journey")
    st.markdown(f"You've completed {st.session_state.mindfulness_sessions} mindfulness exercises!")

# Emergency Support
st.markdown("### Need Immediate Support?")
cols = st.columns([2, 1])
with cols[0]:
    st.markdown("""
        If you're experiencing a mental health emergency or having thoughts of self-harm,
        please reach out for professional help immediately.
    """)
with cols[1]:
    if st.button("View Emergency Contacts", type="primary"):
        for service, number in CRISIS_RESOURCES.items():
            display_resource_card(service, number)

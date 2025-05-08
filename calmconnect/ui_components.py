import streamlit as st
import time

def apply_custom_css():
    """Apply custom CSS styling for the mental health interface"""
    st.markdown("""
        <style>
        .main {
            background-color: #1E1E1E;
            color: white;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #2D2D2D !important;
            color: white !important;
            border: 1px solid #4D4D4D !important;
            padding: 0.75rem !important;
            border-radius: 8px !important;
            font-size: 16px !important;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            background-color: #2D2D2D;
        }
        .chat-message.user {
            background-color: #2D3748;
            margin-left: 20%;
            border-left: 4px solid #4CAF50;
        }
        .chat-message.assistant {
            background-color: #1A2234;
            margin-right: 20%;
            border-left: 4px solid #2196F3;
        }
        .support-card {
            background-color: #2D2D2D;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border-left: 4px solid #9C27B0;
        }
        .resource-card {
            background-color: #2D2D2D;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #FF9800;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            padding: 0.75rem;
            background-color: #4CAF50;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .emergency-button > button {
            background-color: #f44336;
        }
        .emergency-button > button:hover {
            background-color: #d32f2f;
        }
        .mood-tracker {
            background-color: #2D2D2D;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        h1, h2, h3 {
            color: #4CAF50 !important;
            font-weight: 600 !important;
        }
        .stProgress > div > div > div {
            background-color: #4CAF50 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def display_chat_message(role, content):
    """Display a chat message with proper styling"""
    st.markdown(f"""
        <div class="chat-message {role}">
            <strong>{'You' if role == 'user' else 'CalmConnect'}:</strong>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

def display_resource_card(title, content):
    """Display a resource card with proper styling"""
    st.markdown(f"""
        <div class="resource-card">
            <strong>{title}</strong>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

def display_support_card(title, content):
    """Display a support information card"""
    st.markdown(f"""
        <div class="support-card">
            <h4>{title}</h4>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with mental health resources"""
    with st.sidebar:
        st.title("CalmConnect")
        st.markdown("---")
        
        # Emergency Resources Section
        st.subheader("Emergency Resources")
        if st.button("Show Emergency Contacts", key="emergency"):
            for service, number in CRISIS_RESOURCES.items():
                display_resource_card(service, number)
        
        st.markdown("---")
        
        # Mood Tracking
        st.subheader("Mood Tracker")
        mood = st.slider("How are you feeling today?", 1, 10, 5)
        if st.button("Log Mood"):
            st.session_state.setdefault('mood_history', []).append(mood)
            st.success("Mood logged successfully!")
            
        # Show mood history if available
        if 'mood_history' in st.session_state and st.session_state['mood_history']:
            st.line_chart(st.session_state['mood_history'])
        
        st.markdown("---")
        
        # Quick Access Tools
        st.subheader("Quick Tools")
        if st.button("Breathing Exercise"):
            st.markdown("### 4-7-8 Breathing")
            for _ in range(3):
                st.info("Breathe in... (4s)")
                time.sleep(4)
                st.info("Hold... (7s)")
                time.sleep(7)
                st.info("Breathe out... (8s)")
                time.sleep(8) 
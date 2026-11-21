"""
SpamGuard AI - Main Application
Intelligent Email, SMS & Phishing Protection
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.ui_components import apply_glassmorphism_style, show_header
from utils.database import DetectionDatabase

# Page configuration
st.set_page_config(
    page_title="SpamGuard AI - Intelligent Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_glassmorphism_style()

# Initialize database
if 'db' not in st.session_state:
    st.session_state.db = DetectionDatabase()

# Initialize message detector (lazy loading)
if 'message_detector' not in st.session_state:
    st.session_state.message_detector = None

# Sidebar navigation
st.sidebar.markdown("# 🛡️ SpamGuard AI")
st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📧 Email Detection",
        "📱 SMS Detection",
        "🔗 URL Scanner",
        "📊 Bulk Detection",
        "📜 Detection History",
        "📈 Analytics",
        "🎯 Model Performance",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")

try:
    stats = st.session_state.db.get_statistics()
    st.sidebar.metric("Total Scans", stats['total_detections'])
    st.sidebar.metric("Spam Detected", stats['spam_count'])
    st.sidebar.metric("URLs Analyzed", stats['url_scans'])
except Exception as e:
    st.sidebar.info("No statistics available yet")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px; color: #b8b8ff;'>
    <small>Powered by Machine Learning<br>
    Built with Python & Streamlit</small>
</div>
""", unsafe_allow_html=True)

# Page routing
if page == "🏠 Dashboard":
    from pages import dashboard
    dashboard.show()

elif page == "📧 Email Detection":
    from pages import email_detection
    email_detection.show()

elif page == "📱 SMS Detection":
    from pages import sms_detection
    sms_detection.show()

elif page == "🔗 URL Scanner":
    from pages import url_scanner
    url_scanner.show()

elif page == "📊 Bulk Detection":
    from pages import bulk_detection
    bulk_detection.show()

elif page == "📜 Detection History":
    from pages import history
    history.show()

elif page == "📈 Analytics":
    from pages import analytics
    analytics.show()

elif page == "🎯 Model Performance":
    from pages import model_performance
    model_performance.show()

elif page == "ℹ️ About":
    from pages import about
    about.show()

"""
UI components and styling for SpamGuard AI
"""
import streamlit as st


def apply_glassmorphism_style():
    """Apply glassmorphism CSS styling to the app"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Title Styling */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(138, 43, 226, 0.5);
    }
    
    h2 {
        color: #e0e0ff;
        font-weight: 600;
        margin-top: 30px;
    }
    
    h3 {
        color: #c8c8ff;
        font-weight: 500;
    }
    
    /* Text Colors */
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(138, 43, 226, 0.6) !important;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Success Message */
    .stSuccess {
        background: rgba(76, 175, 80, 0.15) !important;
        border: 1px solid rgba(76, 175, 80, 0.3) !important;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Error Message */
    .stError, .stAlert {
        background: rgba(244, 67, 54, 0.15) !important;
        border: 1px solid rgba(244, 67, 54, 0.3) !important;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Warning Message */
    .stWarning {
        background: rgba(255, 152, 0, 0.15) !important;
        border: 1px solid rgba(255, 152, 0, 0.3) !important;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Info Message */
    .stInfo {
        background: rgba(33, 150, 243, 0.15) !important;
        border: 1px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #c8c8ff;
    }
    
    /* Data Frame */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #ffffff !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #c8c8ff;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(138, 43, 226, 0.3);
        color: #ffffff;
    }
    
    /* Sidebar Navigation */
    .sidebar-nav {
        padding: 10px;
    }
    
    .nav-item {
        padding: 12px 20px;
        margin: 5px 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #e0e0e0;
    }
    
    .nav-item:hover {
        background: rgba(138, 43, 226, 0.2);
        transform: translateX(5px);
    }
    
    /* Custom Card Classes */
    .risk-high {
        background: rgba(244, 67, 54, 0.15);
        border: 2px solid rgba(244, 67, 54, 0.5);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .risk-suspicious {
        background: rgba(255, 152, 0, 0.15);
        border: 2px solid rgba(255, 152, 0, 0.5);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .risk-low {
        background: rgba(255, 235, 59, 0.15);
        border: 2px solid rgba(255, 235, 59, 0.5);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .risk-safe {
        background: rgba(76, 175, 80, 0.15);
        border: 2px solid rgba(76, 175, 80, 0.5);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(138, 43, 226, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(138, 43, 226, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)


def show_header(title: str, subtitle: str = None):
    """Display app header with title and subtitle"""
    st.markdown(f"<h1>🛡️ {title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #b8b8ff; margin-top: -10px;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)


def show_result_card(prediction: str, confidence: float = None, risk_score: int = None):
    """Display result in a styled card"""
    
    if prediction in ['SPAM', 'HIGH RISK']:
        card_class = 'risk-high'
        icon = '🚨'
        color = '#f44336'
    elif prediction in ['SUSPICIOUS']:
        card_class = 'risk-suspicious'
        icon = '⚠️'
        color = '#ff9800'
    elif prediction in ['LOW RISK']:
        card_class = 'risk-low'
        icon = '⚡'
        color = '#ffeb3b'
    elif prediction in ['SAFE', 'BENIGN', 'LEGITIMATE']:
        card_class = 'risk-safe'
        icon = '✅'
        color = '#4caf50'
    else:
        card_class = 'glass-card'
        icon = '❓'
        color = '#9e9e9e'
    
    score_text = ""
    if confidence is not None:
        score_text = f"<p style='font-size: 1.5rem; margin: 10px 0;'>Confidence: <strong>{confidence*100:.1f}%</strong></p>"
    elif risk_score is not None:
        score_text = f"<p style='font-size: 1.5rem; margin: 10px 0;'>Risk Score: <strong>{risk_score}/100</strong></p>"
    
    st.markdown(f"""
    <div class='{card_class}'>
        <div style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>{icon}</div>
            <h2 style='color: {color}; margin: 10px 0; text-shadow: 0 0 10px {color}50;'>{prediction}</h2>
            {score_text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_keyword_highlights(keywords: list, categories: dict):
    """Display highlighted suspicious keywords"""
    if not keywords:
        return
    
    st.markdown("### 🔍 Suspicious Keywords Detected")
    
    # Show by category
    for category, words in categories.items():
        category_display = category.replace('_', ' ').title()
        st.markdown(f"**{category_display}:**")
        
        # Create colored badges
        badges = []
        for word in words[:10]:  # Limit to 10 per category
            badges.append(f'<span style="background: rgba(244, 67, 54, 0.2); padding: 5px 12px; border-radius: 15px; margin: 3px; display: inline-block; border: 1px solid rgba(244, 67, 54, 0.4);">{word}</span>')
        
        st.markdown(' '.join(badges), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def show_url_results(url_results: list):
    """Display URL analysis results"""
    if not url_results:
        return
    
    st.markdown("### 🔗 URL Analysis")
    
    for result in url_results:
        risk_level = result.get('risk_level', 'UNKNOWN')
        risk_score = result.get('risk_score', 0)
        url = result.get('url', '')
        reasons = result.get('reasons', [])
        
        # Determine color
        if risk_level == 'HIGH RISK':
            color = '#f44336'
            icon = '🚨'
        elif risk_level == 'SUSPICIOUS':
            color = '#ff9800'
            icon = '⚠️'
        elif risk_level == 'LOW RISK':
            color = '#ffeb3b'
            icon = '⚡'
        else:
            color = '#4caf50'
            icon = '✅'
        
        with st.expander(f"{icon} {url} - {risk_level} ({risk_score}/100)"):
            st.markdown(f"**Risk Level:** {risk_level}")
            st.markdown(f"**Risk Score:** {risk_score}/100")
            
            if reasons:
                st.markdown("**Analysis:**")
                for reason in reasons:
                    st.markdown(f"- {reason}")


def create_metric_card(label: str, value: str, delta: str = None):
    """Create a styled metric card"""
    delta_html = f"<p style='color: #4caf50; font-size: 0.9rem;'>{delta}</p>" if delta else ""
    
    st.markdown(f"""
    <div class='glass-card' style='text-align: center; padding: 20px;'>
        <p style='color: #c8c8ff; font-size: 1rem; margin: 0;'>{label}</p>
        <h2 style='color: #ffffff; font-size: 2.5rem; margin: 10px 0;'>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

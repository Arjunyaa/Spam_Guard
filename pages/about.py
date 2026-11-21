"""
About page with project information
"""
import streamlit as st
from utils.ui_components import show_header


def show():
    """Display about page"""
    
    show_header("About SpamGuard AI", "Advanced AI-Powered Security Detection System")
    
    st.markdown("""
    <div class='glass-card'>
        <h2>🛡️ What is SpamGuard AI?</h2>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
            SpamGuard AI is a comprehensive, intelligent security detection application that protects you from 
            spam emails, scam SMS messages, and phishing URLs using advanced Machine Learning and Natural Language Processing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("### ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4>📧 Email Spam Detection</h4>
            <ul>
                <li>Analyze email content and subject lines</li>
                <li>Detect phishing attempts</li>
                <li>Identify suspicious sender patterns</li>
                <li>Extract and analyze embedded URLs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h4>🔗 URL Security Scanner</h4>
            <ul>
                <li>Analyze URL structure and patterns</li>
                <li>Detect IP-based phishing sites</li>
                <li>Identify URL shortener obfuscation</li>
                <li>Check for homograph attacks</li>
                <li>Risk scoring from 0-100</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h4>📊 Analytics Dashboard</h4>
            <ul>
                <li>Real-time detection statistics</li>
                <li>Interactive charts and graphs</li>
                <li>Threat trend analysis</li>
                <li>Protection impact metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4>📱 SMS Scam Detection</h4>
            <ul>
                <li>Identify lottery and prize scams</li>
                <li>Detect OTP phishing attempts</li>
                <li>Flag financial fraud messages</li>
                <li>Recognize urgency tactics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h4>🗂️ Bulk Processing</h4>
            <ul>
                <li>Upload and scan CSV files</li>
                <li>Batch message analysis</li>
                <li>Bulk URL scanning</li>
                <li>Export results to CSV</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
            <h4>📜 Detection History</h4>
            <ul>
                <li>SQLite database storage</li>
                <li>Search and filter history</li>
                <li>Export detection records</li>
                <li>Privacy-focused data handling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("### 🔧 Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h4>Backend</h4>
            <p>• Python 3.x<br>
            • Scikit-learn<br>
            • Pandas<br>
            • NumPy<br>
            • SQLite</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h4>Machine Learning</h4>
            <p>• TF-IDF Vectorization<br>
            • LinearSVC Classifier<br>
            • NLP Preprocessing<br>
            • Pattern Recognition<br>
            • Heuristic Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card' style='text-align: center;'>
            <h4>Frontend</h4>
            <p>• Streamlit<br>
            • Plotly Charts<br>
            • Custom CSS<br>
            • Glassmorphism UI<br>
            • Responsive Design</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("### 🔍 How It Works")
    
    st.markdown("""
    <div class='glass-card'>
        <h4>1️⃣ Text Analysis Pipeline</h4>
        <p><strong>Message Detection:</strong></p>
        <ol>
            <li><strong>Preprocessing:</strong> Clean and normalize text input</li>
            <li><strong>Feature Extraction:</strong> Convert text to TF-IDF vectors (unigrams + bigrams)</li>
            <li><strong>Classification:</strong> LinearSVC model predicts spam/safe</li>
            <li><strong>Keyword Analysis:</strong> Identify suspicious patterns and phrases</li>
            <li><strong>Confidence Scoring:</strong> Calculate prediction confidence</li>
        </ol>
        
        <h4>2️⃣ URL Analysis Pipeline</h4>
        <p><strong>URL Security Scanning:</strong></p>
        <ol>
            <li><strong>URL Parsing:</strong> Extract scheme, hostname, path, query parameters</li>
            <li><strong>Pattern Detection:</strong> Check for IP addresses, suspicious TLDs, punycode</li>
            <li><strong>Heuristic Analysis:</strong> Evaluate URL length, subdomains, special characters</li>
            <li><strong>Keyword Matching:</strong> Identify phishing-related terms</li>
            <li><strong>Risk Scoring:</strong> Calculate cumulative risk score (0-100)</li>
            <li><strong>ML Classification:</strong> Additional model-based prediction (optional)</li>
        </ol>
        
        <h4>3️⃣ Combined Analysis</h4>
        <p>For messages containing URLs:</p>
        <ul>
            <li>Message content is analyzed by the spam detection model</li>
            <li>Embedded URLs are extracted and analyzed separately</li>
            <li>Both results are presented with individual risk assessments</li>
            <li>Overall threat level is determined by combining both analyses</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Details
    st.markdown("### 🤖 Machine Learning Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4>Message Classification Model</h4>
            <p><strong>Algorithm:</strong> Linear Support Vector Classifier (LinearSVC)</p>
            <p><strong>Features:</strong> TF-IDF with 1-2 grams</p>
            <p><strong>Training Data:</strong> 5,572 SMS messages</p>
            <p><strong>Accuracy:</strong> ~98%</p>
            <p><strong>Why LinearSVC?</strong></p>
            <ul>
                <li>Fast training and prediction</li>
                <li>Excellent for high-dimensional text data</li>
                <li>Industry-proven for spam detection</li>
                <li>Memory efficient</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4>URL Classification Model</h4>
            <p><strong>Algorithm:</strong> LinearSVC (character n-grams)</p>
            <p><strong>Features:</strong> Character-level TF-IDF (1-3 grams)</p>
            <p><strong>Training Data:</strong> 60 labeled URLs</p>
            <p><strong>Note:</strong> Small dataset - supplemented with heuristics</p>
            <p><strong>Heuristic Rules:</strong></p>
            <ul>
                <li>Protocol analysis (HTTP/HTTPS)</li>
                <li>Domain structure validation</li>
                <li>Pattern matching for phishing indicators</li>
                <li>Entropy-based randomness detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Security Approach
    st.markdown("### 🔒 Security & Privacy")
    
    st.markdown("""
    <div class='glass-card'>
        <h4>Our Security Principles:</h4>
        <ul>
            <li><strong>Offline Analysis:</strong> URLs are analyzed without visiting them</li>
            <li><strong>No Auto-Execution:</strong> Links are never automatically opened</li>
            <li><strong>Local Processing:</strong> All analysis happens on your machine</li>
            <li><strong>Privacy-First:</strong> Detection history is stored locally in SQLite</li>
            <li><strong>No Data Transmission:</strong> Your messages are never sent to external servers</li>
            <li><strong>Transparent:</strong> Clear explanations for all detections</li>
        </ul>
        
        <h4>Important Limitations:</h4>
        <ul>
            <li>⚠️ HTTPS does NOT guarantee a website is safe</li>
            <li>⚠️ Cannot detect all sophisticated phishing attacks</li>
            <li>⚠️ Model performance depends on training data</li>
            <li>⚠️ Should be used as one layer of defense, not the only one</li>
            <li>⚠️ Always verify unexpected communications through official channels</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Information
    st.markdown("### 📚 Project Information")
    
    st.markdown("""
    <div class='glass-card'>
        <h4>Project Details</h4>
        <p><strong>Project Name:</strong> SpamGuard AI - Intelligent Email, SMS & Phishing Protection</p>
        <p><strong>Domain:</strong> Machine Learning, Cybersecurity, Natural Language Processing</p>
        <p><strong>Purpose:</strong> College Project / Portfolio Demonstration</p>
        <p><strong>Version:</strong> 1.0.0</p>
        
        <h4>Technologies Used</h4>
        <ul>
            <li><strong>Python:</strong> Core programming language</li>
            <li><strong>Streamlit:</strong> Web application framework</li>
            <li><strong>Scikit-learn:</strong> Machine learning library</li>
            <li><strong>Pandas:</strong> Data manipulation</li>
            <li><strong>Plotly:</strong> Interactive visualizations</li>
            <li><strong>SQLite:</strong> Local database</li>
            <li><strong>TF-IDF:</strong> Text feature extraction</li>
            <li><strong>LinearSVC:</strong> Classification algorithm</li>
        </ul>
        
        <h4>Features Implemented</h4>
        <ul>
            <li>✅ Real-time spam detection</li>
            <li>✅ URL security analysis</li>
            <li>✅ Bulk processing capabilities</li>
            <li>✅ Detection history with SQLite</li>
            <li>✅ Interactive analytics dashboard</li>
            <li>✅ Model performance evaluation</li>
            <li>✅ Modern glassmorphism UI</li>
            <li>✅ Comprehensive testing</li>
            <li>✅ CSV import/export</li>
            <li>✅ Responsive design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Acknowledgments
    st.markdown("### 🙏 Acknowledgments")
    
    st.markdown("""
    <div class='glass-card'>
        <p><strong>Datasets:</strong></p>
        <ul>
            <li>SMS Spam Collection Dataset (UCI Machine Learning Repository)</li>
            <li>Custom URL dataset for phishing detection</li>
        </ul>
        
        <p><strong>Libraries & Frameworks:</strong></p>
        <ul>
            <li>Streamlit Team - For the amazing web framework</li>
            <li>Scikit-learn Contributors - For ML tools</li>
            <li>Plotly Team - For interactive charts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #b8b8ff;'>
        <h3>🛡️ SpamGuard AI</h3>
        <p>Protecting You from Spam, Scams, and Phishing</p>
        <p style='font-size: 0.9rem; margin-top: 20px;'>
            Built with ❤️ using Python, Machine Learning & Streamlit<br>
            For Educational and Demonstration Purposes
        </p>
    </div>
    """, unsafe_allow_html=True)

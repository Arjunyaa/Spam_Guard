"""
Email spam detection page
"""
import streamlit as st
from utils.message_detection import MessageDetector
from utils.url_analyzer import batch_analyze_urls
from utils.ui_components import show_header, show_result_card, show_keyword_highlights, show_url_results


def show():
    """Display email detection page"""
    
    show_header("Email Spam Detection", "Analyze email messages for spam and phishing attempts")
    
    # Initialize detector
    if st.session_state.message_detector is None:
        try:
            st.session_state.message_detector = MessageDetector()
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            st.info("Please ensure the model files exist in the models/ directory.")
            return
    
    detector = st.session_state.message_detector
    
    # Input form
    st.markdown("### ✉️ Enter Email Details")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        subject = st.text_input("📌 Email Subject (Optional)", placeholder="e.g., Your Account Has Been Suspended")
    
    with col2:
        sender = st.text_input("👤 Sender (Optional)", placeholder="e.g., noreply@example.com")
    
    message = st.text_area(
        "📧 Email Message *",
        height=250,
        placeholder="Paste the email content here...\n\nExample:\nCongratulations! You have won a $1000 gift card. Click here to claim your prize now!"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Email", use_container_width=True, type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    # Analysis
    if analyze_button:
        if not message.strip():
            st.warning("⚠️ Please enter an email message to analyze.")
            return
        
        # Combine subject and message
        full_text = f"{subject} {message}" if subject else message
        
        with st.spinner("🔍 Analyzing email..."):
            try:
                # Analyze message
                result = detector.analyze_message(full_text, message_type='email')
                
                prediction = result['prediction']
                confidence = result['confidence']
                suspicious_words = result['suspicious_words']
                categories = result['categories']
                urls = result['urls']
                explanation = result['explanation']
                
                # Display result
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("## 📊 Analysis Results")
                
                show_result_card(prediction, confidence=confidence)
                
                # Explanation
                st.markdown("### 📝 Detailed Analysis")
                st.markdown(f"""
                <div class='glass-card'>
                    {explanation.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Show suspicious keywords
                if suspicious_words:
                    st.markdown("<br>", unsafe_allow_html=True)
                    show_keyword_highlights(suspicious_words, categories)
                
                # Analyze URLs if present
                if urls:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"### 🔗 Found {len(urls)} URL(s) in Email")
                    
                    with st.spinner("Analyzing URLs..."):
                        url_results = batch_analyze_urls(urls)
                        show_url_results(url_results)
                        
                        # Check for high-risk URLs
                        high_risk_urls = [r for r in url_results if r['risk_level'] == 'HIGH RISK']
                        if high_risk_urls:
                            st.error(f"🚨 Warning: {len(high_risk_urls)} high-risk URL(s) detected!")
                
                # Additional context
                st.markdown("### 💡 What to Do Next")
                
                if prediction == 'SPAM':
                    st.markdown("""
                    <div class='risk-high'>
                        <h4>⚠️ This email appears to be spam. Here's what you should do:</h4>
                        <ul>
                            <li>❌ Do NOT click any links in this email</li>
                            <li>❌ Do NOT reply or provide any personal information</li>
                            <li>❌ Do NOT download any attachments</li>
                            <li>✅ Mark this email as spam in your email client</li>
                            <li>✅ Delete the email</li>
                            <li>✅ If you received this from a known sender, contact them through another channel</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='risk-safe'>
                        <h4>✅ This email appears legitimate, but stay cautious:</h4>
                        <ul>
                            <li>✓ The message doesn't show obvious spam indicators</li>
                            <li>⚠️ Always verify the sender's email address</li>
                            <li>⚠️ Hover over links before clicking to see the actual URL</li>
                            <li>⚠️ Be cautious of urgent requests for personal information</li>
                            <li>⚠️ When in doubt, contact the sender through official channels</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Save to history
                try:
                    db = st.session_state.db
                    db.add_detection(
                        detection_type='email',
                        content=full_text,
                        prediction=prediction,
                        confidence=confidence,
                        explanation=explanation
                    )
                except Exception as e:
                    st.warning(f"Could not save to history: {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Examples
    with st.expander("📚 See Example Spam Emails"):
        st.markdown("""
        **Example 1: Prize Scam**
        ```
        Subject: CONGRATULATIONS! You've Won!
        
        Dear Winner,
        
        You have been selected to receive a FREE $1000 Walmart gift card! 
        Click here immediately to claim your prize before it expires.
        This offer is only valid for the next 24 hours!
        
        Claim Now: http://free-prize-claim.example/urgent
        ```
        
        **Example 2: Account Phishing**
        ```
        Subject: Urgent: Your Account Will Be Suspended
        
        We have detected suspicious activity on your account.
        Your account will be permanently suspended within 24 hours unless you verify your identity.
        
        Click here to verify now: http://verify-account-now.example/login
        
        Security Team
        ```
        
        **Example 3: Legitimate Email**
        ```
        Subject: Weekly Newsletter - Python Tips
        
        Hi there,
        
        Here are this week's Python programming tips and tutorials.
        Check out our latest article on data structures.
        
        Read more: https://www.example.com/blog/python-tips
        
        Best regards,
        The Team
        ```
        """)

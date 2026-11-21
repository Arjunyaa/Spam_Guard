"""
SMS spam detection page
"""
import streamlit as st
from utils.message_detection import MessageDetector
from utils.url_analyzer import batch_analyze_urls
from utils.ui_components import show_header, show_result_card, show_keyword_highlights, show_url_results


def show():
    """Display SMS detection page"""
    
    show_header("SMS Spam Detection", "Detect spam and scam messages in SMS texts")
    
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
    st.markdown("### 📱 Enter SMS Message")
    
    message = st.text_area(
        "SMS Text *",
        height=200,
        placeholder="Paste the SMS message here...\n\nExample:\nFREE entry in 2 a wkly comp to win FA Cup final tkts. Txt FA to 87121 to receive entry question"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 Analyze SMS", use_container_width=True, type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    # Analysis
    if analyze_button:
        if not message.strip():
            st.warning("⚠️ Please enter an SMS message to analyze.")
            return
        
        with st.spinner("🔍 Analyzing SMS..."):
            try:
                # Analyze message
                result = detector.analyze_message(message, message_type='sms')
                
                prediction = result['prediction']
                confidence = result['confidence']
                suspicious_words = result['suspicious_words']
                categories = result['categories']
                urls = result['urls']
                explanation = result['explanation']
                features = result['features']
                
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
                
                # Message statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Message Length", f"{features['length']} chars")
                
                with col2:
                    st.metric("Word Count", features['word_count'])
                
                with col3:
                    st.metric("URLs Found", features['url_count'])
                
                # Show suspicious keywords
                if suspicious_words:
                    st.markdown("<br>", unsafe_allow_html=True)
                    show_keyword_highlights(suspicious_words, categories)
                    
                    # Common SMS scam indicators
                    st.markdown("### 🚩 Common SMS Scam Indicators Found")
                    
                    scam_indicators = []
                    if 'urgency' in categories:
                        scam_indicators.append("⚠️ **Urgency tactics** - Creates pressure to act immediately")
                    if 'financial' in categories:
                        scam_indicators.append("💰 **Financial incentives** - Promises of free money or prizes")
                    if 'calls_to_action' in categories:
                        scam_indicators.append("📞 **Aggressive calls to action** - Demands immediate response")
                    if 'otp_scam' in categories:
                        scam_indicators.append("🔐 **OTP/Code requests** - May be attempting account takeover")
                    if 'credential_phishing' in categories:
                        scam_indicators.append("🎣 **Credential phishing** - Trying to steal login information")
                    
                    if scam_indicators:
                        for indicator in scam_indicators:
                            st.markdown(f"- {indicator}")
                
                # Analyze URLs if present
                if urls:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"### 🔗 Found {len(urls)} URL(s) in SMS")
                    
                    with st.spinner("Analyzing URLs..."):
                        url_results = batch_analyze_urls(urls)
                        show_url_results(url_results)
                        
                        # Check for high-risk URLs
                        high_risk_urls = [r for r in url_results if r['risk_level'] == 'HIGH RISK']
                        if high_risk_urls:
                            st.error(f"🚨 Warning: {len(high_risk_urls)} high-risk URL(s) detected!")
                
                # Phone numbers detected
                if features['has_phone']:
                    st.warning("📞 Phone number detected in message. Be cautious about calling unknown numbers.")
                
                # Safety recommendations
                st.markdown("### 💡 Safety Recommendations")
                
                if prediction == 'SPAM':
                    st.markdown("""
                    <div class='risk-high'>
                        <h4>🚨 This SMS appears to be spam/scam. Protect yourself:</h4>
                        <ul>
                            <li>❌ Do NOT click any links</li>
                            <li>❌ Do NOT call any phone numbers</li>
                            <li>❌ Do NOT reply to this message</li>
                            <li>❌ Do NOT share OTP codes or passwords</li>
                            <li>✅ Delete this message immediately</li>
                            <li>✅ Block the sender number</li>
                            <li>✅ Report as spam to your carrier</li>
                        </ul>
                        
                        <h4>⚠️ Common SMS scam types:</h4>
                        <ul>
                            <li>Prize/lottery scams</li>
                            <li>Fake delivery notifications</li>
                            <li>Banking/payment alerts</li>
                            <li>OTP phishing</li>
                            <li>Job offer scams</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='risk-safe'>
                        <h4>✅ This SMS appears legitimate, but always be careful:</h4>
                        <ul>
                            <li>✓ No obvious spam indicators detected</li>
                            <li>⚠️ Verify sender identity if requesting sensitive info</li>
                            <li>⚠️ Don't share OTP codes with anyone</li>
                            <li>⚠️ Be cautious of urgent payment requests</li>
                            <li>⚠️ When in doubt, contact the organization directly</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Save to history
                try:
                    db = st.session_state.db
                    db.add_detection(
                        detection_type='sms',
                        content=message,
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
    with st.expander("📚 See Example SMS Messages"):
        st.markdown("""
        **Example 1: Lottery Scam SMS**
        ```
        WINNER!! As a valued customer you have been selected to receive 
        a $900 prize reward! To claim call 09061701461. Claim code KL341. 
        Valid 12 hours only.
        ```
        **Classification:** SPAM
        **Indicators:** Urgency, prize lure, limited time, call to action
        
        ---
        
        **Example 2: Fake Delivery SMS**
        ```
        Your parcel has arrived but requires a customs fee of $2.99. 
        Pay now to avoid return: http://track-parcel-customs-fee.example/fee
        ```
        **Classification:** SPAM
        **Indicators:** Unexpected fee, suspicious URL, payment pressure
        
        ---
        
        **Example 3: OTP Phishing**
        ```
        Your bank OTP is 847293. Do not share this code with anyone. 
        If you didn't request this, call us immediately at 1-800-XXX-XXXX.
        ```
        **Classification:** Could be legitimate or scam
        **Note:** Banks never ask for OTPs. Verify sender before taking action.
        
        ---
        
        **Example 4: Legitimate SMS**
        ```
        Your appointment with Dr. Smith is confirmed for tomorrow at 2:00 PM.
        Reply CANCEL to reschedule. Thank you!
        ```
        **Classification:** SAFE
        **Indicators:** No urgency, no suspicious links, clear purpose
        
        ---
        
        **Example 5: Free Prize Scam**
        ```
        Congratulations! You've won a FREE iPhone 15! Click here to claim: 
        http://free-mobile-recharge.example/redeem. Limited stock!
        ```
        **Classification:** SPAM
        **Indicators:** Free prize, urgency, suspicious URL, too good to be true
        """)
    
    # Tips section
    with st.expander("🛡️ SMS Security Tips"):
        st.markdown("""
        ### How to Identify SMS Scams
        
        **Red Flags:**
        1. 🚩 Unexpected prizes or rewards
        2. 🚩 Urgent threats (account suspended, legal action)
        3. 🚩 Requests for OTP codes or passwords
        4. 🚩 Suspicious shortened URLs
        5. 🚩 Poor grammar or spelling
        6. 🚩 Sender doesn't match claimed organization
        7. 🚩 Requests for immediate payment
        8. 🚩 Too good to be true offers
        
        **Stay Safe:**
        - ✅ Never share OTP codes with anyone
        - ✅ Verify sender through official channels
        - ✅ Don't click links from unknown senders
        - ✅ Enable spam filters on your phone
        - ✅ Report scam messages to your carrier
        - ✅ Keep your phone's security software updated
        """)

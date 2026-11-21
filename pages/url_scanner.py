"""
URL scanner and analyzer page
"""
import streamlit as st
from utils.url_analyzer import analyze_url, batch_analyze_urls
from utils.ui_components import show_header, show_result_card


def show():
    """Display URL scanner page"""
    
    show_header("URL Security Scanner", "Analyze URLs for phishing and suspicious patterns")
    
    # Important security notice
    st.markdown("""
    <div class='glass-card' style='background: rgba(33, 150, 243, 0.1); border-color: rgba(33, 150, 243, 0.3);'>
        <h4>🔒 Important Security Notice</h4>
        <p>This tool analyzes URL patterns and structures <strong>without visiting them</strong>. 
        It uses heuristic analysis and machine learning to identify suspicious characteristics.</p>
        <p><strong>⚠️ Note:</strong> HTTPS does not guarantee a website is safe. Phishing sites can also use HTTPS.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for single and bulk scanning
    tab1, tab2 = st.tabs(["🔗 Single URL", "📋 Multiple URLs"])
    
    with tab1:
        st.markdown("### Analyze a Single URL")
        
        url_input = st.text_input(
            "Enter URL to analyze:",
            placeholder="https://example.com/page",
            help="Paste any URL to check for suspicious patterns"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            scan_button = st.button("🔍 Scan URL", use_container_width=True, type="primary")
        
        if scan_button:
            if not url_input.strip():
                st.warning("⚠️ Please enter a URL to analyze.")
            else:
                with st.spinner("🔍 Analyzing URL..."):
                    result = analyze_url(url_input)
                    
                    risk_level = result['risk_level']
                    risk_score = result['risk_score']
                    reasons = result['reasons']
                    features = result['features']
                    
                    # Display result
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("## 📊 Analysis Results")
                    
                    show_result_card(risk_level, risk_score=risk_score)
                    
                    # Risk details
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Risk Score", f"{risk_score}/100")
                    
                    with col2:
                        protocol = features.get('scheme', 'unknown').upper()
                        color = 'green' if protocol == 'HTTPS' else 'red'
                        st.metric("Protocol", protocol)
                    
                    with col3:
                        url_type = "Domain" if not features.get('is_ip_address') else "IP Address"
                        st.metric("Type", url_type)
                    
                    # Analysis details
                    st.markdown("### 🔍 Detailed Analysis")
                    
                    if reasons:
                        for reason in reasons:
                            if reason.startswith('✓'):
                                st.success(reason)
                            elif reason.startswith('⚠️') or reason.startswith('❌'):
                                st.warning(reason)
                            else:
                                st.info(reason)
                    
                    # Technical details
                    with st.expander("🔧 Technical Details"):
                        st.markdown(f"""
                        **URL Components:**
                        - **Scheme:** {features.get('scheme', 'N/A')}
                        - **Hostname:** {features.get('hostname', 'N/A')}
                        - **Path:** {features.get('path', 'N/A') if features.get('path') else '/'}
                        - **Query:** {features.get('query', 'N/A') if features.get('query') else 'None'}
                        
                        **Analysis:**
                        - **URL Length:** {features.get('url_length', 0)} characters
                        - **Subdomain Count:** {features.get('subdomain_count', 0)}
                        - **Uses IP Address:** {'Yes' if features.get('is_ip_address') else 'No'}
                        - **Suspicious Keywords:** {len(features.get('suspicious_keywords', []))}
                        - **Entropy Score:** {features.get('entropy', 0):.2f}
                        """)
                        
                        if features.get('suspicious_keywords'):
                            st.markdown("**Suspicious Keywords Found:**")
                            st.write(', '.join(features['suspicious_keywords']))
                    
                    # Recommendations
                    st.markdown("### 💡 Recommendations")
                    
                    if risk_level == 'HIGH RISK':
                        st.markdown("""
                        <div class='risk-high'>
                            <h4>🚨 HIGH RISK - Do Not Visit This URL</h4>
                            <ul>
                                <li>❌ Do NOT click or visit this link</li>
                                <li>❌ Do NOT enter any personal information</li>
                                <li>❌ Do NOT download anything</li>
                                <li>✅ Delete messages containing this URL</li>
                                <li>✅ Report to security team if received at work</li>
                                <li>✅ Warn others if shared in groups</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif risk_level == 'SUSPICIOUS':
                        st.markdown("""
                        <div class='risk-suspicious'>
                            <h4>⚠️ SUSPICIOUS - Exercise Extreme Caution</h4>
                            <ul>
                                <li>⚠️ Verify this URL through official channels</li>
                                <li>⚠️ Do not enter sensitive information</li>
                                <li>⚠️ Check sender legitimacy</li>
                                <li>✅ Contact organization directly if claiming to be from them</li>
                                <li>✅ Use official website instead</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif risk_level == 'LOW RISK':
                        st.markdown("""
                        <div class='risk-low'>
                            <h4>⚡ LOW RISK - Some Concerns Present</h4>
                            <ul>
                                <li>✓ Generally appears safe but has minor concerns</li>
                                <li>⚠️ Verify sender if received unexpectedly</li>
                                <li>⚠️ Check URL carefully before visiting</li>
                                <li>⚠️ Avoid entering sensitive data unless certain</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:  # BENIGN
                        st.markdown("""
                        <div class='risk-safe'>
                            <h4>✅ BENIGN - Appears Safe</h4>
                            <ul>
                                <li>✓ No obvious suspicious indicators detected</li>
                                <li>✓ Uses proper domain structure</li>
                                <li>ℹ️ Still verify sender if received unexpectedly</li>
                                <li>ℹ️ Hover over links to verify before clicking</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Save to database
                    try:
                        db = st.session_state.db
                        db.add_url_scan(url_input, risk_level, risk_score, reasons)
                    except Exception as e:
                        pass  # Silent fail for history
    
    with tab2:
        st.markdown("### Analyze Multiple URLs")
        st.info("Enter one URL per line to analyze multiple URLs at once")
        
        urls_input = st.text_area(
            "Enter URLs (one per line):",
            height=200,
            placeholder="https://example.com/page1\nhttps://example.org/page2\nhttps://example.net/page3"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            scan_multiple_button = st.button("🔍 Scan All URLs", use_container_width=True, type="primary")
        
        if scan_multiple_button:
            if not urls_input.strip():
                st.warning("⚠️ Please enter at least one URL.")
            else:
                urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
                
                if len(urls) > 50:
                    st.error("❌ Maximum 50 URLs allowed at once.")
                else:
                    st.info(f"Analyzing {len(urls)} URL(s)...")
                    
                    progress_bar = st.progress(0)
                    results_container = st.container()
                    
                    results = []
                    for i, url in enumerate(urls):
                        result = analyze_url(url)
                        results.append(result)
                        progress_bar.progress((i + 1) / len(urls))
                    
                    progress_bar.empty()
                    
                    # Summary
                    high_risk = sum(1 for r in results if r['risk_level'] == 'HIGH RISK')
                    suspicious = sum(1 for r in results if r['risk_level'] == 'SUSPICIOUS')
                    low_risk = sum(1 for r in results if r['risk_level'] == 'LOW RISK')
                    benign = sum(1 for r in results if r['risk_level'] == 'BENIGN')
                    
                    st.markdown("### 📊 Scan Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🚨 High Risk", high_risk)
                    with col2:
                        st.metric("⚠️ Suspicious", suspicious)
                    with col3:
                        st.metric("⚡ Low Risk", low_risk)
                    with col4:
                        st.metric("✅ Benign", benign)
                    
                    # Detailed results
                    st.markdown("### 📋 Detailed Results")
                    
                    for result in results:
                        risk_level = result['risk_level']
                        risk_score = result['risk_score']
                        url = result['url']
                        reasons = result['reasons']
                        
                        # Color coding
                        if risk_level == 'HIGH RISK':
                            icon = '🚨'
                            color = '#f44336'
                        elif risk_level == 'SUSPICIOUS':
                            icon = '⚠️'
                            color = '#ff9800'
                        elif risk_level == 'LOW RISK':
                            icon = '⚡'
                            color = '#ffeb3b'
                        else:
                            icon = '✅'
                            color = '#4caf50'
                        
                        with st.expander(f"{icon} {url} - {risk_level} ({risk_score}/100)"):
                            st.markdown(f"**Risk Level:** {risk_level}")
                            st.markdown(f"**Risk Score:** {risk_score}/100")
                            
                            st.markdown("**Analysis:**")
                            for reason in reasons:
                                st.markdown(f"- {reason}")
                        
                        # Save to database
                        try:
                            db = st.session_state.db
                            db.add_url_scan(url, risk_level, risk_score, reasons)
                        except:
                            pass
    
    # Educational content
    with st.expander("📚 Understanding URL Analysis"):
        st.markdown("""
        ### What We Check
        
        Our URL analyzer examines multiple characteristics:
        
        1. **Protocol Security**
           - HTTP vs HTTPS encryption
           - Note: HTTPS does NOT guarantee safety
        
        2. **Domain Analysis**
           - IP addresses instead of domains
           - Suspicious top-level domains (.tk, .ml, etc.)
           - Punycode/IDN homograph attacks
        
        3. **URL Structure**
           - Excessive length
           - Too many subdomains
           - @ symbol tricks
           - Unusual ports
        
        4. **Pattern Recognition**
           - URL shorteners (hidden destination)
           - Suspicious keywords (login, verify, urgent)
           - Random-looking strings (high entropy)
        
        5. **Known Indicators**
           - Brand impersonation patterns
           - Common phishing techniques
        
        ### Limitations
        
        - Analysis is based on URL structure only
        - Cannot detect all sophisticated attacks
        - False positives may occur
        - Should be used as one layer of defense
        
        ### Best Practices
        
        - Always verify unexpected links
        - Check sender legitimacy
        - Use official websites directly
        - Don't trust links in unsolicited messages
        - Enable 2FA for important accounts
        """)

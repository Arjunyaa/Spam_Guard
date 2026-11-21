"""
Bulk detection page for processing multiple messages from CSV
"""
import streamlit as st
import pandas as pd
import io
from utils.message_detection import MessageDetector
from utils.url_analyzer import batch_analyze_urls, analyze_url
from utils.ui_components import show_header


def show():
    """Display bulk detection page"""
    
    show_header("Bulk Detection", "Analyze multiple messages or URLs from CSV files")
    
    # Initialize detector
    if st.session_state.message_detector is None:
        try:
            st.session_state.message_detector = MessageDetector()
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return
    
    detector = st.session_state.message_detector
    
    # Tabs for different bulk operations
    tab1, tab2 = st.tabs(["📧 Bulk Messages", "🔗 Bulk URLs"])
    
    with tab1:
        st.markdown("### 📊 Analyze Multiple Messages")
        
        st.info("""
        **CSV Format Required:**
        - Must contain a column named **'message'** or **'text'**
        - Optional: **'type'** column ('email' or 'sms')
        - Each row will be analyzed separately
        """)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file containing messages to analyze"
        )
        
        if uploaded_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(uploaded_file)
                
                st.success(f"✅ Loaded {len(df)} messages")
                
                # Show preview
                with st.expander("👀 Preview Data"):
                    st.dataframe(df.head(10))
                
                # Find message column
                message_col = None
                for col in ['message', 'text', 'Message', 'Text', 'content', 'Content']:
                    if col in df.columns:
                        message_col = col
                        break
                
                if message_col is None:
                    st.error("❌ No 'message' or 'text' column found in CSV")
                    st.info("Please ensure your CSV has a column named 'message' or 'text'")
                else:
                    # Type column
                    type_col = 'type' if 'type' in df.columns else None
                    
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        analyze_button = st.button("🔍 Analyze All", use_container_width=True, type="primary")
                    
                    if analyze_button:
                        st.markdown("### 🔄 Processing Messages...")
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        results = []
                        
                        for idx, row in df.iterrows():
                            message = str(row[message_col])
                            msg_type = row[type_col] if type_col else 'message'
                            
                            status_text.text(f"Analyzing message {idx+1}/{len(df)}...")
                            
                            # Analyze
                            analysis = detector.analyze_message(message, msg_type)
                            
                            results.append({
                                'message': message[:100] + '...' if len(message) > 100 else message,
                                'prediction': analysis['prediction'],
                                'confidence': f"{analysis['confidence']*100:.1f}%",
                                'suspicious_words': len(analysis['suspicious_words']),
                                'urls_found': len(analysis['urls'])
                            })
                            
                            # Save to database
                            try:
                                db = st.session_state.db
                                db.add_detection(
                                    detection_type=msg_type,
                                    content=message,
                                    prediction=analysis['prediction'],
                                    confidence=analysis['confidence'],
                                    explanation=analysis['explanation']
                                )
                            except:
                                pass
                            
                            progress_bar.progress((idx + 1) / len(df))
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        
                        # Summary
                        st.markdown("### 📊 Analysis Summary")
                        
                        spam_count = sum(1 for r in results if r['prediction'] == 'SPAM')
                        safe_count = sum(1 for r in results if r['prediction'] == 'SAFE')
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Analyzed", len(results))
                        with col2:
                            st.metric("🚨 Spam", spam_count)
                        with col3:
                            st.metric("✅ Safe", safe_count)
                        with col4:
                            spam_rate = (spam_count / len(results) * 100) if len(results) > 0 else 0
                            st.metric("Spam Rate", f"{spam_rate:.1f}%")
                        
                        # Display results
                        st.markdown("### 📋 Detailed Results")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="bulk_detection_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        st.success("✅ Bulk analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error processing CSV: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
        
        # Template download
        st.markdown("### 📄 Download CSV Template")
        
        template_df = pd.DataFrame({
            'message': [
                'FREE entry to win a $1000 prize! Click now!',
                'Your meeting is scheduled for tomorrow at 2 PM',
                'URGENT: Your account will be suspended. Verify now!'
            ],
            'type': ['sms', 'email', 'sms']
        })
        
        template_csv = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template CSV",
            data=template_csv,
            file_name="message_template.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.markdown("### 🔗 Analyze Multiple URLs")
        
        st.info("""
        **CSV Format Required:**
        - Must contain a column named **'url'**
        - Each row should contain one URL
        """)
        
        # File uploader
        url_file = st.file_uploader(
            "Upload CSV file with URLs",
            type=['csv'],
            help="Upload a CSV file containing URLs to analyze",
            key="url_uploader"
        )
        
        if url_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(url_file)
                
                st.success(f"✅ Loaded {len(df)} URLs")
                
                # Show preview
                with st.expander("👀 Preview Data"):
                    st.dataframe(df.head(10))
                
                # Find URL column
                url_col = None
                for col in ['url', 'URL', 'link', 'Link']:
                    if col in df.columns:
                        url_col = col
                        break
                
                if url_col is None:
                    st.error("❌ No 'url' column found in CSV")
                    st.info("Please ensure your CSV has a column named 'url'")
                else:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        analyze_urls_button = st.button("🔍 Analyze All URLs", use_container_width=True, type="primary")
                    
                    if analyze_urls_button:
                        st.markdown("### 🔄 Processing URLs...")
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        results = []
                        
                        for idx, row in df.iterrows():
                            url = str(row[url_col])
                            
                            status_text.text(f"Analyzing URL {idx+1}/{len(df)}...")
                            
                            # Analyze
                            analysis = analyze_url(url)
                            
                            results.append({
                                'url': url,
                                'risk_level': analysis['risk_level'],
                                'risk_score': analysis['risk_score'],
                                'protocol': analysis['features'].get('scheme', 'unknown').upper(),
                                'is_ip': 'Yes' if analysis['features'].get('is_ip_address') else 'No'
                            })
                            
                            # Save to database
                            try:
                                db = st.session_state.db
                                db.add_url_scan(
                                    url=url,
                                    risk_level=analysis['risk_level'],
                                    risk_score=analysis['risk_score'],
                                    reasons=analysis['reasons']
                                )
                            except:
                                pass
                            
                            progress_bar.progress((idx + 1) / len(df))
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        
                        # Summary
                        st.markdown("### 📊 Analysis Summary")
                        
                        high_risk = sum(1 for r in results if r['risk_level'] == 'HIGH RISK')
                        suspicious = sum(1 for r in results if r['risk_level'] == 'SUSPICIOUS')
                        low_risk = sum(1 for r in results if r['risk_level'] == 'LOW RISK')
                        benign = sum(1 for r in results if r['risk_level'] == 'BENIGN')
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("🚨 High Risk", high_risk)
                        with col2:
                            st.metric("⚠️ Suspicious", suspicious)
                        with col3:
                            st.metric("⚡ Low Risk", low_risk)
                        with col4:
                            st.metric("✅ Benign", benign)
                        
                        # Display results
                        st.markdown("### 📋 Detailed Results")
                        
                        # Color-code the dataframe
                        def highlight_risk(row):
                            if row['risk_level'] == 'HIGH RISK':
                                return ['background-color: rgba(244, 67, 54, 0.2)'] * len(row)
                            elif row['risk_level'] == 'SUSPICIOUS':
                                return ['background-color: rgba(255, 152, 0, 0.2)'] * len(row)
                            elif row['risk_level'] == 'LOW RISK':
                                return ['background-color: rgba(255, 235, 59, 0.2)'] * len(row)
                            else:
                                return ['background-color: rgba(76, 175, 80, 0.2)'] * len(row)
                        
                        styled_df = results_df.style.apply(highlight_risk, axis=1)
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="url_scan_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        st.success("✅ Bulk URL scan complete!")
                
            except Exception as e:
                st.error(f"❌ Error processing CSV: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
        
        # Template download
        st.markdown("### 📄 Download CSV Template")
        
        url_template_df = pd.DataFrame({
            'url': [
                'https://www.example.com/contact',
                'http://claim-free-prize.example/urgent',
                'https://www.example.org/about'
            ]
        })
        
        url_template_csv = url_template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template CSV",
            data=url_template_csv,
            file_name="url_template.csv",
            mime="text/csv",
            key="url_template_download"
        )

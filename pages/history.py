"""
Detection history page
"""
import streamlit as st
import pandas as pd
from utils.ui_components import show_header


def show():
    """Display detection history page"""
    
    show_header("Detection History", "View and manage your past detections")
    
    db = st.session_state.db
    
    # Control buttons
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search history", placeholder="Enter search term...")
    
    with col2:
        filter_type = st.selectbox("Filter by type", ["All", "email", "sms", "url"])
    
    with col3:
        filter_result = st.selectbox("Filter by result", ["All", "SPAM", "SAFE"])
    
    with col4:
        if st.button("🗑️ Clear All History", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                db.clear_all_history()
                st.success("✅ History cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm")
    
    # Get detections based on filters
    try:
        if search_term:
            detections = db.search_detections(search_term)
        elif filter_type != "All":
            detections = db.get_detections_by_type(filter_type)
        elif filter_result != "All":
            detections = db.get_detections_by_prediction(filter_result)
        else:
            detections = db.get_all_detections(limit=100)
        
        if not detections:
            st.info("📭 No detection history found. Start analyzing messages to build your history!")
        else:
            st.markdown(f"### 📊 Showing {len(detections)} detection(s)")
            
            # Export button
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col3:
                # Create CSV
                df = pd.DataFrame(detections)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv,
                    file_name="detection_history.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Display detections
            for detection in detections:
                detection_id = detection['id']
                detection_type = detection['detection_type']
                content = detection['content']
                prediction = detection['prediction']
                confidence = detection.get('confidence')
                risk_score = detection.get('risk_score')
                explanation = detection.get('explanation', '')
                timestamp = detection['timestamp']
                
                # Determine color and icon
                if 'spam' in prediction.lower() or 'high risk' in prediction.lower():
                    color = '#f44336'
                    icon = '🚨'
                    border_color = 'rgba(244, 67, 54, 0.5)'
                elif 'suspicious' in prediction.lower():
                    color = '#ff9800'
                    icon = '⚠️'
                    border_color = 'rgba(255, 152, 0, 0.5)'
                elif 'safe' in prediction.lower() or 'legitimate' in prediction.lower() or 'benign' in prediction.lower():
                    color = '#4caf50'
                    icon = '✅'
                    border_color = 'rgba(76, 175, 80, 0.5)'
                else:
                    color = '#9e9e9e'
                    icon = '❓'
                    border_color = 'rgba(158, 158, 158, 0.5)'
                
                # Truncate content
                content_preview = content[:200] + "..." if len(content) > 200 else content
                
                # Score display
                score_text = ""
                if confidence is not None:
                    score_text = f"Confidence: {confidence*100:.1f}%"
                elif risk_score is not None:
                    score_text = f"Risk Score: {risk_score}/100"
                
                with st.container():
                    st.markdown(f"""
                    <div class='glass-card' style='border: 1px solid {border_color}; padding: 20px; margin: 10px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: start;'>
                            <div style='flex: 1;'>
                                <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                                    <span style='font-size: 1.8rem; margin-right: 10px;'>{icon}</span>
                                    <div>
                                        <strong style='color: {color}; font-size: 1.2rem;'>{prediction}</strong>
                                        <br>
                                        <small style='color: #b8b8ff;'>{detection_type.upper()} • {timestamp}</small>
                                    </div>
                                </div>
                                <p style='color: #e0e0e0; margin: 10px 0; font-family: monospace; font-size: 0.9rem;'>{content_preview}</p>
                                {f"<p style='color: #c8c8ff; margin: 10px 0;'>{score_text}</p>" if score_text else ""}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        if explanation:
                            with st.expander("📝 View Explanation"):
                                st.markdown(explanation)
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{detection_id}", use_container_width=True):
                            db.delete_detection(detection_id)
                            st.success("✅ Deleted!")
                            st.rerun()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error loading history: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

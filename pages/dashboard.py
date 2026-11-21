"""
Dashboard page with statistics and overview
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd


def show():
    """Display the dashboard page"""
    
    st.markdown("<h1 style='text-align: center;'>🛡️ SpamGuard AI Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #b8b8ff;'>Intelligent Email, SMS & Phishing Protection</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    
    # Get statistics
    try:
        db = st.session_state.db
        stats = db.get_statistics()
        
        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <p style='color: #c8c8ff; font-size: 1rem; margin: 0;'>Total Scans</p>
                <h2 style='color: #ffffff; font-size: 2.5rem; margin: 10px 0;'>{stats['total_detections']}</h2>
                <p style='color: #4caf50; font-size: 0.9rem;'>All time</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            spam_percentage = (stats['spam_count'] / stats['total_detections'] * 100) if stats['total_detections'] > 0 else 0
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <p style='color: #c8c8ff; font-size: 1rem; margin: 0;'>Spam Detected</p>
                <h2 style='color: #f44336; font-size: 2.5rem; margin: 10px 0;'>{stats['spam_count']}</h2>
                <p style='color: #ff9800; font-size: 0.9rem;'>{spam_percentage:.1f}% of total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <p style='color: #c8c8ff; font-size: 1rem; margin: 0;'>Safe Messages</p>
                <h2 style='color: #4caf50; font-size: 2.5rem; margin: 10px 0;'>{stats['safe_count']}</h2>
                <p style='color: #66bb6a; font-size: 0.9rem;'>Legitimate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <p style='color: #c8c8ff; font-size: 1rem; margin: 0;'>Suspicious URLs</p>
                <h2 style='color: #ff9800; font-size: 2.5rem; margin: 10px 0;'>{stats['suspicious_urls']}</h2>
                <p style='color: #ffa726; font-size: 0.9rem;'>Flagged</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Spam vs Safe Distribution")
            
            if stats['total_detections'] > 0:
                # Pie chart
                labels = ['Safe Messages', 'Spam Messages']
                values = [stats['safe_count'], stats['spam_count']]
                colors = ['#4caf50', '#f44336']
                
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),
                    hole=0.4,
                    textinfo='label+percent',
                    textfont=dict(size=14, color='white')
                )])
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    showlegend=True,
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available yet. Start analyzing messages!")
        
        with col2:
            st.markdown("### 📈 Detection Activity")
            
            # Get recent activity
            activity_df = db.get_recent_activity(days=7)
            
            if not activity_df.empty:
                # Create bar chart
                fig = px.bar(
                    activity_df,
                    x='date',
                    y='count',
                    color='detection_type',
                    title='Last 7 Days Activity',
                    labels={'count': 'Number of Detections', 'date': 'Date'},
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
                )
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=350,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No recent activity. Start scanning to see trends!")
        
        # Detection by type
        st.markdown("### 📱 Detection by Type")
        
        if stats['by_type']:
            type_df = pd.DataFrame(list(stats['by_type'].items()), columns=['Type', 'Count'])
            
            fig = go.Figure(data=[go.Bar(
                x=type_df['Type'],
                y=type_df['Count'],
                marker=dict(
                    color=['#667eea', '#764ba2', '#f093fb'][:len(type_df)],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=type_df['Count'],
                textposition='auto',
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=300,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Count')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No type data available yet.")
        
        # Recent detections
        st.markdown("### 🕐 Recent Activity")
        
        recent = db.get_all_detections(limit=5)
        
        if recent:
            for detection in recent:
                # Truncate content for display
                content = detection['content'][:100] + "..." if len(detection['content']) > 100 else detection['content']
                
                # Determine color
                if 'spam' in detection['prediction'].lower():
                    color = '#f44336'
                    icon = '🚨'
                elif 'safe' in detection['prediction'].lower() or 'legitimate' in detection['prediction'].lower():
                    color = '#4caf50'
                    icon = '✅'
                else:
                    color = '#ff9800'
                    icon = '⚠️'
                
                st.markdown(f"""
                <div class='glass-card' style='padding: 15px; margin: 10px 0;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='flex: 1;'>
                            <span style='font-size: 1.5rem;'>{icon}</span>
                            <strong style='color: {color}; margin-left: 10px;'>{detection['prediction']}</strong>
                            <span style='color: #b8b8ff; margin-left: 10px;'>({detection['detection_type']})</span>
                        </div>
                        <small style='color: #888;'>{detection['timestamp']}</small>
                    </div>
                    <p style='color: #c8c8ff; margin: 10px 0 0 0; font-size: 0.9rem;'>{content}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent detections. Start analyzing to build your history!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Start using the detection features to see statistics here!")
    
    # Quick action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Analyze Email", use_container_width=True):
            st.switch_page("pages/email_detection.py")
    
    with col2:
        if st.button("📱 Analyze SMS", use_container_width=True):
            st.switch_page("pages/sms_detection.py")
    
    with col3:
        if st.button("🔗 Scan URL", use_container_width=True):
            st.switch_page("pages/url_scanner.py")

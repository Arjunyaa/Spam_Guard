"""
Analytics and visualization page
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.ui_components import show_header


def show():
    """Display analytics page"""
    
    show_header("Analytics & Insights", "Visualize detection patterns and trends")
    
    db = st.session_state.db
    
    try:
        stats = db.get_statistics()
        
        if stats['total_detections'] == 0:
            st.info("📊 No data available yet. Start analyzing messages to see analytics!")
            return
        
        # Time period selector
        period = st.selectbox(
            "📅 Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"]
        )
        
        days_map = {
            "Last 7 Days": 7,
            "Last 30 Days": 30,
            "Last 90 Days": 90,
            "All Time": 365 * 10  # Large number
        }
        
        days = days_map[period]
        
        # Overall metrics
        st.markdown("### 📊 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Detections",
                stats['total_detections'],
                delta=None
            )
        
        with col2:
            spam_rate = (stats['spam_count'] / stats['total_detections'] * 100) if stats['total_detections'] > 0 else 0
            st.metric(
                "Spam Detection Rate",
                f"{spam_rate:.1f}%",
                delta=f"{stats['spam_count']} spam"
            )
        
        with col3:
            safe_rate = (stats['safe_count'] / stats['total_detections'] * 100) if stats['total_detections'] > 0 else 0
            st.metric(
                "Safe Message Rate",
                f"{safe_rate:.1f}%",
                delta=f"{stats['safe_count']} safe"
            )
        
        with col4:
            st.metric(
                "URLs Scanned",
                stats['url_scans'],
                delta=f"{stats['suspicious_urls']} suspicious"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🥧 Spam vs Safe Distribution")
            
            labels = ['Safe Messages', 'Spam Messages']
            values = [stats['safe_count'], stats['spam_count']]
            colors = ['#4caf50', '#f44336']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                hole=0.5,
                textinfo='label+percent+value',
                textfont=dict(size=14, color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                height=350,
                title=dict(
                    text=f"Total: {stats['total_detections']} messages",
                    font=dict(size=14, color='#c8c8ff')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📱 Detection by Type")
            
            if stats['by_type']:
                type_labels = list(stats['by_type'].keys())
                type_values = list(stats['by_type'].values())
                
                fig = go.Figure(data=[go.Bar(
                    x=type_labels,
                    y=type_values,
                    marker=dict(
                        color=['#667eea', '#764ba2', '#f093fb'][:len(type_labels)],
                        line=dict(color='rgba(255,255,255,0.3)', width=1)
                    ),
                    text=type_values,
                    textposition='auto',
                    textfont=dict(size=14, color='white'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                )])
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=350,
                    xaxis=dict(
                        showgrid=False,
                        title=dict(text='Detection Type', font=dict(color='#c8c8ff'))
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        title=dict(text='Count', font=dict(color='#c8c8ff'))
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Activity over time
        st.markdown(f"### 📈 Activity Trend - {period}")
        
        activity_df = db.get_recent_activity(days=days)
        
        if not activity_df.empty:
            # Prepare data
            fig = px.line(
                activity_df,
                x='date',
                y='count',
                color='detection_type',
                title=f'Detection Activity Over Time',
                labels={'count': 'Number of Detections', 'date': 'Date', 'detection_type': 'Type'},
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data available for the selected period.")
        
        # Detailed breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### By Detection Type")
            
            if stats['by_type']:
                type_df = pd.DataFrame(list(stats['by_type'].items()), columns=['Type', 'Count'])
                type_df['Percentage'] = (type_df['Count'] / type_df['Count'].sum() * 100).round(1)
                type_df['Percentage'] = type_df['Percentage'].astype(str) + '%'
                
                st.dataframe(type_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Risk Summary")
            
            risk_data = {
                'Category': ['Spam Detected', 'Safe Messages', 'Suspicious URLs', 'Total Scans'],
                'Count': [
                    stats['spam_count'],
                    stats['safe_count'],
                    stats['suspicious_urls'],
                    stats['total_detections']
                ]
            }
            
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        # Protection impact
        st.markdown("### 🛡️ Protection Impact")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px; border: 2px solid rgba(244, 67, 54, 0.5);'>
                <h3 style='color: #f44336; font-size: 2.5rem; margin: 10px 0;'>{stats['spam_count']}</h3>
                <p style='color: #c8c8ff;'>Spam Messages<br>Blocked</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px; border: 2px solid rgba(255, 152, 0, 0.5);'>
                <h3 style='color: #ff9800; font-size: 2.5rem; margin: 10px 0;'>{stats['suspicious_urls']}</h3>
                <p style='color: #c8c8ff;'>Suspicious URLs<br>Flagged</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            protection_rate = (stats['spam_count'] + stats['suspicious_urls']) / stats['total_detections'] * 100 if stats['total_detections'] > 0 else 0
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 20px; border: 2px solid rgba(76, 175, 80, 0.5);'>
                <h3 style='color: #4caf50; font-size: 2.5rem; margin: 10px 0;'>{protection_rate:.1f}%</h3>
                <p style='color: #c8c8ff;'>Threat Detection<br>Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

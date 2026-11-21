"""
Model performance and evaluation page
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import plotly.graph_objects as go
import plotly.figure_factory as ff
from utils.ui_components import show_header


def show():
    """Display model performance page"""
    
    show_header("Model Performance", "Evaluate and compare ML models")
    
    st.info("📊 This page shows the performance metrics of the trained spam detection model.")
    
    # Load and evaluate model
    try:
        # Load dataset
        dataset_path = 'dataset/spam.csv'
        df = pd.read_csv(dataset_path, encoding='latin-1')
        df = df[['v1', 'v2']]
        df.columns = ['label', 'message']
        df['label_num'] = df.label.map({'ham': 0, 'spam': 1})
        
        st.markdown("### 📁 Dataset Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Messages", len(df))
        
        with col2:
            ham_count = len(df[df['label'] == 'ham'])
            st.metric("Ham (Safe)", ham_count)
        
        with col3:
            spam_count = len(df[df['label'] == 'spam'])
            st.metric("Spam", spam_count)
        
        with col4:
            spam_percentage = (spam_count / len(df)) * 100
            st.metric("Spam Ratio", f"{spam_percentage:.1f}%")
        
        # Distribution chart
        st.markdown("### 📊 Dataset Distribution")
        
        fig = go.Figure(data=[go.Bar(
            x=['Ham (Safe)', 'Spam'],
            y=[ham_count, spam_count],
            marker=dict(
                color=['#4caf50', '#f44336'],
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            text=[ham_count, spam_count],
            textposition='auto',
            textfont=dict(size=16, color='white')
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title='Count'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Model evaluation
        st.markdown("### 🎯 Model Evaluation")
        
        with st.spinner("Evaluating models..."):
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                df['message'], df['label_num'], 
                test_size=0.2, random_state=42, stratify=df['label_num']
            )
            
            # Vectorize
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=2)
            X_train_vec = vectorizer.fit_transform(X_train)
            X_test_vec = vectorizer.transform(X_test)
            
            st.info(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}")
            
            # Compare models
            models = {
                'LinearSVC (Current)': LinearSVC(random_state=42),
                'Multinomial Naive Bayes': MultinomialNB(),
                'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
            }
            
            results = {}
            
            for name, model in models.items():
                model.fit(X_train_vec, y_train)
                y_pred = model.predict(X_test_vec)
                
                accuracy = accuracy_score(y_test, y_pred)
                report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
                cm = confusion_matrix(y_test, y_pred)
                
                results[name] = {
                    'accuracy': accuracy,
                    'precision': report['1']['precision'],
                    'recall': report['1']['recall'],
                    'f1': report['1']['f1-score'],
                    'confusion_matrix': cm,
                    'predictions': y_pred
                }
            
            # Display comparison
            st.markdown("#### 📈 Model Comparison")
            
            comparison_data = []
            for name, metrics in results.items():
                comparison_data.append({
                    'Model': name,
                    'Accuracy': f"{metrics['accuracy']*100:.2f}%",
                    'Precision': f"{metrics['precision']*100:.2f}%",
                    'Recall': f"{metrics['recall']*100:.2f}%",
                    'F1-Score': f"{metrics['f1']*100:.2f}%"
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            # Detailed metrics for current model
            st.markdown("### 🎯 LinearSVC (Current Model) - Detailed Metrics")
            
            current_model = results['LinearSVC (Current)']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Accuracy", f"{current_model['accuracy']*100:.2f}%")
            
            with col2:
                st.metric("Precision", f"{current_model['precision']*100:.2f}%")
            
            with col3:
                st.metric("Recall", f"{current_model['recall']*100:.2f}%")
            
            with col4:
                st.metric("F1-Score", f"{current_model['f1']*100:.2f}%")
            
            # Confusion Matrix
            st.markdown("#### 📊 Confusion Matrix")
            
            cm = current_model['confusion_matrix']
            
            # Create annotated heatmap
            z = cm
            x = ['Predicted Ham', 'Predicted Spam']
            y = ['Actual Ham', 'Actual Spam']
            
            z_text = [[str(val) for val in row] for row in z]
            
            fig = ff.create_annotated_heatmap(
                z, x=x, y=y, annotation_text=z_text,
                colorscale='Blues',
                showscale=True
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis=dict(side='bottom'),
                yaxis=dict(side='left')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            tn, fp, fn, tp = cm.ravel()
            
            st.markdown(f"""
            **Confusion Matrix Breakdown:**
            - **True Negatives (TN):** {tn} - Correctly identified as Ham
            - **False Positives (FP):** {fp} - Ham incorrectly flagged as Spam
            - **False Negatives (FN):** {fn} - Spam incorrectly marked as Ham
            - **True Positives (TP):** {tp} - Correctly identified as Spam
            """)
            
            # Performance bar chart
            st.markdown("#### 📊 Performance Metrics Visualization")
            
            metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
            metrics_values = [
                current_model['accuracy'] * 100,
                current_model['precision'] * 100,
                current_model['recall'] * 100,
                current_model['f1'] * 100
            ]
            
            fig = go.Figure(data=[go.Bar(
                x=metrics_names,
                y=metrics_values,
                marker=dict(
                    color=['#667eea', '#764ba2', '#f093fb', '#4facfe'],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=[f"{v:.2f}%" for v in metrics_values],
                textposition='auto',
                textfont=dict(size=16, color='white')
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                xaxis=dict(showgrid=False),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title='Percentage (%)',
                    range=[0, 100]
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        st.success("✅ Model evaluation complete!")
        
    except FileNotFoundError:
        st.error("❌ Dataset not found. Please ensure dataset/spam.csv exists.")
    except Exception as e:
        st.error(f"❌ Error evaluating model: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
    
    # Metrics explanation
    with st.expander("📚 Understanding the Metrics"):
        st.markdown("""
        ### Performance Metrics Explained
        
        **Accuracy:**
        - Percentage of correct predictions (both spam and ham)
        - Formula: (TP + TN) / (TP + TN + FP + FN)
        - Higher is better
        
        **Precision:**
        - Of all messages predicted as spam, how many were actually spam?
        - Formula: TP / (TP + FP)
        - High precision means few false alarms
        
        **Recall (Sensitivity):**
        - Of all actual spam messages, how many did we catch?
        - Formula: TP / (TP + FN)
        - High recall means we catch most spam
        
        **F1-Score:**
        - Harmonic mean of precision and recall
        - Formula: 2 × (Precision × Recall) / (Precision + Recall)
        - Balances precision and recall
        
        ### Why LinearSVC?
        
        - **Fast:** Efficient for text classification
        - **Scalable:** Works well with large feature spaces
        - **Effective:** High accuracy on text data
        - **Proven:** Industry-standard for spam detection
        
        ### Model Limitations
        
        - Cannot detect entirely new spam patterns
        - Performance depends on training data quality
        - May struggle with obfuscated text
        - Requires periodic retraining
        - Language-specific (trained on English)
        """)

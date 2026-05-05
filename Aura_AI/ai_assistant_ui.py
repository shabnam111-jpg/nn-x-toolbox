"""
Aura AI Assistant Module
Interactive Q&A with visualization, calculations, and deep insights
Leverages AI Engine for intelligent responses with neural network analysis
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

from utils.styles import (
    section_header, render_log, gradient_header, inject_global_css, 
    stat_card, render_theory_card
)
from utils.nn_helpers import P, C, G, A, R, TEXT, MUTED, GRID, BG, PLOTLY_BASE, plotly_layout, hex2rgba
from utils.ai_engine import aura_ai

# Initialize AI Engine
@st.cache_resource
def get_ai_engine():
    return aura_ai

def generate_response_analysis(question: str, response: str, answer_type: str = "full"):
    """Generate analysis metrics for the response"""
    # Calculate metrics
    words = response.split()
    sentences = response.split('.')
    keywords = [w for w in words if len(w) > 4]
    
    # Complexity score based on word length and density
    avg_word_len = np.mean([len(w) for w in words]) if words else 0
    complexity = min(100, int(avg_word_len * 8))
    
    # Relevance score based on keyword overlap
    question_words = set(question.lower().split())
    response_words = set(response.lower().split())
    relevance = int(100 * len(question_words & response_words) / max(len(question_words), 1))
    
    # Clarity based on sentence structure
    clarity = min(100, int(100 - (complexity - 50)))
    
    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "complexity": complexity,
        "relevance": relevance,
        "clarity": clarity,
        "avg_word_length": round(avg_word_len, 2),
        "key_concepts": list(set(keywords))[:5]
    }

def create_response_visualization(analysis: dict):
    """Create visualization showing response metrics"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Readability Metrics", "Content Analysis", "Key Metrics", "Complexity Score"),
        specs=[[{"type": "indicator"}, {"type": "bar"}],
               [{"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # Readability indicators
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=analysis["clarity"],
            title="Clarity Score",
            number={'suffix': "%", 'font': {'color': G}}
        ),
        row=1, col=1
    )
    
    # Content bars
    fig.add_trace(
        go.Bar(
            y=["Words", "Sentences", "Keywords"],
            x=[analysis["word_count"], analysis["sentence_count"], len(analysis["key_concepts"])],
            orientation="h",
            marker=dict(color=[P, C, G]),
            text=[analysis["word_count"], analysis["sentence_count"], len(analysis["key_concepts"])],
            textposition="auto"
        ),
        row=1, col=2
    )
    
    # Relevance indicator
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=analysis["relevance"],
            title="Relevance",
            number={'suffix': "%", 'font': {'color': C}}
        ),
        row=2, col=1
    )
    
    # Complexity gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=analysis["complexity"],
            title="Complexity",
            gauge=dict(
                axis=dict(range=[0, 100]),
                bar=dict(color=R),
                steps=[
                    dict(range=[0, 25], color="rgba(0, 245, 160, 0.2)"),
                    dict(range=[25, 50], color="rgba(255, 215, 0, 0.2)"),
                    dict(range=[50, 75], color="rgba(255, 100, 100, 0.2)"),
                    dict(range=[75, 100], color="rgba(255, 23, 68, 0.2)")
                ]
            )
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        **plotly_layout()
    )
    
    return fig

def create_concept_network():
    """Create visualization of related concepts"""
    # Sample concept relationships for neural networks
    concepts = [
        {"name": "Neural Networks", "size": 50},
        {"name": "Perceptron", "size": 35},
        {"name": "Backprop", "size": 35},
        {"name": "Gradients", "size": 30},
        {"name": "Activation", "size": 28},
        {"name": "Weights", "size": 25},
        {"name": "Loss", "size": 25},
    ]
    
    fig = go.Figure(data=[go.Scatter(
        x=np.random.rand(len(concepts)) * 10,
        y=np.random.rand(len(concepts)) * 10,
        mode='markers+text',
        marker=dict(
            size=[c["size"] for c in concepts],
            color=np.linspace(0, 100, len(concepts)),
            colorscale='Viridis',
            showscale=True,
            line=dict(width=2, color='white')
        ),
        text=[c["name"] for c in concepts],
        textposition="middle center",
        textfont=dict(size=12, color='white', family='monospace')
    )])
    
    fig.update_layout(
        title="Concept Relationship Network",
        height=400,
        showlegend=False,
        hovermode='closest',
        **plotly_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    
    return fig

def ai_assistant_page():
    """Main AI Assistant Module"""
    inject_global_css()
    
    # Initialize session state
    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []
    if "ai_engine_ready" not in st.session_state:
        st.session_state.ai_engine_ready = False
    
    # Header
    gradient_header(
        "AI Assistant Studio",
        "Intelligent Q&A with Analysis, Visualization & Calculations",
        "🤖",
        img_path="https://images.unsplash.com/photo-1677442135019-21780ecad995?auto=format&fit=crop&q=90&w=1200"
    )
    
    # Sidebar for AI Configuration
    with st.sidebar:
        section_header("⚙️ Assistant Configuration", "Set your preferences")
        
        # Answer length preference
        answer_type = st.radio(
            "Answer Format",
            ["Brief", "Detailed", "Both"],
            index=1,
            help="Brief: 2-3 sentences | Detailed: Full explanation | Both: Both versions"
        )
        
        # Temperature for creativity
        temperature = st.slider(
            "Creativity Level",
            0.0, 2.0, 0.7, 0.1,
            help="Lower = More focused | Higher = More creative"
        )
        
        # Show calculations
        show_calc = st.checkbox("Show Calculations", True)
        show_concepts = st.checkbox("Show Related Concepts", True)
        show_visualization = st.checkbox("Show Visualizations", True)
        
        st.divider()
        
        section_header("📚 Knowledge Base", "What can I help with?")
        
        st.markdown("""
        **Expertise Areas:**
        - 🧠 Neural Networks & Deep Learning
        - 📊 Machine Learning Algorithms
        - 🎯 Perceptrons & Classification
        - 🔄 Backpropagation & Optimization
        - 📈 Gradient Descent Methods
        - 🎨 Computer Vision & OpenCV
        - 💬 NLP & Sentiment Analysis
        - 🏗️ Neural Architecture Design
        - ⚡ Performance Optimization
        """)
        
        st.divider()
        
        section_header("💾 Conversation History", f"{len(st.session_state.ai_history)} exchanges")
        
        if st.button("🗑️ Clear History"):
            st.session_state.ai_history = []
            st.rerun()
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(96,165,250,0.1), rgba(34,211,238,0.1)); 
                    border: 1px solid rgba(34,211,238,0.3); border-radius: 12px; 
                    padding: 20px; margin-bottom: 20px;">
            <h3 style="margin-top: 0; color: #F1F5F9;">💡 Ask Me Anything</h3>
            <p style="color: #CBD5E1; margin: 0;">
                Ask questions about neural networks, AI, machine learning, or anything else. 
                I'll provide detailed explanations with visualizations and calculations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Question Input
        question = st.text_area(
            "Your Question",
            placeholder="Example: How does backpropagation work? What's the difference between batch and stochastic gradient descent?",
            height=100,
            label_visibility="collapsed"
        )
        
        col_submit, col_clear = st.columns(2)
        with col_submit:
            submit_btn = st.button("🚀 Get Answer", use_container_width=True, type="primary")
        with col_clear:
            if st.button("📋 Example Questions", use_container_width=True):
                st.session_state.show_examples = True
    
    with col2:
        st.metric("Questions Asked", len(st.session_state.ai_history))
        st.metric("Avg Answer Length", 
                 f"{np.mean([len(h.get('response', '').split()) for h in st.session_state.ai_history]) if st.session_state.ai_history else 0:.0f} words")
    
    # Show example questions
    if st.session_state.get("show_examples", False):
        st.markdown("### 📋 Example Questions")
        examples = [
            "How does the perceptron learning rule work?",
            "Explain backpropagation in simple terms",
            "What's the difference between gradient descent variants?",
            "How do neurons in a neural network learn?",
            "What is a decision boundary?",
            "How does activation functions affect learning?",
        ]
        
        cols = st.columns(2)
        for i, ex in enumerate(examples):
            with cols[i % 2]:
                if st.button(f"→ {ex}", use_container_width=True):
                    question = ex
                    submit_btn = True
    
    # Process Question
    if submit_btn and question:
        with st.spinner("🤖 Aura is thinking..."):
            # Generate response
            response = generate_contextual_response(question)
            
            # Generate analysis
            analysis = generate_response_analysis(question, response, answer_type)
            
            # Store in history
            st.session_state.ai_history.append({
                "timestamp": datetime.now(),
                "question": question,
                "response": response,
                "answer_type": answer_type,
                "analysis": analysis
            })
            
            # Display response
            st.markdown("---")
            st.markdown("### 📝 Response")
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📖 Full Answer", "📊 Analytics", "🎓 Breakdown", "💾 History"])
            
            with tab1:
                # Show appropriate answer length
                if answer_type == "Brief":
                    sentences = response.split('.')
                    brief = '. '.join(sentences[:2]) + '.'
                    st.markdown(f"""
                    <div style="background: rgba(34,211,238,0.1); border-left: 4px solid #00D9FF; 
                                padding: 16px; border-radius: 8px; color: #F1F5F9; line-height: 1.8;">
                        <b>Brief Answer:</b><br>{brief}
                    </div>
                    """, unsafe_allow_html=True)
                
                elif answer_type == "Detailed":
                    st.markdown(f"""
                    <div style="background: rgba(34,211,238,0.1); border-left: 4px solid #00D9FF; 
                                padding: 16px; border-radius: 8px; color: #F1F5F9; line-height: 1.8;">
                        <b>Detailed Answer:</b><br>{response}
                    </div>
                    """, unsafe_allow_html=True)
                
                else:  # Both
                    sentences = response.split('.')
                    brief = '. '.join(sentences[:2]) + '.'
                    st.markdown(f"""
                    <div style="background: rgba(52,211,153,0.1); border-left: 4px solid #00F5A0; 
                                padding: 16px; border-radius: 8px; color: #F1F5F9; margin-bottom: 16px; line-height: 1.8;">
                        <b>📌 Quick Summary:</b><br>{brief}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: rgba(34,211,238,0.1); border-left: 4px solid #00D9FF; 
                                padding: 16px; border-radius: 8px; color: #F1F5F9; line-height: 1.8;">
                        <b>📖 Full Explanation:</b><br>{response}
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                if show_visualization:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Word Count", analysis["word_count"])
                        st.metric("Clarity Score", f"{analysis['clarity']}%")
                    with col2:
                        st.metric("Complexity", f"{analysis['complexity']}/100")
                        st.metric("Relevance", f"{analysis['relevance']}%")
                    
                    st.plotly_chart(create_response_visualization(analysis), use_container_width=True)
            
            with tab3:
                st.markdown("**Key Concepts Mentioned:**")
                concept_chips = " ".join([f"🏷️ {c}" for c in analysis["key_concepts"]])
                st.markdown(f"""
                <div style="background: rgba(96,165,250,0.1); padding: 12px; border-radius: 8px; color: #F1F5F9;">
                    {concept_chips}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Metrics:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Word Length", f"{analysis['avg_word_length']} chars")
                with col2:
                    st.metric("Sentences", analysis["sentence_count"])
                with col3:
                    st.metric("Keywords", len(analysis["key_concepts"]))
                
                if show_concepts:
                    st.plotly_chart(create_concept_network(), use_container_width=True)
            
            with tab4:
                st.markdown("**Conversation History:**")
                for i, entry in enumerate(reversed(st.session_state.ai_history[-5:])):
                    with st.expander(f"Q{len(st.session_state.ai_history)-i}: {entry['question'][:50]}...", 
                                   expanded=i==0):
                        st.markdown(f"**Q:** {entry['question']}")
                        st.markdown(f"**A:** {entry['response'][:200]}...")
                        st.caption(f"📊 Complexity: {entry['analysis']['complexity']}/100 | Relevance: {entry['analysis']['relevance']}%")
    
    # Additional Features
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,23,68,0.1), rgba(255,100,100,0.1)); 
                    border: 1px solid rgba(255,23,68,0.3); border-radius: 12px; 
                    padding: 16px; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 8px;">🧠</div>
            <div style="color: #F1F5F9; font-weight: bold;">Neural Networks</div>
            <div style="color: #CBD5E1; font-size: 12px;">Deep learning fundamentals</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(34,211,238,0.1), rgba(0,217,255,0.1)); 
                    border: 1px solid rgba(34,211,238,0.3); border-radius: 12px; 
                    padding: 16px; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 8px;">📊</div>
            <div style="color: #F1F5F9; font-weight: bold;">Visualization</div>
            <div style="color: #CBD5E1; font-size: 12px;">Real-time analysis charts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,245,160,0.1), rgba(52,211,153,0.1)); 
                    border: 1px solid rgba(0,245,160,0.3); border-radius: 12px; 
                    padding: 16px; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 8px;">⚡</div>
            <div style="color: #F1F5F9; font-weight: bold;">Calculations</div>
            <div style="color: #CBD5E1; font-size: 12px;">Instant computation analysis</div>
        </div>
        """, unsafe_allow_html=True)

def generate_contextual_response(question: str) -> str:
    """Generate intelligent response using the shared AI engine"""
    from utils.ai_engine import aura_ai
    from utils.ai_sidebar import build_system_context
    
    response = aura_ai.query_aura(
        question,
        system_context=build_system_context("AI Assistant Studio"),
    )
    return response

if __name__ == "__main__":
    ai_assistant_page()

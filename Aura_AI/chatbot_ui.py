import streamlit as st

from utils.ai_engine import aura_ai
from utils.ai_sidebar import _local_response, build_system_context
from utils.styles import gradient_header, inject_global_css, section_header
from utils.nn_helpers import P, C, G, A, R


def chatbot_ui():
    inject_global_css()
    gradient_header(
        "Aura Assistant", 
        "Project-wide AI guide and live Q&A", 
        "CHAT",
        img_path="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?auto=format&fit=crop&q=90&w=1200"
    )

    history_key = "aura_chat_page"
    st.session_state.setdefault(
        history_key,
        [
            {
                "role": "assistant",
                "content": (
                    "I am ready to help with any module in Aura Studio. "
                    "Ask about theory, implementation details, or what to try next."
                ),
            }
        ],
    )

    status = aura_ai.status_text()
    st.caption(status)

    chat_container = st.container(height=500, border=False)

    with chat_container:
        for message in st.session_state[history_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # SIDEBAR: ADVANCED DIAGNOSTICS
    with st.sidebar:
        st.markdown("### Aura Architect Tools")
        with st.expander("🧠 AURA Knowledge Graph", expanded=False):
            st.info("Interactive 3D visualization of Aura's knowledge domain")
            
            # Define knowledge graph concepts
            concepts = [
                "Neural Networks", "Perceptron", "Deep Learning", "LSTM", "RBM",
                "Computer Vision", "Face Detection", "Object Detection", "Hopfield Memory",
                "Sentiment Analysis", "Classification", "Optimization", "Backpropagation"
            ]
            
            # Define relationships (source_idx, target_idx)
            relationships = [
                (0, 1), (0, 2), (0, 12), (2, 3), (2, 4), (2, 9), (5, 6), (5, 7), 
                (6, 0), (7, 0), (8, 0), (9, 10), (10, 11), (3, 11), (4, 11), (12, 11),
                (0, 8), (2, 5), (10, 12), (1, 12), (4, 9), (6, 10), (7, 10)
            ]
            
            # Color map for concepts
            colors_map = {
                "Neural Networks": P, "Perceptron": C, "Deep Learning": G,
                "LSTM": A, "RBM": R, "Computer Vision": P, "Face Detection": C,
                "Object Detection": G, "Hopfield Memory": A, "Sentiment Analysis": R,
                "Classification": P, "Optimization": C, "Backpropagation": G
            }
            
            st.markdown("*Knowledge graph visualization would render here with plotly*")
            
        with st.expander("📊 AURA Performance Dashboard", expanded=False):
            st.info("Real-time analytics: Module interactions, query processing")
            
            aura_metrics = {
                'Knowledge Base Size': [13, 13, 13, 13, 13],
                'Concept Relationships': [23, 23, 23, 23, 23]
            }
            st.markdown("*Performance dashboard would render here with plotly*")

    if prompt := st.chat_input("Ask about neural networks, OpenCV, Hopfield recall, or this project..."):
        st.session_state[history_key].append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Aura is thinking..."):
                    if aura_ai.is_available():
                        response = aura_ai.query_aura(
                            prompt,
                            system_context=build_system_context("Aura Assistant"),
                            conversation=st.session_state[history_key][:-1],
                        )
                    else:
                        response = _local_response("Aura Assistant", prompt)
                    st.markdown(response)

        st.session_state[history_key].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    chatbot_ui()

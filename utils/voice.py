"""
Voice/Audio utilities for Aura AI Studio
Optional voice narration and audio feedback
"""

import streamlit as st


def render_voice_button(text, key_suffix="default", label="🔊 Hear Reading"):
    """
    Render voice button for optional audio narration.
    
    Args:
        text: Text to narrate
        key_suffix: Unique suffix for streamlit key
        label: Button label
    """
    try:
        import pyttsx3
        
        col = st.columns([1, 4])[0]
        with col:
            if st.button(label, key=f"voice_{key_suffix}", use_container_width=True):
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.say(text)
                    engine.runAndWait()
                    st.success("✅ Audio played")
                except Exception:
                    st.info("🔊 Voice feature unavailable")
    except ImportError:
        # pyttsx3 not installed - silent pass
        pass


def text_to_speech(text, output_file=None):
    """
    Convert text to speech.
    
    Args:
        text: Text to convert
        output_file: Optional output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        if output_file:
            engine.save_to_file(text, output_file)
        
        engine.runAndWait()
        return True
    except (ImportError, Exception):
        return False


def render_audio_player(audio_bytes, label="Play Audio"):
    """
    Render audio player component.
    
    Args:
        audio_bytes: Audio file bytes
        label: Player label
    """
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3", label=label)

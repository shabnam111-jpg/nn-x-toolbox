"""
Palm Detection and Analysis Integration Module
Integrates MediaPipe hand detection with advanced palmistry analysis.
Maintains consistent UI/UX with neon cyberpunk theme.
"""

import os
import sys
import cv2
import numpy as np
import streamlit as st
from pathlib import Path
from functools import lru_cache
from typing import Optional, Dict, Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════════════════════
# OPTIONAL IMPORTS - GRACEFUL FALLBACK
# ═════════════════════════════════════════════════════════════════════════════

# Lazy import - only loads when function is called
HAS_MEDIAPIPE = None

def _check_mediapipe():
    global HAS_MEDIAPIPE
    if HAS_MEDIAPIPE is None:
        try:
            import mediapipe as mp
            HAS_MEDIAPIPE = True
        except ImportError:
            HAS_MEDIAPIPE = False
    return HAS_MEDIAPIPE

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    logger.warning("PIL not installed. Image processing will be limited.")

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

# Asset paths
ASSETS_DIR = Path(__file__).parent.parent / "assets"
PALM_ASSETS_DIR = ASSETS_DIR / "palm"
HAND_LANDMARK_MODEL = PALM_ASSETS_DIR / "hand_landmarker.task"

# MediaPipe configurations
MP_HANDS_STATIC_IMAGE_MODE = True
MP_HANDS_MAX_NUM_HANDS = 1
MP_HANDS_MIN_DETECTION_CONFIDENCE = 0.7
MP_HANDS_MIN_TRACKING_CONFIDENCE = 0.5

# Palm line names in order of index
PALM_LINES = ['Life', 'Head', 'Heart', 'Fate', 'Mercury']

# Neon color palette (RGB)
COLORS = {
    'cyan': (34, 211, 238),      # Cyan
    'indigo': (129, 140, 248),   # Indigo
    'rose': (251, 113, 133),     # Rose
    'emerald': (52, 211, 169),   # Emerald
    'gold': (253, 224, 71),      # Gold
}

# ═════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1)
def load_hand_detector():
    """
    Load MediaPipe hand detection model with caching.
    Returns detector or None if not available.
    """
    if not _check_mediapipe():
        logger.warning("MediaPipe not available for hand detection")
        return None
    
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands_detector = mp_hands.Hands(
            static_image_mode=MP_HANDS_STATIC_IMAGE_MODE,
            max_num_hands=MP_HANDS_MAX_NUM_HANDS,
            min_detection_confidence=MP_HANDS_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MP_HANDS_MIN_TRACKING_CONFIDENCE,
        )
        logger.info("✓ Hand detector loaded successfully")
        return hands_detector
    except Exception as e:
        logger.error(f"Failed to load hand detector: {e}")
        return None

def detect_hand_landmarks(image_input) -> Optional[Dict]:
    """
    Detect hand landmarks in an image using MediaPipe.
    
    Args:
        image_input: numpy array or PIL Image
    
    Returns:
        Dictionary with landmark data or None
    """
    if not _check_mediapipe():
        logger.warning("MediaPipe not available")
        return None
    
    try:
        # Convert PIL to numpy if needed
        if HAS_PIL and isinstance(image_input, Image.Image):
            image_array = np.array(image_input)
        else:
            image_array = np.array(image_input)
        
        # Ensure RGB format
        if len(image_array.shape) == 3:
            if image_array.shape[2] == 4:  # RGBA
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            elif image_array.shape[2] == 3:  # BGR
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        # Load detector
        hands_detector = load_hand_detector()
        if hands_detector is None:
            return None
        
        # Detect landmarks
        results = hands_detector.process(image_array)
        
        if not results.multi_hand_landmarks:
            logger.info("No hand detected in image")
            return None
        
        # Extract first hand (if multiple detected)
        landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label
        
        # Convert landmarks to coordinates
        h, w = image_array.shape[:2]
        landmark_coords = []
        for lm in landmarks.landmark:
            x = int(lm.x * w)
            y = int(lm.y * h)
            z = lm.z
            landmark_coords.append({'x': x, 'y': y, 'z': z})
        
        logger.info(f"✓ Detected {len(landmark_coords)} hand landmarks ({handedness})")
        
        return {
            'landmarks': landmark_coords,
            'handedness': handedness,
            'image_shape': image_array.shape,
            'confidence': results.multi_handedness[0].classification[0].score,
        }
        
    except Exception as e:
        logger.error(f"Error in hand detection: {e}")
        return None

def extract_palm_features(landmark_data: Dict) -> Optional[Dict]:
    """
    Extract palm reading features from hand landmarks.
    
    Args:
        landmark_data: Output from detect_hand_landmarks
    
    Returns:
        Dictionary with extracted palm features
    """
    if not landmark_data:
        return None
    
    try:
        landmarks = landmark_data['landmarks']
        
        # Palm point indices (MediaPipe hand model)
        WRIST = 0
        THUMB_MCP = 2
        INDEX_MCP = 5
        MIDDLE_MCP = 9
        RING_MCP = 13
        PINKY_MCP = 17
        
        # Extract key points for palm analysis
        wrist = np.array([landmarks[WRIST]['x'], landmarks[WRIST]['y']])
        thumb_base = np.array([landmarks[THUMB_MCP]['x'], landmarks[THUMB_MCP]['y']])
        index_base = np.array([landmarks[INDEX_MCP]['x'], landmarks[INDEX_MCP]['y']])
        middle_base = np.array([landmarks[MIDDLE_MCP]['x'], landmarks[MIDDLE_MCP]['y']])
        ring_base = np.array([landmarks[RING_MCP]['x'], landmarks[RING_MCP]['y']])
        pinky_base = np.array([landmarks[PINKY_MCP]['x'], landmarks[PINKY_MCP]['y']])
        
        # Calculate palm measurements
        palm_width = np.linalg.norm(thumb_base - pinky_base)
        palm_height = np.linalg.norm(middle_base - wrist)
        palm_area = palm_width * palm_height
        
        # Analyze hand spread
        hand_spread = np.linalg.norm(index_base - ring_base)
        
        # Calculate average confidence
        avg_z = np.mean([lm['z'] for lm in landmarks])
        
        features = {
            'palm_width': float(palm_width),
            'palm_height': float(palm_height),
            'palm_area': float(palm_area),
            'hand_spread': float(hand_spread),
            'aspect_ratio': float(palm_width / palm_height) if palm_height > 0 else 0,
            'depth_confidence': float(avg_z),
            'total_landmarks': len(landmarks),
            'handedness': landmark_data['handedness'],
            'detection_confidence': float(landmark_data['confidence']),
        }
        
        logger.info(f"✓ Extracted palm features: {list(features.keys())}")
        return features
        
    except Exception as e:
        logger.error(f"Error extracting palm features: {e}")
        return None

def draw_palm_landmarks(image_input, landmark_data: Dict) -> Optional[np.ndarray]:
    """
    Draw hand landmarks on image with neon styling.
    
    Args:
        image_input: Input image (numpy array or PIL Image)
        landmark_data: Output from detect_hand_landmarks
    
    Returns:
        Image with drawn landmarks or None
    """
    if not landmark_data or not HAS_PIL:
        return None
    
    try:
        # Convert to numpy array
        if isinstance(image_input, Image.Image):
            image_array = np.array(image_input)
        else:
            image_array = np.array(image_input)
        
        # Convert RGB to BGR for OpenCV
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        landmarks = landmark_data['landmarks']
        
        # Draw connections (palm lines)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),      # Index (potential Head line)
            (0, 9), (9, 10), (10, 11), (11, 12), # Middle (potential Life line)
            (0, 13), (13, 14), (14, 15), (15, 16), # Ring (potential Heart line)
            (0, 17), (17, 18), (18, 19), (19, 20), # Pinky (potential Fate line)
            (5, 9), (9, 13), (13, 17),           # Palm base connections
        ]
        
        color_palette = [COLORS['cyan'], COLORS['indigo'], COLORS['rose'], 
                        COLORS['emerald'], COLORS['gold']]
        
        # Draw lines
        for idx, (start, end) in enumerate(connections):
            if start < len(landmarks) and end < len(landmarks):
                p1 = (landmarks[start]['x'], landmarks[start]['y'])
                p2 = (landmarks[end]['x'], landmarks[end]['y'])
                color = color_palette[idx % len(color_palette)]
                cv2.line(image_array, p1, p2, color, 2)
        
        # Draw landmarks as circles
        for idx, lm in enumerate(landmarks):
            center = (lm['x'], lm['y'])
            color = color_palette[idx % len(color_palette)]
            cv2.circle(image_array, center, 4, color, -1)
            cv2.circle(image_array, center, 5, (255, 255, 255), 1)
        
        # Convert back to RGB
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        logger.info("✓ Landmarks drawn successfully")
        return image_array
        
    except Exception as e:
        logger.error(f"Error drawing landmarks: {e}")
        return None

# ═════════════════════════════════════════════════════════════════════════════
# STREAMLIT INTEGRATION FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def render_palm_detection_ui():
    """
    Render palm detection UI component with Streamlit.
    Integrated with neon theme.
    """
    st.markdown("""
        <style>
        .palm-detection-container {
            background: linear-gradient(135deg, rgba(129, 140, 248, 0.1) 0%, rgba(52, 211, 169, 0.1) 100%);
            border: 2px solid #818CF8;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px rgba(129, 140, 248, 0.3), inset 0 0 20px rgba(129, 140, 248, 0.1);
        }
        .palm-title {
            color: #22D3EE;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0 0 10px #22D3EE;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="palm-title">🌙 Palm Analysis</div>', unsafe_allow_html=True)
        st.write("Upload a palm image for detailed analysis with AI-powered insights.")
    
    with col2:
        if not _check_mediapipe():
            st.warning("⚠️ MediaPipe not installed - limited detection capabilities")
        else:
            st.success("✓ Hand detection ready")
    
    return True

def process_palm_image(uploaded_file) -> Optional[Dict]:
    """
    Process uploaded palm image with full analysis pipeline.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        Dictionary with complete analysis results
    """
    if not uploaded_file:
        return None
    
    try:
        # Load image
        if HAS_PIL:
            image = Image.open(uploaded_file)
        else:
            image_array = np.frombuffer(uploaded_file.read(), np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Detect landmarks
        landmark_data = detect_hand_landmarks(image)
        if not landmark_data:
            return {'error': 'No hand detected in image. Please try another image.'}
        
        # Extract features
        palm_features = extract_palm_features(landmark_data)
        if not palm_features:
            return {'error': 'Could not extract palm features. Please try again.'}
        
        # Draw landmarks
        annotated_image = draw_palm_landmarks(image, landmark_data)
        
        # Prepare results
        results = {
            'original_image': image,
            'annotated_image': annotated_image,
            'landmark_data': landmark_data,
            'palm_features': palm_features,
            'success': True,
        }
        
        logger.info("✓ Palm image processing completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Error processing palm image: {e}")
        return {'error': f'Error processing image: {str(e)}'}

# ═════════════════════════════════════════════════════════════════════════════
# VERSION & HEALTH CHECK
# ═════════════════════════════════════════════════════════════════════════════

def get_palm_detection_info() -> Dict:
    """Get information about palm detection module status."""
    return {
        'module': 'Palm Detection Integration',
        'version': '1.0.0',
        'mediapipe_available': _check_mediapipe(),
        'pil_available': HAS_PIL,
        'model_path': str(HAND_LANDMARK_MODEL),
        'model_exists': HAND_LANDMARK_MODEL.exists() if PALM_ASSETS_DIR.exists() else False,
        'assets_dir': str(PALM_ASSETS_DIR),
    }

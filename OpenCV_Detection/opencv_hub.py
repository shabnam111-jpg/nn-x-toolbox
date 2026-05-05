from __future__ import annotations

import datetime
import os
import tempfile
import time

try:
    import cv2
    OPENCV_READY = True
except ImportError:
    OPENCV_READY = False
import numpy as np
import pandas as pd
import streamlit as st

from utils.palmistry_engine import (
    answer_palm_question,
    build_palm_report,
)
from utils.styles import section_header, gradient_header, render_content_card, render_info_grid, MODULE_THEMES, inject_module_theme

os.environ.setdefault("NO_ALBUMENTATIONS_UPDATE", "1")

try:
    from streamlit_webrtc import webrtc_streamer, RTCConfiguration
    import av

    WEBRTC_READY = True
except ImportError:
    WEBRTC_READY = False

if WEBRTC_READY:
    RTC_CONFIG_LOCAL = RTCConfiguration({"iceServers": []})
    RTC_CONFIG_STUN = RTCConfiguration(
        {
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                {"urls": ["stun:stun1.l.google.com:19302"]},
                {"urls": ["stun:stun2.l.google.com:19302"]},
            ]
        }
    )
else:
    RTC_CONFIG_LOCAL = None
    RTC_CONFIG_STUN = None

LIVE_INPUT_SOURCES = ["📷 Photo", "📸 Camera Snapshot", "🔴 Live WebRTC", "📹 Video File"]
LIVE_MEDIA_STREAM_CONSTRAINTS = {
    "video": {
        "width": {"ideal": 640},
        "height": {"ideal": 480},
        "frameRate": {"ideal": 15, "max": 24},
    },
    "audio": False,
}

CV_GALLERY_PATH = "OpenCV_Detection/page_gallery.py"

CV_MODULES = [
    {
        "key": "attendance",
        "icon": "📋",
        "title": "Attendance",
        "gallery_subtitle": "Face log · Export CSV",
        "page_title": "OpenCV Attendance Studio",
        "page_subtitle": "Face logging, registration, and CSV-ready attendance tracking",
        "path": "OpenCV_Detection/page_attendance.py",
        "banner": os.path.join("assets", "banners", "attendance_banner_1774323273637.png"),
        "features": ["Real-time Face Detection", "User Registration", "CSV Attendance Export"],
    },
    {
        "key": "face_scan",
        "icon": "🔍",
        "title": "Face Scanner",
        "gallery_subtitle": "Eyes · Smile · ROI",
        "page_title": "OpenCV Face Scanner",
        "page_subtitle": "Multi-cascade face analysis with eyes, smile, and region tracking",
        "path": "OpenCV_Detection/page_face_scan.py",
        "banner": os.path.join("assets", "banners", "face_scanner_banner_1774323291585.png"),
        "features": ["Multi-Cascade Detection", "Ocular Tracking", "Mood and Smile Recognition"],
    },
    {
        "key": "vehicle",
        "icon": "🚗",
        "title": "Vehicles",
        "gallery_subtitle": "Traffic · Live Counting",
        "page_title": "OpenCV Vehicle Detection",
        "page_subtitle": "YOLO-powered traffic counting and live vehicle analytics",
        "path": "OpenCV_Detection/page_vehicle.py",
        "banner": os.path.join("assets", "banners", "vehicles_banner_1774323308501.png"),
        "features": ["YOLOv8 Inference", "Vehicle Classification", "Live Stats"],
    },
    {
        "key": "sign",
        "icon": "🛑",
        "title": "Sign Detection",
        "gallery_subtitle": "Shapes · Colors",
        "page_title": "OpenCV Sign Detection",
        "page_subtitle": "Color filtering and contour analysis for road-sign style recognition",
        "path": "OpenCV_Detection/page_sign.py",
        "banner": os.path.join("assets", "banners", "sign_detection_banner_1774323328063.png"),
        "features": ["Color Space Filtering", "Contour Analysis", "Symbolic Recognition"],
    },
    {
        "key": "palm",
        "icon": "🖐️",
        "title": "Palm Reading",
        "gallery_subtitle": "Hands · Gestures",
        "page_title": "OpenCV Palm Reading",
        "page_subtitle": "Hand segmentation, feature extraction, and palm-line overlays",
        "path": "OpenCV_Detection/page_palm.py",
        "banner": os.path.join("assets", "banners", "palm_reading_banner_1774323346147.png"),
        "features": ["CNN Segmentation", "Feature Extraction", "Career Analysis"],
    },
]

CV_MODULE_MAP = {item["key"]: item for item in CV_MODULES}
CV_NAV_GALLERY = "cv_gallery"
CV_NAV_BY_MODULE_KEY = {
    "attendance": "cv_attendance",
    "face_scan": "cv_face_scan",
    "vehicle": "cv_vehicle",
    "sign": "cv_sign",
    "palm": "cv_palm",
}

CV_MODULE_PREVIEW_COLORS = {
    "attendance": ("#0EA5E9", "#1E293B", "#22C55E"),
    "face_scan": ("#6366F1", "#0F172A", "#22D3EE"),
    "vehicle": ("#0F766E", "#1E293B", "#F59E0B"),
    "sign": ("#DC2626", "#1F2937", "#FACC15"),
    "palm": ("#9333EA", "#0F172A", "#FB7185"),
}


def process_video_realtime(video_file, callback_fn):
    """Processes an uploaded video file frame-by-frame with a callback."""
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(video_file.read())
    tfile.close()
    
    cap = cv2.VideoCapture(tfile.name)
    st_frame = st.empty()
    
    stop_btn = st.button("⏹ Stop Processing", key=f"stop_{video_file.name}")
    
    while cap.isOpened() and not stop_btn:
        ret, frame = cap.read()
        if not ret: break
        
        # Process frame
        processed_frame = callback_fn(frame)
        
        # Display
        st_frame.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), use_column_width=True)
        time.sleep(0.01) # Small delay for UI stability
        
    cap.release()
    os.unlink(tfile.name)
    st.success("Video Processing Complete!")


def _decode_image_file(file_obj):
    if file_obj is None:
        return None
    data = np.frombuffer(file_obj.getvalue(), np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def _hex_to_bgr(color_hex):
    clean = color_hex.lstrip("#")
    if len(clean) != 6:
        return (120, 120, 120)
    return (int(clean[4:6], 16), int(clean[2:4], 16), int(clean[0:2], 16))


@st.cache_data(show_spinner=False)
def _build_module_preview(module_key, title):
    h, w = 220, 380
    start_hex, end_hex, accent_hex = CV_MODULE_PREVIEW_COLORS.get(module_key, ("#334155", "#0F172A", "#22D3EE"))
    start = np.array(_hex_to_bgr(start_hex), dtype=np.float32)
    end = np.array(_hex_to_bgr(end_hex), dtype=np.float32)

    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    blend = np.linspace(0.0, 1.0, w, dtype=np.float32)
    for c in range(3):
        row = (start[c] * (1.0 - blend) + end[c] * blend).astype(np.uint8)
        canvas[:, :, c] = np.tile(row, (h, 1))

    accent = _hex_to_bgr(accent_hex)
    cv2.rectangle(canvas, (8, 8), (w - 8, h - 8), accent, 2)

    if module_key == "attendance":
        cv2.rectangle(canvas, (28, 44), (150, 172), (236, 245, 255), 2)
        for row in range(3):
            y = 72 + row * 30
            cv2.line(canvas, (45, y), (95, y), (236, 245, 255), 2)
            cv2.circle(canvas, (120, y), 6, (52, 211, 153), -1)
    elif module_key == "face_scan":
        cv2.circle(canvas, (100, 108), 58, (236, 245, 255), 2)
        cv2.circle(canvas, (78, 96), 8, (34, 211, 238), -1)
        cv2.circle(canvas, (122, 96), 8, (34, 211, 238), -1)
        cv2.ellipse(canvas, (100, 124), (24, 14), 0, 0, 180, (236, 245, 255), 2)
        cv2.rectangle(canvas, (170, 58), (330, 160), (236, 245, 255), 2)
        cv2.line(canvas, (170, 92), (330, 92), accent, 2)
        cv2.line(canvas, (170, 124), (330, 124), accent, 2)
    elif module_key == "vehicle":
        cv2.rectangle(canvas, (48, 112), (278, 156), (236, 245, 255), -1)
        cv2.rectangle(canvas, (96, 88), (236, 118), (236, 245, 255), -1)
        cv2.circle(canvas, (98, 162), 18, (15, 23, 42), -1)
        cv2.circle(canvas, (236, 162), 18, (15, 23, 42), -1)
        cv2.circle(canvas, (98, 162), 8, (148, 163, 184), -1)
        cv2.circle(canvas, (236, 162), 8, (148, 163, 184), -1)
    elif module_key == "sign":
        sign = np.array([[86, 56], [134, 56], [166, 88], [166, 136], [134, 168], [86, 168], [54, 136], [54, 88]], np.int32)
        cv2.fillPoly(canvas, [sign], (220, 38, 38))
        cv2.polylines(canvas, [sign], True, (255, 255, 255), 3)
        cv2.putText(canvas, "STOP", (68, 121), cv2.FONT_HERSHEY_DUPLEX, 0.95, (255, 255, 255), 2, cv2.LINE_AA)
    elif module_key == "palm":
        palm_outline = np.array([[86, 170], [72, 138], [76, 98], [92, 74], [110, 64], [126, 70], [138, 58], [154, 64], [166, 52], [184, 60], [194, 78], [202, 102], [198, 146], [182, 176], [152, 188], [120, 188]], np.int32)
        cv2.polylines(canvas, [palm_outline], True, (236, 245, 255), 2)
        cv2.line(canvas, (98, 136), (182, 122), (244, 114, 182), 2)
        cv2.line(canvas, (98, 152), (170, 160), (34, 211, 238), 2)
        cv2.line(canvas, (106, 120), (166, 96), (52, 211, 153), 2)

    cv2.putText(canvas, title.upper(), (20, h - 24), cv2.FONT_HERSHEY_DUPLEX, 0.72, accent, 2, cv2.LINE_AA)
    cv2.putText(canvas, "MODULE PREVIEW", (20, h - 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (236, 245, 255), 1, cv2.LINE_AA)

    return cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)


@st.cache_data(show_spinner=False)
def _gallery_preview_for_module(module_key, title, banner_path):
    if banner_path and os.path.exists(banner_path):
        banner_img = cv2.imread(banner_path)
        if banner_img is not None:
            return cv2.cvtColor(banner_img, cv2.COLOR_BGR2RGB)
    return _build_module_preview(module_key, title)


def _load_image_from_source(src, upload_label, upload_key, camera_label, camera_key):
    if src == "📷 Photo":
        return _decode_image_file(st.file_uploader(upload_label, type=["jpg", "jpeg", "png"], key=upload_key))
    if src == "📸 Camera Snapshot":
        return _decode_image_file(st.camera_input(camera_label, key=camera_key))
    return None


def _rtc_configuration_selector(key_prefix):
    if not WEBRTC_READY:
        return None

    st.caption(
        "Low-latency local mode is the default and avoids STUN. Turn STUN on only when the app is running remotely and the live stream will not connect."
    )
    use_stun = st.toggle("Use STUN servers", value=False, key=f"{key_prefix}_use_stun")
    return RTC_CONFIG_STUN if use_stun else RTC_CONFIG_LOCAL


def _start_webrtc_stream(stream_key, callback, label, key_prefix, hint=None):
    if not WEBRTC_READY:
        st.error("`streamlit-webrtc` is missing. Install it to enable live camera streaming.")
        return

    st.markdown(f"**{label}**")
    if hint:
        st.caption(hint)

    webrtc_streamer(
        key=stream_key,
        video_frame_callback=callback,
        rtc_configuration=_rtc_configuration_selector(key_prefix),
        media_stream_constraints=LIVE_MEDIA_STREAM_CONSTRAINTS,
        async_processing=True,
    )

def draw_cyber_hud(img, x, y, w, h, label, color_bgr):
    """Draws a futuristic HUD overlay rectangle around a detected object."""
    thick = max(1, min(w, h) // 100 + 2)
    length = max(15, min(w, h) // 4)
    # Corner brackets
    # Top-left
    cv2.line(img, (x, y), (x + length, y), color_bgr, thick)
    cv2.line(img, (x, y), (x, y + length), color_bgr, thick)
    # Top-right
    cv2.line(img, (x + w, y), (x + w - length, y), color_bgr, thick)
    cv2.line(img, (x + w, y), (x + w, y + length), color_bgr, thick)
    # Bottom-left
    cv2.line(img, (x, y + h), (x + length, y + h), color_bgr, thick)
    cv2.line(img, (x, y + h), (x, y + h - length), color_bgr, thick)
    # Bottom-right
    cv2.line(img, (x + w, y + h), (x + w - length, y + h), color_bgr, thick)
    cv2.line(img, (x + w, y + h), (x + w, y + h - length), color_bgr, thick)
    
    # Semi-transparent inner fill
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color_bgr, -1)
    cv2.addWeighted(overlay, 0.12, img, 0.88, 0, img)
    
    # Label with background
    if label:
        display_label = f" {label} "
        (lw, lh), _ = cv2.getTextSize(display_label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.rectangle(img, (x, max(0, y - lh - 12)), (x + lw, y), color_bgr, -1)
        # Use dark text for contrast
        text_color = (15, 23, 42) if sum(color_bgr) > 300 else (255, 255, 255)
        cv2.putText(img, display_label, (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, text_color, 2, cv2.LINE_AA)


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 1 — ATTENDANCE SYSTEM
# ═════════════════════════════════════════════════════════════════════════════
def _attendance_module():
    section_header("Face Log & Attendance", "Match Faces · Export CSV")
    # render_nlp_insight removed - now in chatbot
    if "cv_attendance" not in st.session_state: st.session_state.cv_attendance=[]

    c1,c2=st.columns([1,1])
    with c1:
        reg_name=st.text_input("Full Name (Target)", placeholder="e.g. Clark Kent", key="cv_reg_name")
        reg_id=st.text_input("ID / Roll No.", placeholder="e.g. DC-001", key="cv_reg_id")
        
        st.divider()
        src = st.radio("Input Source", LIVE_INPUT_SOURCES, horizontal=True, key="cv_att_src")
        
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        def _att_cb(img):
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(30,30))
                for idx, (x, y, w, h) in enumerate(faces):
                    person = reg_name if reg_name else f"PERSON {idx+1}"
                    draw_cyber_hud(img, x, y, w, h, person, (0, 91, 234))
                # Metrics Overlay
                cv2.putText(img, f"TARGETS: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            except Exception as e:
                pass
            return img

        if src in ("📷 Photo", "📸 Camera Snapshot"):
            img = _load_image_from_source(
                src,
                "Upload Target Photo",
                "cv_att_photo",
                "Capture Target Photo",
                "cv_att_camera",
            )
            if img is not None and st.button("📸 Detect & Register", type="primary", use_container_width=True):
                processed = _att_cb(img.copy())
                st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_column_width=True)

        elif src == "📹 Video File":
             v = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="cv_att_video")
             if v: process_video_realtime(v, _att_cb)

        else:
            st.markdown("**Live WebRTC Camera**")
            def face_log_callback(frame: av.VideoFrame) -> av.VideoFrame:
                try:
                    # Frame skipping
                    if 'att_frame_count' not in st.session_state: st.session_state.att_frame_count = 0
                    st.session_state.att_frame_count += 1
                    if st.session_state.att_frame_count % 2 != 0: return frame
                    
                    img = frame.to_ndarray(format="bgr24")
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(40,40))
                    
                    for idx, (x,y,w,h) in enumerate(faces):
                        person = reg_name if reg_name else f"TARGET {idx+1}"
                        draw_cyber_hud(img, x, y, w, h, person.upper(), (239, 68, 68)) # Flash Red HUD
                    
                    # Live tracking metrics
                    cv2.putText(img, f"LIVE TRACKS: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (239, 68, 68), 2)
                    return av.VideoFrame.from_ndarray(img, format="bgr24")
                except Exception:
                    return frame

            _start_webrtc_stream(
                "att_stream",
                face_log_callback,
                "Live WebRTC Camera",
                "att_stream",
                hint="If live streaming still fails in your setup, switch to Camera Snapshot above for a no-STUN fallback.",
            )

    with c2:
        section_header("Attendance Log", f"{len(st.session_state.cv_attendance)} entries")
        st.info("Log your attendance manually after detection.")
        if st.button("Log Current Detection"):
            st.session_state.cv_attendance.append({
                "Timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "Name": reg_name or "Unknown", "ID": reg_id or "N/A", "Status": "Present"
            })
            st.rerun()

        if st.session_state.cv_attendance:
            df = pd.DataFrame(st.session_state.cv_attendance)
            st.dataframe(df, hide_index=True, use_container_width=True)
            if st.button("🗑 Clear Log", use_container_width=True):
                st.session_state.cv_attendance=[]; st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 2 — FACE SCANNER
# ═════════════════════════════════════════════════════════════════════════════
def _face_scan_module():
    section_header("Face Scanner", "Multi-Cascade · Eyes & Smiles")
    
    src = st.radio("Input Source", LIVE_INPUT_SOURCES, horizontal=True, key="cv_fs_src")
    
    face_cas = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    eye_cas = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_eye.xml")
    smile_cas = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_smile.xml")

    def _fs_cb(img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cas.detectMultiScale(gray, 1.1, 5, minSize=(40,40))
            for (x,y,w,h) in faces:
                draw_cyber_hud(img, x, y, w, h, "FACE DETECTED", (242, 169, 0))
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                
                # Eyes
                eyes = eye_cas.detectMultiScale(roi_gray, 1.1, 5)
                for (ex,ey,ew,eh) in eyes: 
                    draw_cyber_hud(roi_color, ex, ey, ew, eh, "", (0,177,64))
                
                # Smiles
                smiles = smile_cas.detectMultiScale(roi_gray, 1.8, 20)
                for (sx,sy,sw,sh) in smiles: 
                    draw_cyber_hud(roi_color, sx, sy, sw, sh, "SMILE", (237, 29, 36))
            
            cv2.putText(img, f"SCANNER ACTIVE | FACES: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (242, 169, 0), 2)
        except Exception:
            pass
        return img

    if src in ("📷 Photo", "📸 Camera Snapshot"):
        img = _load_image_from_source(
            src,
            "Upload Photo",
            "fs_photo",
            "Capture Photo",
            "fs_camera",
        )
        if img is not None:
            processed = _fs_cb(img.copy())
            st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_column_width=True)
    elif src == "📹 Video File":
        v = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="fs_video")
        if v: process_video_realtime(v, _fs_cb)
    else:
        def face_scan_callback(frame: av.VideoFrame) -> av.VideoFrame:
            try:
                # Frame skipping
                if 'fs_frame_count' not in st.session_state: st.session_state.fs_frame_count = 0
                st.session_state.fs_frame_count += 1
                if st.session_state.fs_frame_count % 2 != 0: return frame

                img = frame.to_ndarray(format="bgr24")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cas.detectMultiScale(gray, 1.1, 5, minSize=(40,40))
                for (x,y,w,h) in faces:
                    draw_cyber_hud(img, x, y, w, h, "FACE TRACKER", (250, 204, 21)) # Yellow UI
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
                    eyes = eye_cas.detectMultiScale(roi_gray, 1.1, 5)
                    for (ex,ey,ew,eh) in eyes: draw_cyber_hud(roi_color, ex, ey, ew, eh, "", (22, 197, 94))
                    smiles = smile_cas.detectMultiScale(roi_gray, 1.8, 20)
                    for (sx,sy,sw,sh) in smiles: draw_cyber_hud(roi_color, sx, sy, sw, sh, "+SMILE", (239, 68, 68))
                
                cv2.putText(img, f"OPS: FACE SCAN | SUBJECTS: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (250, 204, 21), 2)
                return av.VideoFrame.from_ndarray(img, format="bgr24")
            except Exception:
                return frame

        _start_webrtc_stream(
            "face_scan_stream",
            face_scan_callback,
            "Live WebRTC Camera",
            "face_scan_stream",
            hint="The stream runs at a lower default resolution for faster face detection.",
        )


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 3 — VEHICLES (YOLO MOCK / CASCADE)
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_yolo_model():
    """Shared global cache for the YOLO detector."""
    try:
        from ultralytics import YOLO
        return YOLO('yolov8n.pt')
    except Exception as e:
        st.error(f"Failed to load YOLO: {e}")
        return None

def _vehicle_module():
    section_header("Vehicle Detection", "YOLOv8 Real-Time Counting")
    
    src = st.radio("Input Source", LIVE_INPUT_SOURCES, horizontal=True, key="cv_vd_src")
    
    model = load_yolo_model()
    if model is None: return

    def _vd_cb(img):
        try:
            results = model(img, verbose=False, imgsz=640)[0]
            count = 0
            for box in results.boxes:
                cls = int(box.cls[0])
                name = results.names[cls]
                if name in ['car', 'truck', 'bus', 'motorcycle', 'person']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    draw_cyber_hud(img, x1, y1, x2 - x1, y2 - y1, f"{name.upper()} {conf:.2f}", (0, 212, 255))
                    count += 1
            cv2.putText(img, f"YOLOv8 | TICK: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 212, 255), 2)
        except Exception:
            pass
        return img

    if src in ("📷 Photo", "📸 Camera Snapshot"):
        img = _load_image_from_source(
            src,
            "Upload Image",
            "vd_photo",
            "Capture Image",
            "vd_camera",
        )
        if img is not None:
            processed = _vd_cb(img.copy())
            st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_column_width=True)
    elif src == "📹 Video File":
        v = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="vd_video")
        if v: process_video_realtime(v, _vd_cb)
    else:
        st.info("Live YOLOv8 Inference Running...")
        model = load_yolo_model()
        if model is None: return

        def vehicle_callback(frame: av.VideoFrame) -> av.VideoFrame:
            try:
                # Frame skipping (YOLO is heavy)
                if 'vd_frame_count' not in st.session_state: st.session_state.vd_frame_count = 0
                st.session_state.vd_frame_count += 1
                if st.session_state.vd_frame_count % 3 != 0: return frame

                img = frame.to_ndarray(format="bgr24")
                results = model(img, verbose=False, imgsz=416)[0]
                count = 0
                for box in results.boxes:
                    cls = int(box.cls[0])
                    name = results.names[cls]
                    if name in ['car', 'truck', 'bus', 'motorcycle', 'person']:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        draw_cyber_hud(img, x1, y1, x2 - x1, y2 - y1, f"{name.upper()} {conf:.2f}", (249, 115, 22)) # Orange HUD
                        count += 1
                cv2.putText(img, f"YOLO INFERENCE | OBJS: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (249, 115, 22), 2)
                return av.VideoFrame.from_ndarray(img, format="bgr24")
            except Exception:
                return frame

        _start_webrtc_stream(
            "vehicle_stream",
            vehicle_callback,
            "Live WebRTC Camera (YOLOv8)",
            "vehicle_stream",
            hint="The detector uses lower-resolution live inference so it starts faster and drops fewer frames on CPU.",
        )


# ═════════════════════════════════════════════════════════════════════════════
# MODULE 4 — TRAFFIC SIGNS
# ═════════════════════════════════════════════════════════════════════════════
def _sign_module():
    section_header("Traffic Sign Detection", "CNN Classifier · 43 Classes")
    
    src = st.radio("Input Source", LIVE_INPUT_SOURCES, horizontal=True, key="cv_sd_src")
    
    def _sd_cb(img):
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            m1 = cv2.inRange(hsv, np.array([0,100,100]), np.array([10,255,255]))
            m2 = cv2.inRange(hsv, np.array([160,100,100]), np.array([179,255,255]))
            red_mask = cv2.bitwise_or(m1, m2)
            cnts, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            count = 0
            for c in cnts:
                if cv2.contourArea(c) > 1000:
                    x, y, w, h = cv2.boundingRect(c)
                    draw_cyber_hud(img, x, y, w, h, "RED SIGN", (237, 29, 36))
                    count += 1
            cv2.putText(img, f"SIGN FILTER (RED) | MATCHES: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (237, 29, 36), 2)
        except Exception:
            pass
        return img

    if src in ("📷 Photo", "📸 Camera Snapshot"):
        img = _load_image_from_source(
            src,
            "Upload Sign",
            "sd_photo",
            "Capture Sign",
            "sd_camera",
        )
        if img is not None:
            processed = _sd_cb(img.copy())
            st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_column_width=True)
    elif src == "📹 Video File":
        v = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="sd_video")
        if v: process_video_realtime(v, _sd_cb)
    else:
        def sign_callback(frame: av.VideoFrame) -> av.VideoFrame:
            try:
                # Frame skipping
                if 'sd_frame_count' not in st.session_state: st.session_state.sd_frame_count = 0
                st.session_state.sd_frame_count += 1
                if st.session_state.sd_frame_count % 2 != 0: return frame

                img = frame.to_ndarray(format="bgr24")
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                m1 = cv2.inRange(hsv, np.array([0,100,100]), np.array([10,255,255]))
                m2 = cv2.inRange(hsv, np.array( [160,100,100]), np.array([179,255,255]))
                red_mask = cv2.bitwise_or(m1, m2)
                cnts, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                count = 0
                for c in cnts:
                    if cv2.contourArea(c) > 1000:
                        x, y, w, h = cv2.boundingRect(c)
                        draw_cyber_hud(img, x, y, w, h, "DETECTED: SIGNS", (250, 204, 21))
                        count += 1
                cv2.putText(img, f"OPS: SIGN FILTER | TARGETS: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (250, 204, 21), 2)
                return av.VideoFrame.from_ndarray(img, format="bgr24")
            except Exception:
                return frame

        _start_webrtc_stream(
            "sign_stream",
            sign_callback,
            "Live WebRTC Camera",
            "sign_stream",
            hint="Local mode starts without STUN to reduce camera handshake failures.",
        )


# ═════════════════════════════════════════════════════════════════════════════
# PALM READING FEATURE EXTRACTION UTILS
# ═════════════════════════════════════════════════════════════════════════════
def extract_skeleton(mask):
    mask_binary = (mask > 0).astype(np.uint8)
    return cv2.ximgproc.thinning(mask_binary * 255) if hasattr(cv2, 'ximgproc') else mask_binary

def get_line_length(mask):
    if mask.max() == 0: return 0
    binary_mask = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours: return 0
    longest_contour = max(contours, key=cv2.contourArea)
    return cv2.arcLength(longest_contour, closed=False)

def get_curvature(mask):
    if mask.max() == 0: return 0
    binary_mask = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours: return 0
    longest_contour = max(contours, key=cv2.contourArea)
    arc_length = cv2.arcLength(longest_contour, closed=False)
    contour_points = longest_contour.reshape(-1, 2)
    if len(contour_points) < 2: return 0
    straight_distance = np.linalg.norm(contour_points[0] - contour_points[-1])
    if straight_distance < 1: return 1.0
    return arc_length / straight_distance

def get_line_angle(mask):
    if mask.max() == 0: return 0
    binary_mask = (mask > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours: return 0
    longest_contour = max(contours, key=cv2.contourArea)
    [vx, vy, x, y] = cv2.fitLine(longest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
    angle = np.arctan2(vy, vx) * 180 / np.pi
    return float(angle[0]) if isinstance(angle, np.ndarray) else float(angle)

def count_intersections(mask1, mask2):
    intersection = cv2.bitwise_and(mask1, mask2)
    if intersection.max() == 0: return 0
    num_labels, _ = cv2.connectedComponents(intersection)
    return max(0, num_labels - 1)

def extract_palm_features(segmentation_mask):
    life_mask = (segmentation_mask == 1).astype(np.uint8) * 255
    head_mask = (segmentation_mask == 2).astype(np.uint8) * 255
    heart_mask = (segmentation_mask == 3).astype(np.uint8) * 255
    features = {}
    features['life_length'] = get_line_length(life_mask)
    features['head_length'] = get_line_length(head_mask)
    features['heart_length'] = get_line_length(heart_mask)
    features['life_curvature'] = get_curvature(life_mask)
    features['head_curvature'] = get_curvature(head_mask)
    features['heart_curvature'] = get_curvature(heart_mask)
    features['life_angle'] = get_line_angle(life_mask)
    features['head_angle'] = get_line_angle(head_mask)
    features['heart_angle'] = get_line_angle(heart_mask)
    features['life_head_intersection'] = count_intersections(life_mask, head_mask)
    features['life_heart_intersection'] = count_intersections(life_mask, heart_mask)
    features['head_heart_intersection'] = count_intersections(head_mask, heart_mask)
    return features

def classify_palm(features):
    classification = {}
    lengths = {'Life': features.get('life_length', 0), 'Head': features.get('head_length', 0), 'Heart': features.get('heart_length', 0)}
    total_length = sum(lengths.values())
    if total_length == 0:
        classification['dominant_line'] = 'Unknown'
        classification['confidence'] = 0.0
    else:
        dominant_line = max(lengths, key=lengths.get)
        classification['dominant_line'] = dominant_line
        classification['confidence'] = round(lengths[dominant_line] / total_length, 3)
    
    avg_curvature = (features.get('life_curvature', 0) + features.get('head_curvature', 0) + features.get('heart_curvature', 0)) / 3
    if avg_curvature > 1.3: classification['palm_type'] = 'Curved/Expressive'
    elif avg_curvature > 1.1: classification['palm_type'] = 'Balanced'
    else: classification['palm_type'] = 'Straight/Practical'
    
    head_angle = abs(features.get('head_angle', 0))
    intersections = features.get('life_head_intersection', 0)
    if head_angle > 10 and intersections > 0:
        classification['career_shift_indicator'] = 'Yes'
        classification['career_shift_confidence'] = 0.7
    else:
        classification['career_shift_indicator'] = 'No'
        classification['career_shift_confidence'] = 0.6
    return classification

def create_palm_overlay(image, mask):
    if mask.shape[:2] != image.shape[:2]:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    overlay = image.copy()
    # Colors in BGR (Life: Red, Head: Green, Heart: Blue)
    colors = {1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 0)}
    for class_id, color in colors.items():
        class_mask = (mask == class_id)
        overlay[class_mask] = overlay[class_mask] * 0.5 + np.array(color) * 0.5
    return overlay.astype(np.uint8)


# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT PALM OBSERVATIONS (replaces the removed expander form)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_OBSERVATIONS = {
    "dominant_hand": "Right",
    "hand_shape": "Auto / unsure",
    "line_depth": "Medium",
    "major_breaks": "A few",
    "fate_line": "Faint",
    "sun_line": "Faint",
}


def _draw_live_palm_summary(image, report):
    output = image.copy()
    labels = [
        f"Dominant: {report['dominant_line']}",
        f"Quality: {report['detection_quality']:.2f}",
        f"Career Shift: {report['career_shift_indicator']}",
    ]
    if report["detection_quality"] < 0.55:
        labels.append("Tip: move closer, flatten palm, use brighter light")

    panel_height = 34 + len(labels) * 22
    cv2.rectangle(output, (10, 10), (470, panel_height), (5, 10, 24), thickness=-1)
    for idx, text in enumerate(labels):
        cv2.putText(
            output,
            text,
            (20, 36 + idx * 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (236, 245, 255),
            2,
            cv2.LINE_AA,
        )
    return output


def _render_palm_report(overlay, features, report):
    from utils.voice import render_voice_button
    import uuid

    # ── Image + key metrics ──────────────────────────────────────────────────
    c1, c2 = st.columns([1.05, 0.95])
    with c1:
        st.image(
            cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB),
            use_column_width=True,
            caption="Line segmentation overlay (Life: red, Head: green, Heart: blue)",
        )
    with c2:
        dq = report.get("detection_quality", 1.0)
        if dq < 0.55:
            render_content_card(
                "⚠️ Scan Quality Low",
                "The palm lines are not fully visible. For a clearer reading: use brighter lighting, "
                "flatten your palm against the camera, and crop tightly so the hand fills the frame.",
                accent_color="#F59E0B",
                icon="⚠️",
            )
        render_info_grid([
            ("Dominant Line", report["dominant_line"]),
            ("Detection Quality", f"{dq:.0%}"),
            ("Career Shift", report["career_shift_indicator"]),
            ("Hand Shape", report["hand_shape_label"]),
        ])
        render_content_card(
            "Reading Summary",
            report["summary"],
            accent_color="#8B5CF6",
            icon="🔮",
        )
        render_voice_button(report["summary"], key_suffix=f"palm_summary_{uuid.uuid4().hex[:8]}")

    st.divider()

    # ── Tabs ─────────────────────────────────────────────────────────────────
    line_strength_df = pd.DataFrame(
        {
            "line": list(report["line_strengths"].keys()),
            "strength": [round(v * 100, 1) for v in report["line_strengths"].values()],
        }
    ).set_index("line")

    overview_tab, feature_tab, detail_tab = st.tabs(["✨ Reading", "📊 Feature Dashboard", "🔬 Extracted Features"])

    with overview_tab:
        st.markdown("#### Major Line Reading")
        line_icons = {"Life": "❤️", "Head": "🧠", "Heart": "💙"}
        line_colors = {"Life": "#10B981", "Head": "#06B6D4", "Heart": "#EC4899"}
        for item in report["line_readings"]:
            render_content_card(
                f"{item['line']} Line",
                f"{item['detail']}<br><span style='color:#94A3B8; font-size:12px;'>Focus: {item['emphasis']}</span>",
                accent_color=line_colors.get(item["line"], "#3B82F6"),
                icon=line_icons.get(item["line"], "〰️"),
            )

        st.markdown("#### Interpretation Themes")
        theme_cards = [
            ("🧠", "Mindset", "mindset", "#06B6D4"),
            ("❤️", "Relationships", "relationships", "#EC4899"),
            ("⚡", "Energy", "energy", "#F59E0B"),
            ("💼", "Career", "career", "#10B981"),
            ("✨", "Visibility", "visibility", "#8B5CF6"),
        ]
        for icon, title, key, color in theme_cards:
            render_content_card(title, report["themes"][key], accent_color=color, icon=icon)

        # Pattern Notes
        notes_html = "".join([f"<div style='margin-bottom:6px;'>• {note}</div>" for note in report["shared_notes"]])
        render_content_card("Pattern Notes", notes_html, accent_color="#8B5CF6", icon="📝")

        # Guidance
        guidance_html = "".join([f"<div style='margin-bottom:6px;'>🧭 {item}</div>" for item in report["guidance"]])
        render_content_card("Guidance", guidance_html, accent_color="#06B6D4", icon="🧭")

    with feature_tab:
        st.caption("Detected line balance")
        st.bar_chart(line_strength_df, height=260)
        st.caption("Palm-reading prompts")
        for question in report["questions"]:
            st.markdown(f"- {question}")

    with detail_tab:
        st.json(
            {
                "report": {
                    "dominant_line": report["dominant_line"],
                    "dominant_strength_pct": report["dominant_strength_pct"],
                    "detection_quality": report["detection_quality"],
                    "observations": report["observations"],
                },
                "features": {k: round(v, 2) if isinstance(v, float) else v for k, v in features.items()},
            }
        )

# ═════════════════════════════════════════════════════════════════════════════
# MODULE 5 — PALM READING (CNN Segmentation)
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_palm_model(device):
    """Shared global cache for the Palm Segmentation model."""
    try:
        import segmentation_models_pytorch as smp
        import torch
        model = smp.Unet(encoder_name="resnet18", encoder_weights=None, in_channels=3, classes=4)
        model.load_state_dict(torch.load("palm_model.pth", map_location=device))
        model.to(device)
        model.eval()
        return model
    except Exception as exc:
        st.error(f"Failed to load Palm Model from 'palm_model.pth': {exc}")
        return None

def _palm_module():
    section_header(
        "Palm Reading Extraction",
        "Book-guided line analysis with camera snapshot fallback and live low-latency prediction",
    )
    st.info(
        "Use `Camera Snapshot` if live WebRTC gives STUN trouble. The palm tutor will use the latest saved scan for personalized questions."
    )
    src = st.radio("Input Source", LIVE_INPUT_SOURCES, horizontal=True, key="cv_palm_src")
    observations = DEFAULT_OBSERVATIONS

    try:
        import torch
        import albumentations as A
        from albumentations.pytorch import ToTensorV2
    except ImportError:
        st.error("Missing dependencies. Please run `pip install -r requirements.txt` (needs torch, albumentations).")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_palm_model(device)
    if model is None: return
    preprocessing = A.Compose(
        [
            A.Resize(256, 256),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ]
    )

    def _palm_cb(img):
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            preprocessed = preprocessing(image=img_rgb)
            image_tensor = preprocessed["image"].unsqueeze(0).to(device)

            with torch.no_grad():
                output = model(image_tensor)
                pred_mask = output.argmax(dim=1).squeeze(0).cpu().numpy()

            mask = cv2.resize(pred_mask.astype(np.uint8), (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
            overlay_img = create_palm_overlay(img, mask)
            features = extract_palm_features(mask)
            report = build_palm_report(features, observations)
            return overlay_img, mask, features, report
        except Exception as e:
            # Fallback to empty if inference fails
            return img, np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8), {}, build_palm_report({}, observations)

    def _live_frame_overlay(img):
        small_img = cv2.resize(img, (384, 288))
        overlay, _, _, report = _palm_cb(small_img)
        overlay = _draw_live_palm_summary(overlay, report)
        return cv2.resize(overlay, (img.shape[1], img.shape[0]))

    if src in ("📷 Photo", "📸 Camera Snapshot"):
        img = _load_image_from_source(
            src,
            "Upload Palm Photo",
            "palm_photo",
            "Capture Palm Photo",
            "palm_camera",
        )
        if img is not None:
            with st.spinner("Analyzing Palm..."):
                overlay, mask, features, report = _palm_cb(img.copy())

            st.session_state["palm_latest_report"] = report
            st.session_state["palm_latest_features"] = features
            st.session_state["palm_latest_summary"] = report["summary"]
            _render_palm_report(overlay, features, report)

    elif src == "📹 Video File":
        v = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="palm_video")
        if v:
            st.caption("Video mode runs the palm overlay and live summary on downscaled frames for smoother playback.")
            process_video_realtime(v, _live_frame_overlay)
    else:
        def palm_callback(frame: av.VideoFrame) -> av.VideoFrame:
            try:
                if "palm_frame_count" not in st.session_state:
                    st.session_state.palm_frame_count = 0
                st.session_state.palm_frame_count += 1
                if st.session_state.palm_frame_count % 2 != 0:
                    return frame

                img = frame.to_ndarray(format="bgr24")
                final_overlay = _live_frame_overlay(img)
                return av.VideoFrame.from_ndarray(final_overlay, format="bgr24")
            except Exception:
                return frame

        _start_webrtc_stream(
            "palm_stream",
            palm_callback,
            "Live WebRTC Camera (Palm Reading)",
            "palm_stream",
            hint="Live mode now defaults to no-STUN local streaming and reduced-resolution inference for faster palm predictions.",
        )

    latest_report = st.session_state.get("palm_latest_report")
    if latest_report:
        st.caption("Latest saved scan summary")
        st.write(latest_report["summary"])


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _cv_module_renderer(module_key):
    renderers = {
        "attendance": _attendance_module,
        "face_scan": _face_scan_module,
        "vehicle": _vehicle_module,
        "sign": _sign_module,
        "palm": _palm_module,
    }
    return renderers[module_key]


def _set_cv_nav(route_key):
    st.session_state["nav_selection"] = route_key
    st.rerun()


def _render_cv_shell(title, subtitle, icon):
    from utils.styles import inject_global_css

    inject_global_css()
    gradient_header(title, subtitle, icon)

    if not WEBRTC_READY:
        st.error("`streamlit-webrtc` is missing. Features requiring live camera will not function.")


def _render_cv_jump_bar(active_key=None):
    options = [("OpenCV Gallery", CV_NAV_GALLERY)] + [
        (f"{item['icon']} {item['title']}", CV_NAV_BY_MODULE_KEY[item["key"]]) for item in CV_MODULES
    ]
    labels = [label for label, _ in options]
    route_map = {label: route_key for label, route_key in options}

    current_route = CV_NAV_GALLERY
    if active_key in CV_NAV_BY_MODULE_KEY:
        current_route = CV_NAV_BY_MODULE_KEY[active_key]

    current_label = next((label for label, route_key in options if route_key == current_route), "OpenCV Gallery")

    st.markdown("<hr style='border: 0; height: 1px; background: rgba(34, 211, 238, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.2])
    with c1:
        if active_key is None:
            st.button("📸 Optical Gallery", use_container_width=True, disabled=True, key="cv_gallery_home_disabled")
        else:
            if st.button("⬅ Back to Gallery", use_container_width=True, key=f"cv_back_{active_key}"):
                _set_cv_nav(CV_NAV_GALLERY)
    with c2:
        selected = st.selectbox(
            "Jump to Vision Analytics",
            labels,
            index=labels.index(current_label),
            key=f"cv_jump_{active_key or 'gallery'}",
        )
        selected_route = route_map[selected]
        if selected_route != current_route:
            _set_cv_nav(selected_route)
    st.markdown("<hr style='border: 0; height: 1px; background: rgba(34, 211, 238, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)



def _render_cv_gallery():
    _render_cv_shell("Optical Analytics Hub", "Face Identity · Live Motion · Structural Analysis", "👁️")
    _render_cv_jump_bar()

    st.info("Each OpenCV tool below now opens on its own dedicated page, so you can focus on one vision workflow at a time.")
    st.markdown('<h3 style="font-family: \'Montserrat\', sans-serif; color: white; font-weight: 700; margin-bottom: 25px; border-bottom: 2px solid #06B6D4; display: inline-block; padding-bottom: 10px;">Modules Gallery</h3>', unsafe_allow_html=True)

    st.caption("Each card now uses its own module preview and can run independently like a separate OpenCV mini-project.")

    for idx, item in enumerate(CV_MODULES):
        card_color = "#06B6D4" if idx % 2 == 0 else "#3B82F6"
        with st.container():
            e_col1, e_col2, e_col3 = st.columns([1.2, 3, 1])

            with e_col1:
                module_preview = _gallery_preview_for_module(item["key"], item["title"], item.get("banner"))
                st.image(module_preview, use_column_width=True)

            with e_col2:
                st.markdown(
                    f"""
                    <div style="padding: 5px 0;">
                        <div style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 20px; color: white; margin-bottom: 5px;">{item['title']} {item['icon']}</div>
                        <p style="color: #F8FAFC; font-size: 14px; line-height: 1.5; margin-bottom: 12px; font-weight: 500;">{item['gallery_subtitle']}. Optimized for real-time vision processing.</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            {"".join([f'<span style="background: rgba(255,255,255,0.05); padding: 3px 10px; border-radius: 4px; color: {card_color}; font-size: 11px; font-weight: 600; border: 1px solid rgba(255,255,255,0.1);">{feature}</span>' for feature in item['features']])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with e_col3:
                st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                if st.button(f"Open {item['title']}", key=f"launch_cv_page_{item['key']}", type="primary", use_container_width=True):
                    _set_cv_nav(CV_NAV_BY_MODULE_KEY[item["key"]])

            st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>", unsafe_allow_html=True)



def _render_cv_module_page(module_key):
    module = CV_MODULE_MAP.get(module_key)
    if module is None:
        st.warning("Unknown OpenCV module route. Redirecting to gallery.")
        _set_cv_nav(CV_NAV_GALLERY)
        return

    inject_module_theme("opencv")
    _render_cv_shell(module["page_title"], module["page_subtitle"], module["icon"])
    _render_cv_jump_bar(module_key)
    render_content_card(
        module["page_title"],
        module["page_subtitle"],
        accent_color="#F59E0B",
        icon=module["icon"],
    )
    _cv_module_renderer(module_key)()
    st.divider()



def opencv_detection_page():
    st.session_state.pop("cv_active_module", None)
    _render_cv_gallery()


def opencv_attendance_page():
    _render_cv_module_page("attendance")


def opencv_face_scan_page():
    _render_cv_module_page("face_scan")


def opencv_vehicle_page():
    _render_cv_module_page("vehicle")


def opencv_sign_page():
    _render_cv_module_page("sign")


def opencv_palm_page():
    _render_cv_module_page("palm")


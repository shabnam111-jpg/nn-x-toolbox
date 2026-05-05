#!/usr/bin/env python3
"""
Dependency Checker for Palm Reading Module
Verifies all required packages and identifies missing dependencies
"""

import sys
from pathlib import Path

def check_dependency(module_name, pip_name=None, required=True):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        status = "✅ INSTALLED"
        return True
    except ImportError:
        pip_name = pip_name or module_name
        status = f"❌ MISSING - Install with: pip install {pip_name}"
        if required:
            print(f"  {status}")
            return False
        else:
            print(f"  ⚠️ OPTIONAL - {status}")
            return True

def main():
    print("=" * 70)
    print("🔍 PALM READING MODULE - DEPENDENCY CHECK")
    print("=" * 70)
    
    print("\n📦 CORE DEPENDENCIES (Required)")
    print("-" * 70)
    
    core_deps = {
        'streamlit': 'streamlit',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pandas': 'pandas',
    }
    
    core_ok = all(check_dependency(k, v, True) for k, v in core_deps.items())
    
    print("\n🔧 PYTORCH & ML DEPENDENCIES (Required for Palm Reading)")
    print("-" * 70)
    
    ml_deps = {
        'torch': 'torch',
        'albumentations': 'albumentations',
        'segmentation_models_pytorch': 'segmentation-models-pytorch',
    }
    
    ml_ok = all(check_dependency(k, v, True) for k, v in ml_deps.items())
    
    print("\n🎥 WEBRTC DEPENDENCIES (Optional - for live streaming)")
    print("-" * 70)
    
    webrtc_deps = {
        'streamlit_webrtc': 'streamlit-webrtc',
        'av': 'av',
    }
    
    for k, v in webrtc_deps.items():
        check_dependency(k, v, False)
    
    print("\n📊 OPTIONAL ENHANCEMENTS")
    print("-" * 70)
    
    optional_deps = {
        'reportlab': 'reportlab',  # PDF generation
        'pydub': 'pydub',  # Audio processing
        'plotly': 'plotly',  # Advanced charts
        'sklearn': 'scikit-learn',  # ML utilities
    }
    
    for k, v in optional_deps.items():
        check_dependency(k, v, False)
    
    print("\n" + "=" * 70)
    if core_ok and ml_ok:
        print("✅ ALL CORE DEPENDENCIES MET - Palm Reading is ready!")
    else:
        print("⚠️  MISSING CORE DEPENDENCIES - Install required packages:")
        print("\n   pip install torch albumentations segmentation-models-pytorch")
        print("   pip install streamlit-webrtc av")
    
    print("=" * 70)
    
    # Check for model file
    print("\n🎯 MODEL FILE CHECK")
    print("-" * 70)
    
    model_path = Path("palm_model.pth")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  ✅ palm_model.pth found ({size_mb:.1f} MB)")
    else:
        print(f"  ❌ palm_model.pth NOT FOUND")
        print(f"     Expected at: {model_path.absolute()}")
        print(f"     This file is required for palm analysis to work")

if __name__ == "__main__":
    main()

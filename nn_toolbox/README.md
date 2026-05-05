# Neural Network Toolbox

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b)
![License](https://img.shields.io/badge/License-MIT-green)
[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-0aa5a8)](https://nn-tool-box.streamlit.app/)

An interactive **Streamlit-based learning toolbox** for understanding core **Neural Network concepts** and **Computer Vision techniques** through hands-on experimentation and visualizations.

**Live App**: https://nn-tool-box.streamlit.app/
> Since it's freely deployed, the app may need a few seconds to wake up.

---

## Highlights

- Interactive, educational UI built with Streamlit
- Perceptron training with logic gates or custom CSV
- Forward and backward propagation walkthroughs
- Multi-Layer Perceptron (MLP) with binary & multiclass support
- **Advanced Visualization Toolbox** with interactive training dynamics:
  - Animated decision boundary visualization
  - Real-time training metrics dashboard
  - Confusion matrix with error analysis
  - Gradient descent animation with weight path
  - Learning rate comparison & activation functions
  - Model & report export (HTML with embedded charts)
- **ML Experimentation Hub - Phase 1** (Advanced Analysis Platform):
  - 🎬 **Training Replay**: Epoch-by-epoch decision boundary evolution with playback controls
  - 📊 **Gradient Flow Analysis**: Detect vanishing/exploding gradients, per-layer gradient tracking
  - 🗻 **3D Loss Landscape**: Interactive 3D visualization of loss surface around trained weights
  - 🔍 **Model Debugger**: Step-by-step forward/backward pass inspection with neuron values & gradients
  - 📈 **Learning Rate Analysis**: Train multiple learning rates in parallel, compare convergence
- OpenCV-based object detection:
  - Face
  - Eye + Smile
  - Stop Sign
  - Face Count
- Real-time webcam detection & image upload
- Built-in sample dataset (IRIS)

---

## Getting Started

### 1️⃣The repository
git clone https://github.com/akashsinghsagar/nn_toolbox.git
cd nn_toolbox
```

### 2️⃣ Create & activate a virtual environment

```powershell
python -m venv .venv
```
```powershell
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## Project Structure

```
.
├── app.py                    # Main Streamlit entry point
├── requirements.txt
│
├── data/
│   └── IRIS.csv              # Sample dataset
│
└── src/
    ├── __init__.py
    │
    ├── assets/
    │   ├── image/
    │   │   └── nn_image.jpg  # Home page banner
    │   └── documents/        # In-app documentation pages
    │       ├── perceptron.py
    │       ├── forward_propagation.py
    │       ├── back_propagation.py
    │       └── mnp.py
    │
    ├── ui/                   # Interactive module pages
    │   ├── perceptron_ui.py
    │   ├── forward_propagation.py
    │   ├── backward_propagation.py
    │   ├── mlp.py
    │   ├── advanced_visualization.py  # Advanced neural network visualization
    │   ├── ml_experimentation_hub.py  # ML Experimentation Platform - Phase 1
    │   │
    │   ├── modules/           # Feature modules for ML Experimentation Hub
    │   │   ├── training_replay.py      # Epoch-by-epoch training visualization
    │   │   ├── gradient_analyzer.py    # Gradient flow and health monitoring
    │   │   ├── loss_landscape.py       # 3D loss surface visualization
    │   │   ├── model_debugger.py       # Forward/backward pass inspection
    │   │   └── learning_rate_optimizer.py  # Learning rate comparison & analysis
    │   │
    │   └── utils/             # Utility modules
    │       ├── model_checkpoint.py     # Checkpoint management & tracking
    │       └── gradient_tracker.py     # Gradient flow monitoring
    │
    └── open_cv/              # OpenCV detection module
        ├── open_cv_detection.py
        ├── cascades/         # Haar cascade XML files
        └── sample/           # Sample images for demo
```

---

## Architecture Overview

```mermaid
flowchart TB
    A[app.py] --> B[Streamlit UI Pages]
    B --> C[Perceptron UI]
    B --> D[Forward Prop UI]
    B --> E[Backward Prop UI]
    B --> F[MLP UI]
    B --> G[OpenCV Detection UI]
    A --> H[Docs Pages]
    H --> I[Perceptron Docs]
    H --> J[Forward Prop Docs]
    H --> K[Backward Prop Docs]
    H --> L[MLP Docs]
    C --> M[data/ OR uploaded CSV]
    F --> M
    G --> N[Webcam OR Image Upload]
```

---

## Module Flow

```mermaid
flowchart LR
    X[Input Data] --> Y[Preprocess / Validate]
    Y --> Z[Forward Pass]
    Z --> AA[Loss]
    AA --> AB[Backward Pass]
    AB --> AC[Parameter Update]
    AC --> AD[Metrics / Visualization]
```

---

## Usage Guide

- Use the **sidebar** to navigate between modules or documentation pages
- **Perceptron / MLP**
  - Select logic gates or upload a CSV file
  - Tune learning parameters and train
- **OpenCV Detection**
  - Choose a detection type (Face, Eye+Smile, Stop Sign, Face Count)
  - Use webcam, upload a video, or upload an image
- Visualize training behavior and results interactively

---

## Data Input Rules

- **Perceptron** — exactly 2 binary feature columns + binary target
- **MLP** — numeric & categorical features; binary or multiclass target
- **OpenCV** — webcam, image files (JPG/JPEG/PNG), or video files
- Large datasets are restricted to maintain UI performance

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `numpy` | Numerical computation |
| `pandas` | Data handling |
| `plotly` | Interactive charts |
| `opencv-python` | Computer vision |
| `streamlit-webrtc` | Real-time webcam on cloud |
| `av` | Video processing |

---

## Notes

- This project prioritizes **learning & explainability** over raw performance
- MLP module includes standardization and one-hot encoding
- Designed for **students, demos, and concept clarity**

---

## License

MIT License — free to use, modify, and share for learning and beyond.

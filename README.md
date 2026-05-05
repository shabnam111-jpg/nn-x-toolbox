

# Neural Network Toolbox

A full-stack machine learning ecosystem that integrates face recognition attendance systems, neural network visualization tools, and a modern web interface for interactive AI exploration.

---

## Live Demo

Access the deployed application:

**Web Interface:**
[https://akashsinghsagar.github.io/Neural-Network-Toolbox/](https://akashsinghsagar.github.io/Neural-Network-Toolbox/)

---

## Overview

Neural Network Toolbox is designed as a modular AI platform consisting of three integrated systems:

* A computer vision-based attendance solution
* A neural network experimentation and visualization tool
* A modern frontend interface for seamless interaction

This project demonstrates real-world system design by combining machine learning, computer vision, and full-stack development.

---

## Architecture

The platform is divided into three main components:

### 1. Attendance Vision

A real-time face recognition system for attendance tracking and analytics.

**Features**

* Face detection and recognition using live camera feed
* Image and video upload processing
* Attendance recording and history tracking
* Department-wise filtering and analytics
* Interactive dashboards with visual insights

**Tech Stack**
Python, Streamlit, OpenCV, face_recognition, Pandas, Plotly

---

### 2. NN Toolbox

An interactive machine learning lab for understanding neural networks.

**Features**

* Perceptron learning visualization
* Multi-layer perceptron (MLP) implementation
* Forward and backward propagation simulation
* Gradient descent visualization
* Loss landscape exploration
* Step-by-step training replay

**Tech Stack**
Python, Streamlit, NumPy, Pandas, Plotly

---

### 3. Web Interface

A modern React-based frontend acting as the central hub.

**Features**

* Animated landing page with neuron-to-network transition
* Glassmorphic dark UI design
* Responsive layout
* Navigation across all modules
* Smooth transitions and motion effects

**Tech Stack**
React 18, Vite, Tailwind CSS, Framer Motion, Lottie

---

## Key Features

* Modular multi-application architecture
* Real-time computer vision processing
* Interactive machine learning visualizations
* Clean and modern UI/UX design
* Fully local execution (no cloud dependency required)
* Extensible and scalable structure

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* Node.js 16 or higher
* npm or yarn
* Git

---

### Installation

#### Clone the repository

```bash
git clone https://github.com/akashsinghsagar/Neural-Network-Toolbox.git
cd Neural-Network-Toolbox
```

---

### Backend Setup

```bash
cd "Attendance vision/attendance_app"
pip install -r requirements.txt
```

```bash
cd nn_toolbox
pip install -r requirements.txt
```

---

### Frontend Setup

```bash
cd nn_toolbox_web
npm install
```

---

## Running the Application

Run each module in a separate terminal:

### Attendance Vision

```bash
cd "Attendance vision/attendance_app"
streamlit run app.py --server.port 8504
```

### NN Toolbox

```bash
cd nn_toolbox
streamlit run app.py --server.port 8505
```

### Web Interface

```bash
cd nn_toolbox_web
npm run dev
```

---

## Access Points

| Application       | URL                                            |
| ----------------- | ---------------------------------------------- |
| Web Interface     | [http://localhost:5174](http://localhost:5174) |
| Attendance Vision | [http://localhost:8504](http://localhost:8504) |
| NN Toolbox        | [http://localhost:8505](http://localhost:8505) |

---

## Project Structure

```
Neural-Network-Toolbox/
├── Attendance vision/
│   └── attendance_app/
├── nn_toolbox/
├── nn_toolbox_web/
└── README.md
```

---

## Configuration

Environment variables can be configured for customization:

### Attendance System

```
DEBUG=False
DATABASE_PATH=attendance.db
CAMERA_INDEX=0
```

### NN Toolbox

```
EPOCHS=100
LEARNING_RATE=0.01
BATCH_SIZE=32
```

### Web Interface

```
VITE_API_PORT=8504
VITE_NN_PORT=8505
```

---

## Deployment

### Frontend

* GitHub Pages (current deployment)
* Vercel or Netlify (recommended for production)

### Backend

* Railway
* Render
* Heroku

---

## API Endpoints

### Attendance Vision

* `POST /register-user`
* `POST /mark-attendance`
* `GET /records`
* `GET /analytics`
* `POST /upload-image`
* `POST /upload-video`

### NN Toolbox

* `GET /models`
* `POST /train-model`
* `GET /visualization`
* `POST /evaluate`

---

## Use Cases

* Students learning neural networks visually
* Developers experimenting with ML models
* Institutions automating attendance systems
* Demonstrating full-stack AI system design

---

## Future Improvements

* User authentication system
* Cloud deployment with API integration
* Real-time streaming interface
* AI-based performance insights
* Mobile application support

---

## Author

**Akash Singh Sagar**
GitHub: [https://github.com/akashsinghsagar](https://github.com/akashsinghsagar)

---

## License

This project is licensed under the MIT License.

---

## Summary

Neural Network Toolbox is a complete AI-driven platform that bridges the gap between theoretical learning and practical implementation. It combines computer vision, machine learning, and modern frontend design into a unified system suitable for both education and real-world applications.


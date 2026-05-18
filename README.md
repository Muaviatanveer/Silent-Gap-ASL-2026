# 🌉 Sara's Bridge: Advanced ASL Sign Language Classification

**AI Hackathon 2026 — Forman Computer Science Club**  
🏆 *Ranked Top 5 (4th Place) on the Kaggle Leaderboard*

---

## 🌟 The Vision

70 million deaf people worldwide use sign language, yet less than 5% of the hearing population understands it. For "Sara," everyday interactions at work or the hospital are a frustrating struggle. Automated tools often fail because they are built on "clean" lab data and break when exposed to real-world backgrounds and lighting.

**Sara's Bridge** is a robust, real-time AI solution designed to close this gap with extreme technical resilience and real-time word-spelling capabilities.

---

## 🚀 Technical Highlights & Approach

Rather than simply training on the provided competition data, our team prioritized **Generalization** and **Real-World Stability**.

- **Architecture (ResNet50):** Utilized a Residual Neural Network via transfer learning. Chosen for its optimal balance of high feature-extraction (accuracy) and low latency (speed) required for real-time mobile deployment.
- **The "Nuclear" Data Strategy:** We recognized that standard models fail on "Background Variations" (the hidden test set). To combat this, we merged the competition data with massive external datasets, successfully training on **over 300,000 images**.
- **Indestructible Pipeline:** We built an automated OS-level pathfinder and label-normalization system (`get_label`) to ensure our code survives blind Kaggle reruns without crashing.
- **Inference Stability:** Utilized **TTA** (Test Time Augmentation) to double-check predictions across varied lighting and rotation.

---

## 🛠️ Phase 2: Creative Extension (Live Word Speller)

To move beyond a simple image classifier, we built a **Two-Way Bridge Interface**. Instead of just outputting single letters, we developed a **Buffer-Based Spelling Algorithm**:

1. **30 FPS Processing:** The model reads the live webcam feed in real-time.
2. **Commit Logic:** It requires the user to hold a sign for a consecutive number of frames before "committing" the letter.
3. **Noise Filtering:** This acts as an organic filter, preventing "flicker" and allowing Sara to seamlessly type entire words and sentences (utilizing the `space` and `del` classes).

---

## 📊 Results & Performance

- **Kaggle Leaderboard Rank:** 4th Place (Score: 0.5247)
- **Validation Accuracy (Clean Data):** 100%
- **Validation Accuracy (Extreme Augmentation):** 99.9%
- **Latency:** Optimized for real-time webcam inference.

---

## 💻 How to Run the Live Demo (Deployment)

### 1. Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/saras-bridge.git
cd saras-bridge
```

### 2. Download the Model:
Download `resnet50_final.pkl` from the link below and place it in the root directory:

https://drive.google.com/file/d/17kvs7X_tb2tJCOA33VhvhE0AkqaZTw6o/view?usp=sharing

> **Note:** Make sure the downloaded file name remains `resnet50_final.pkl`.

### 3. Install Dependencies:
```bash
pip install fastai gradio opencv-python
```

### 4. Run the Interface:
```bash
python app.py
```

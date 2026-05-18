🌉 Sara's Bridge: Advanced ASL Sign Language Classification
AI Hackathon 2026 — Forman Computer Science Club
Ranked Top 5 on the Kaggle Leaderboard
🌟 The Vision
70 million deaf people worldwide use sign language, yet less than 5% of the hearing population understands it. For "Sara," everyday interactions at work or the hospital are a frustrating struggle. Automated tools often fail because they are built on "clean" lab data and break when exposed to real-world backgrounds and lighting.
Sara's Bridge is a robust, real-time AI solution designed to close this gap with extreme technical resilience and real-time word-spelling capabilities.
🚀 Technical Highlights & Approach
Rather than simply training on the provided competition data, our team prioritized Generalization and Real-World Stability.
Architecture: ResNet50 Residual Neural Network (Transfer Learning). Chosen for its optimal balance of high feature-extraction (accuracy) and low latency (speed) required for real-time mobile deployment.
The "Nuclear" Data Strategy: We recognized that standard models fail on "Background Variations" (the hidden test set). To combat this, we merged the competition data with massive external datasets, successfully training on over 300,000 images.
Indestructible Pipeline: We built an automated OS-level pathfinder and label-normalization system (get_label) to ensure our code survives blind Kaggle reruns without crashing.
Inference Stability: Utilized TTA (Test Time Augmentation) to double-check predictions across varied lighting and rotation, ensuring high confidence on unseen test data.
🛠️ Phase 2: Creative Extension (Live Word Speller)
To move beyond a simple image classifier, we built a Two-Way Bridge Interface.
Instead of just outputting single letters (e.g., "A", "B"), we developed a Buffer-Based Spelling Algorithm.
The model reads the live webcam feed at 30 FPS.
It requires the user to hold a sign for a consecutive number of frames before "committing" the letter to the text string.
This acts as an organic noise-filter, preventing "flicker" and allowing Sara to seamlessly type entire words and sentences (utilizing the space and del classes).
📊 Results & Performance
Kaggle Leaderboard Rank: 4th Place (Score: 0.5247)
Validation Accuracy (Clean Data): 100%
Validation Accuracy (Extreme Augmentation): 99.9%
Latency: Optimized for real-time webcam inference.
💻 How to Run the Live Demo (Deployment)
Clone this repository to your local machine.
Download our pre-trained model weights (resnet50_final.pkl) and place it in the root directory. (Model file too large for GitHub; available upon request).
Install the required dependencies:
code
Bash
pip install fastai gradio opencv-python
Run the live spelling interface:
code
Bash
python app.py
A local web server will launch. Grant webcam permissions and begin signing!
“Closing the Silent Gap, one frame at a time.”
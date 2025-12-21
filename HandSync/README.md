# HandSync ✋🖱️  
*A Camera‑Driven Virtual Mouse & Gesture Control System*

---

## ⚠️ IMPORTANT – READ THIS FIRST (MediaPipe + Python)
MediaPipe **will fail on newer Python versions** if not set up correctly.

✅ **HandSync is tested and stable ONLY with:**
- **Python 3.11**
- **MediaPipe 0.10.9 (classic `mp.solutions` API)**

❌ Python 3.12+ or MediaPipe ≥ 0.10.30 **will break this project**.

This README **forces a Conda-based setup** to avoid those issues permanently.

---

## 🧙‍♂️ What is HandSync?
**HandSync** turns your webcam into a **virtual mouse and gesture controller**.  
Using real‑time hand‑tracking, you can:

- Move the mouse with **one finger**
- Click using **natural pinch or micro‑jerk motion**
- Scroll using **two fingers**
- Interact with your OS **without touching a mouse**

No gloves. No sensors. Just your hand.

---

## ✨ Key Features (Current)
✔ One‑finger cursor movement (smooth & mapped)  
✔ Natural pinch click (adaptive to hand size)  
✔ Anti‑shake smoothing & click‑lock safety  
✔ Dynamic calibration (works for near/far hands)  
✔ Scroll mode with vertical hand movement  
✔ Visual feedback + active interaction zone  
✔ Fully offline, no internet required  

---

## 🧠 How It Works (Concept)
HandSync uses:
- **MediaPipe Hands** → Detects 21 hand landmarks
- **Dynamic hand scaling** → Click thresholds adapt to hand size
- **Frame smoothing** → Prevents cursor jitter
- **State locking** → Prevents accidental multiple clicks

Instead of fixed distances, **your own hand becomes the ruler**.

---

## 🖐️ Gesture Map (Current)

| Gesture | Action |
|------|------|
| ☝️ Index finger up | Move cursor |
| 🤏 Thumb + Index pinch | Left click |
| ☝️ + sudden jerk | Natural click |
| ☝️ + ✌️ (Index + Middle) | Scroll |
| Hold pinch | Drag‑safe (cursor freeze) |
| Hand out of frame | Idle / Safe mode |

---

## 🧪 Demo Mode
On startup you will see:
- A **white interaction box** → active tracking area
- Live **pinch distance indicator**
- On‑screen feedback for click & scroll modes

---

## 🛠️ Installation (RECOMMENDED – Conda)

### 1️⃣ Install Miniconda
Download from:
https://docs.conda.io/en/latest/miniconda.html

✔ Add Conda to PATH during installation

---

### 2️⃣ Create Correct Environment
```bash
conda create -n handsync python=3.11 -y
conda activate handsync
```

---

### 3️⃣ Install Dependencies (Pinned Versions)
```bash
pip install opencv-python pyautogui mediapipe==0.10.9 numpy
```

⚠️ **DO NOT upgrade MediaPipe**

---

## ▶️ Run HandSync
```bash
python visual_ctrl.py
```

Press **Q** to quit safely.

---

## 📂 Project Structure
```
HandSync/
│
├── visual_ctrl.py   # Main controller
├── README.md        # This file
```

---

## 🔧 Configuration (Inside Code)
```python
SMOOTHING = 6      # Cursor smoothness
FRAME_R = 100      # Active area padding
SCROLL_SPEED = 20  # Scroll intensity
```

Increase `SMOOTHING` → smoother but slower cursor  
Decrease it → faster but shakier

---

## 🚧 Roadmap (Coming Soon)
These features are **planned and in progress**:

🔜 Drag & drop gesture  
🔜 Right‑click gesture  
🔜 Volume control via pinch distance  
🔜 Gesture calibration UI  
🔜 FPS & latency overlay  
🔜 Multi‑hand support  
🔜 Application‑specific profiles  

---

## ⚠️ Known Limitations
- Requires good lighting
- Single‑hand tracking only (for now)
- Webcam quality affects accuracy

---

## 👨‍💻 Author & Credits
**HandSync**  
© 2025 **Prince Raj Singh** & **K. Harish** 
Group: **Carnage Sentinels**

Built using:
- OpenCV
- MediaPipe
- PyAutoGUI

---

## 📜 License
MIT License – Free to use, modify, and share with attribution.

---

🪄 *Wave less. Do more.*

# HandSync

## ⚠️ Disclaimer: The Cauldron Bubbles!

**This project is under active development!** We're brewing new functionalities, refining spells, and squashing bugs. Expect updates, improvements, and possibly some magical mishaps. Use at your own risk—HandSync is not responsible for any accidental tab closures or unexpected media pauses. Contributions and feedback are welcome to help perfect this sorcery!

Welcome to **HandSync**, the ultimate hand-gesture wizardry tool that transforms your webcam into a magical conduit for controlling your computer! Wave your hands like a maestro and command your digital realm with intuitive gestures. Whether you're scrolling through epic tales, pausing dramatic scenes, or closing pesky tabs, this Python-powered enchantment makes it all possible.

## 🌟 What Makes This Spellbinding?

HandSync harnesses the arcane arts of computer vision and machine learning to detect hand gestures in real-time. Built with OpenCV, MediaPipe, and PyAutoGUI, it bridges the gap between your physical movements and digital actions. No wands required—just your webcam and a dash of hand magic!

### Key Enchantments:
- **Real-Time Gesture Detection**: Processes live video feed at lightning speed.
- **Cooldown Mechanism**: Prevents accidental spell casts with a 0.5-second cooldown.
- **Visual Feedback**: See your gestures in action with on-screen labels and landmarks.
- **Customizable Gestures**: Easily tweak finger logic for personalized sorcery.
- **Cross-Platform Control**: Works on any system with Python and a webcam.

## 🖐️ Gesture Spells & Their Secrets

Dive into the grimoire of gestures! Each spell is defined by finger positions (Thumb, Index, Middle, Ring, Pinky) and triggers specific actions. Here's the enchanted table from our ancient scrolls:

| Function          | Physical Gesture          | Finger Logic (T-I-M-R-P) | Why It Works |
|-------------------|---------------------------|---------------------------|--------------|
| Neutral / Ready  | Open Palm                | [1, 1, 1, 1, 1]         | System waits; no actions fired. |
| Play             | Closed Fist              | [0, 0, 0, 0, 0]         | High-intent action, easy to detect. |
| Pause            | Finger Tight             | [0, 1, 1, 1, 1]         | Index/Mid/Ring/Pinky up but pressed together. |
| Scroll Mode      | "V" Sign                 | [0, 1, 1, 0, 0]         | Index and Middle up, others strictly down. |
| Left Click       | Index Pinch              | [0, 1, 0, 0, 0] + Thumb | Thumb touches Index while other fingers closed. |
| Address (Tab)    | Pointing                 | [0, 1, 0, 0, 0]         | Single finger extension; moves focus. |
| Close Tab        | "The OK"                 | [Thumb + Index] Circle   | Uses distance math to avoid "Pinch" confusion. |

## 🛠️ Summoning the Spell (Installation)

To awaken HandSync, you'll need Python 3.x and a trusty webcam. Follow these incantations:

1. **Clone the Repository**:
   ```
   git clone https://github.com/your-repo/handsync.git
   cd handsync
   ```

2. **Install the Arcane Dependencies**:
   ```
   pip install opencv-python mediapipe pyautogui
   ```

3. **Grant Permissions**: Ensure your webcam is accessible and PyAutoGUI has control over your system inputs.

## 🚀 Casting the Spell (Usage)

1. Run the enchantment:
   ```
   python visual_ctrl.py
   ```

2. A window titled "HandSync" will appear, showing your webcam feed.

3. Perform gestures in front of the camera. Watch the "CMD" label for feedback!

4. Press 'q' to dispel the spell and exit.

### Tips for Mastery:
- Position your hand clearly in the frame.
- Experiment with lighting for better detection.
- Customize `COOLDOWN`, `W_CAM`, and `H_CAM` in the script for your setup.

## 📜 Copyright

© 2025 PRINCE RAJ SINGH (Group: CArnage Sentinels). All rights reserved. This project is open-source under the MIT License (or your chosen license). Feel free to fork, modify, and share, but give credit where due!
# 🎭 Swipe That Face!

![Banner](logo/banner.png)

> An interactive and expressive game that challenges your face to keep up!

Swipe That Face! is a face filter game where you mimic fun facial expressions in real-time. From playful winks to wide smiles, test your mimicry skills and progress through levels designed to get your face moving and laughing!

---

## 🔥 Key Features
- 🎮 **User-Friendly Gameplay** – Easy to play, hard to master!
- 🧠 **Real-Time Face Processing** – Powered by face landmarks and expression detection.
- 🎨 **Modern UI** – Clean, responsive, and aesthetic visuals for maximum enjoyment.

---

## 📁 Folder Structure

```plaintext
Assets/
├── kedip.png
├── merem.png
├── senyum.png
├── senyumlebar.png
logo/
├── banner.png
├── icon.png
sound/
├── backsound.mp3
├── berhasil.mp3
.gitignore
expression.py
facedetect.py
game.py
gui.py
main.py
qtgame.py
readme.md
requirements.txt
utils.py
```

## 👥 Project Team

| Name          | Student ID | GitHub ID        |
|---------------|------------|------------------|
| Rahmat Aldi Nasda       | 122140077 | [@urbaee](https://github.com/urbaee) |
| Shafa Aulia    | 122140062 | [@shaapaa](https://github.com/shaapaa) |
| Naufal Saqib Athaya     | 122140072 | [@pallskii](https://github.com/pallskii) |

---

## 📓 Logbook

| Week | Date       | Activities                                | Progress         |
|------|------------|--------------------------------------------|------------------|
| 1    | 2025-05-08 | Project initiation   | 10%, brainstorming the core logic, defining game mechanics, and initiating basic code structure.          |
| 2    | 2025-05-18 | - Adding face detection <br> - Adding cam selector <br> - Adding simple GUI |  25%, Successfully implemented initial face tracking, added basic camera selection, and created a prototype GUI for early testing.           |
| 3    | 2025-03-19 | - Fixing minor issue <br> - Adding filter code       | 50%, resolved early bugs and integrated filter expression logic for real-time face effect matching.    |
| 5    | 2025-03-25 | - Refactoring code <br> - Adding more assets <br> - Adding sound effect and more function <br> - Initiation the report          | 75%, optimized codebase for scalability, enhanced user experience with visual and audio assets, and started documentation draft.  |
| 5    | 2025-03-29 | - Adding interactive GUI for easy use (user-friendly) <br> - Fixing sound effect <br> - Report still in progress          | 90%, completed interactive and intuitive GUI, finalized sound integration, and advanced report writing phase. |
| 6    | 2025-03-30 | - Adding icon and logo <br> - Adding backsound for the filter game <br> - Adding .gitignore <br> - Updating README.md  <br> - Report still in progress        | 95%, finalized branding elements, enriched audio-visual experience, cleaned up project structure, and polished documentation. |

---

## ⚙️ Installation Guide

> Make sure you have **Python 3.8+** and a **working webcam**.

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/swipe-that-face.git
cd swipe-that-face
```
2. **Install dependencies**

We recommend you to use UV or Conda as a virtual environment to avoid package collisions.
```bash
uv pip install -r requirements.txt
or 
pip install -r requirements.txt
```

3. **Run the game**

```bash
python main.py
```


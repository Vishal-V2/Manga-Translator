# 📖 Manga Translator

A powerful end-to-end manga translation tool that automatically detects speech bubbles, cleans up artwork, and translates manga images to any target language.

## ✨ Features

- **Automatic Speech Bubble Detection** — Identifies all text containers in manga pages
- **AI-Powered Text Recognition** — Extracts text using advanced OCR models
- **Intelligent Cleaning** — Removes original text while preserving artwork quality
- **Seamless Translation** — Translates content using state-of-the-art LLMs
- **Professional Typesetting** — Renders translated text with proper formatting
- **Batch Processing** — Handle multiple manga pages at once

## 🚀 Quick Start

1. Create a folder named `out` in the same directory as `app.py`
2. Place all your manga images in the `out` folder
3. Run the application — translated results will be saved to the `output` folder

## 📋 Pipeline Overview

### 1. Original Image
Source manga page ready for processing.

![Original Image Placeholder](https://via.placeholder.com/400x600?text=Original+Image)

### 2. Speech Bubble Detection
AI identifies and isolates all text regions in the image.

![Speech Detection Placeholder](https://via.placeholder.com/400x600?text=Speech+Bubble+Detection)

### 3. Image Cleanup
Original text is removed while preserving artwork integrity.

![Cleaned Image Placeholder](https://via.placeholder.com/400x600?text=Cleaned+Image)

### 4. Translated Output
Final result with translated text professionally typeset.

![Translated Image Placeholder](https://via.placeholder.com/400x600?text=Translated+Image)

## 📦 Requirements

- Python 3.8+
- PyYAML
- PySide6
- ONNX Runtime
- EasyOCR
- Manga OCR
- Additional dependencies in `requirements.txt`

## 📚 Installation

```bash
pip install -r requirements.txt
```

## 🎮 Usage

```bash
python app.py
```

The GUI will launch and automatically process all images in the `out` folder, displaying results in the main window.

## 🤖 Supported Models

- **Speech Bubble Detection**: YOLOv11L optimized for manga
- **Text Cluster Detection**: YOLOv11L for text region segmentation
- **OCR**: EasyOCR & Manga OCR for multilingual text recognition
- **Inpainting**: MIGAN v2 & LaMa for artwork restoration
- **Translation**: Deepseek, Gemini, Groq, LLaMA support

## 📁 Project Structure

```
pipeline/
├── core/
│   ├── detection/      # Speech bubble & text detection
│   ├── recognition/    # OCR models
│   ├── translation/    # LLM translation backends
│   ├── cleaning/       # Inpainting & text removal
│   ├── typesetting/    # Text rendering
│   └── utility/        # Helper functions
├── manager/            # Pipeline orchestration
└── worker/             # Task processing workers
```

## 📝 License

See [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for manga fans everywhere**

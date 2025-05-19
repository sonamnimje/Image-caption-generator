# AI Image Caption Generator

This is a web application that generates captions for images using AI. It uses the Hugging Face Transformers library with a pre-trained Vision Encoder-Decoder model to generate descriptive captions for uploaded images.

## Features

- Drag and drop image upload
- Real-time image preview
- AI-powered caption generation
- Modern and responsive UI
- Error handling and loading states

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd image-caption-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # Since you're on Windows
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an image by either:
   - Dragging and dropping an image onto the drop zone
   - Clicking the drop zone and selecting an image from your file system

4. Wait for the AI to generate a caption for your image

## Technical Details

- Backend: Flask (Python)
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- AI Model: Hugging Face Transformers (Vision Encoder-Decoder)
- Image Processing: Pillow

## Note

The first time you run the application, it will download the pre-trained model which might take a few minutes depending on your internet connection. 
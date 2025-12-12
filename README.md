# AwareMeme AI: Intelligent Meme System for Social Good

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

> An AI-powered meme generator that transforms awareness topics and government policies into engaging, humorous memes using Google's Gemini 3.0 multimodal model.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

**AwareMeme AI** is a Generative AI-powered meme generator designed specifically for social awareness campaigns. The system automatically generates context-aware captions and corresponding meme images from user-provided topics including government policies, mental health, road safety, cyberbullying, and other social issues.

This project demonstrates how modern multimodal AI systems can enhance public communication by automating both linguistic and visual generation tasks, making awareness content creation faster, more engaging, and scalable.

### Why AwareMeme AI?

- **Automated Creation**: Eliminates the need for manual design and caption writing
- **Scalable**: Generate unlimited variations on any awareness topic
- **Accessible**: Simple interface requiring no design skills
- **Responsible**: Built-in safety filters ensure appropriate, non-offensive content
- **Fast**: Generate complete memes in seconds

## ✨ Features

- 🤖 **AI-Powered Generation**: Leverages Google Gemini 3.0 for both text and image creation
- 🎨 **Dynamic Styling**: Automatically selects appropriate meme styles (reaction, character, relatable, sarcastic)
- 📝 **Structured Output**: JSON-formatted captions with top text, bottom text, and descriptions
- 🛡️ **Content Safety**: Built-in filters to prevent offensive or inappropriate content
- 🌐 **Web Interface**: User-friendly frontend for easy meme generation
- ⚡ **High Performance**: FastAPI backend ensures quick response times
- 💾 **Downloadable**: Instant download of generated memes
- 🎯 **Topic Versatility**: Supports wide range of awareness categories

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, high-performance web framework
- **Python 3.13+** - Core programming language
- **Google Gemini 3.0** - Multimodal AI model (`gemini-3-pro-image-preview`)
- **Pydantic** - Data validation

### Frontend
- **HTML5/CSS3** - User interface
- **JavaScript** - Client-side interactions

### Key Libraries
- `google-genai` - Google Generative AI SDK
- `fastapi` - Backend framework
- `uvicorn` - ASGI server

## 🏗️ System Architecture

```
┌─────────────┐
│   Frontend  │
│  (HTML/JS)  │
└──────┬──────┘
       │ HTTP POST
       ▼
┌─────────────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │ API Call
       ▼
┌─────────────┐
│  Gemini 3.0 │
│   (GenAI)   │
└──────┬──────┘
       │
       ├─► Text Generation (JSON Caption)
       │
       └─► Image Generation (Base64)
```

### Workflow

1. **User Input**: Topic entered through web interface
2. **Prompt Engineering**: Backend constructs structured prompt
3. **AI Generation**: Gemini model generates caption (JSON) and image
4. **Response Parsing**: Backend extracts text and image data
5. **Display**: Frontend renders meme with preview and download options

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- Google AI API Key ([Get one here](https://ai.google.dev/))
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/pari006/AwareMemeAI.git
cd AwareMemeAI
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn google-generativeai pydantic
```

4. **Configure API Key**

Open `main.py` and replace the API key:
```python
API_KEY = "your_actual_gemini_api_key_here"
```

⚠️ **Security Note**: Never commit your API key to version control. Consider using environment variables:
```python
API_KEY = os.getenv("GEMINI_API_KEY")
```

5. **Run the application**
```bash
# From the project root directory
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

6. **Access the frontend**

Open `index.html` in your web browser or serve it using a local server:
```bash
# Using Python's built-in server
python -m http.server 8080
```

Then navigate to `http://localhost:8080`

## 🚀 Usage

### Web Interface

1. Open the web application in your browser
2. Enter an awareness topic or government rule in the text field
3. Click "Generate Meme"
4. Preview the generated meme
5. Download the image using the download button

### Example Topics

Try these sample topics:

- "Wear helmets while driving"
- "New income tax slabs for FY 2025-26"
- "Mental health check-ins are important"
- "Cyberbullying awareness campaign"
- "Traffic fine rules updated"
- "Save water, save future"
- "Digital literacy for seniors"

## 📚 API Documentation

### Endpoint: Generate Meme

**POST** `/generate`

#### Request Body

```json
{
  "topic": "string",
  "top_text": "string (optional)",
  "bottom_text": "string (optional)"
}
```

#### Response

```json
{
  "caption": "string",
  "image_b64": "base64_encoded_image_string"
}
```

#### Example Request (cURL)

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Wear seatbelts for safety"}'
```

#### Example Response

```json
{
  "caption": "Meme about road safety and seatbelt usage",
  "image_b64": "iVBORw0KGgoAAAANSUhEUgA..."
}
```

### Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Project Structure

```
awarememe-ai/
│
├── backend/
│   └── main.py              # FastAPI application & API endpoints
│
├── frontend/
│   ├── index.html           # Main web interface
│   ├── style.css            # UI styling
│   └── script.js            # Client-side logic
│
├── docs/
│   └── STTP (1).pdf         # Project documentation
│
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## 🎨 Examples

### Generated Memes

**Topic**: "New traffic fine rules"

**Output**:
- **Top Text**: "Government announces new traffic fines"
- **Bottom Text**: "My wallet is already crying"
- **Style**: Reaction meme with exaggerated facial expression

---

**Topic**: "Mental health awareness"

**Output**:
- **Top Text**: "Remember to check in on yourself"
- **Bottom Text**: "Self-care isn't selfish"
- **Style**: Supportive character meme with soft visuals

---

**Topic**: "Cyberbullying prevention"

**Output**:
- **Top Text**: "Think before you type"
- **Bottom Text**: "Words have impact"
- **Style**: Thoughtful expression meme

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add comments for complex logic
- Test thoroughly before submitting PRs
- Update documentation if adding new features

## 🔮 Future Enhancements

- [ ] Multilingual support (Hindi, Spanish, French, etc.)
- [ ] Custom meme template selection
- [ ] Social media integration (Twitter, Instagram auto-posting)
- [ ] User accounts and saved memes
- [ ] Batch meme generation
- [ ] Advanced style customization
- [ ] Analytics dashboard
- [ ] Mobile application

## 📄 License

This project is developed as part of an academic project at **Galgotias University** for the Bachelor of Technology in Computer Science and Engineering with specialization in AI and ML.

**Submitted by**:
- Pari Srivastava 

**Mentor**: Dr. Garima Pandey  
**Institution**: School of Computer Science and Engineering, Galgotias University

## 🙏 Acknowledgments

- **Google AI** for the Gemini 3.0 multimodal model
- **FastAPI** team for the excellent framework
- **Dr. Garima Pandey** for guidance and mentorship
- **Galgotias University** for supporting this research project

## 📞 Contact

For questions, suggestions, or collaboration opportunities:

- **Email**: [parisrivastava006@gmail.com]
- **LinkedIn**: [https://www.linkedin.com/in/pari-srivastava-a80b762a5/]
- **Github**: [https://github.com/pari006]

---

<div align="center">

**Made with ❤️ for Social Good**

If you find this project useful, please consider giving it a ⭐ on GitHub!

</div>
# 🤖 CAD AI - Intelligent 3D Modeling Assistant

An innovative **AI-powered CAD assistant** that transforms natural language descriptions into production-ready 3D models in FreeCAD. Uses **Ollama (DeepSeek AI)** for intelligent interpretation and **FreeCAD** for precision CAD generation.

---

## ✨ Key Features

### 🧠 **AI-Powered Interpretation**
- Uses **DeepSeek-r1 3B** (Ollama) running locally for intelligent part description parsing
- Natural language support: describe what you want, the AI interprets it
- Parametric inputs: size, width, height, thickness customization
- Fast inference with offline processing (no cloud dependency)

### 🎨 **15+ Parametric CAD Shapes**
Generate production-ready 3D models instantly:

| Shape | Capabilities |
|-------|--------------|
| **Prosthetic Arm** | Full anatomical assembly with socket, shoulder, joint, forearm, wrist, hand, fingers & thumb |
| **Hollow Box** | Customizable dimensions with adjustable wall thickness |
| **Sphere** | Parametric sphere generation |
| **Hollow Cylinder** | Tube generation with custom wall thickness |
| **Cone** | Parametric cone with height control |
| **Spur Gear** | 18-tooth gear with hub and axle |
| **Bolt** | Complete bolt assembly with head and slot |
| **L-Bracket** | Load-bearing bracket with mounting holes |
| **Tube** | Seamless hollow tubes for piping |
| **Spring** | Coiled springs with customizable parameters |
| **Spoked Wheel** | 5-spoke wheel assembly with tire, rim, and axle |
| **Frame** | Structural frame components |
| **Hexagon** | Precision hex shapes (bolts, fasteners) |
| **Pipe** | Industrial pipe generation |
| **Plate** | Flat plate components |

### 🗣️ **Voice Feedback**
- Real-time text-to-speech confirmation using **pyttsx3**
- Offline voice generation (no external TTS API required)
- Customizable speech rate and tone

### 🖥️ **Intuitive GUI**
- Clean Tkinter interface for easy interaction
- Scrollable text displays for review
- Live status updates and error handling
- Professional layout with clear call-to-action buttons

### ⚡ **Smart Parametrization**
Automatically calculates proportional dimensions:
```
Example Input: "prosthetic arm 150"
Output: Full prosthetic arm model with proportional socket, joints, and hand
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **FreeCAD 1.0+** ([Download](https://www.freecadweb.org/))
- **Ollama** with DeepSeek model ([Setup Guide](https://ollama.ai))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rufuspitta-ux/cad-ai.git
   cd cad-ai
   ```

2. **Install Python dependencies**
   ```bash
   pip install pyttsx3 requests
   ```

3. **Ensure Ollama is running**
   ```bash
   ollama serve
   ollama pull deepseek-r1:3b
   ```

4. **Configure paths** (if needed)
   Edit `engineering.py` and update:
   ```python
   FREECAD = r"C:\Path\To\FreeCAD\bin\FreeCAD.exe"
   OLLAMA_URL = "http://localhost:11434/api/generate"
   ```

5. **Run the application**
   ```bash
   python engineering.py
   ```

---

## 📹 Demo Video

Watch the CAD AI in action - generating a prosthetic arm assembly from a simple text description:

[![CAD AI Demo - Prosthetic Arm](demo_arm.mp4)](demo_arm.mp4)

**What you'll see:**
- Natural language input processing
- AI parsing and parameter extraction
- Real-time FreeCAD model generation
- Interactive part visualization
- Complete assembly with joints and articulation

---

## 💡 Usage Examples

### Basic Usage
```
Input: "arm 150"
Output: ✅ Prosthetic arm launched in FreeCAD!
        → Full arm assembly with proportional dimensions
```

### Advanced Parameters
```
Input: "gear 80mm"
Output: ✅ Spur gear generating!
        → 18-tooth gear with 80mm diameter

Input: "hollow box 100x60x40"
Output: ✅ Hollow box ready!
        → 100×60×40mm box with 5mm wall thickness

Input: "wheel 200"
Output: ✅ Wheel launching now!
        → 200mm diameter spoked wheel with tire and hub
```

---

## 🏗️ Technical Architecture

### AI Pipeline
1. **User Input** → Natural language description
2. **Ollama Processing** → JSON parameter extraction
3. **Shape Library** → Parametric Python generation
4. **FreeCAD Python API** → 3D topology creation
5. **Visualization** → Interactive 3D display

### Shape Library Structure
```
Shape → Parameters (size, width, height, thickness)
     → FreeCAD Python Code Generation
     → Part Assembly (Boolean operations)
     → Export/Display
```

### AI Model Specs
- **Model**: DeepSeek-r1:3b
- **Precision**: 0.1 (deterministic output)
- **Max Tokens**: 250
- **Response Format**: JSON (structured output)

---

## 🛠️ Configuration

### Customize Speech
```python
_engine.setProperty("rate", 160)  # Speech speed (default: 160)
```

### Adjust AI Temperature
```python
"options": {"temperature": 0.1, "num_predict": 250}
```

### Add Custom Shapes
Extend the shape library by adding new CAD functions:
```python
def cad_custom(p):
    S = val(p, "size", 100)
    code = f"""
    # Your FreeCAD Python code here
    result = Part.makeSphere({S})
    """
    return code, "Custom Shape"
```

---

## 📦 Project Structure

```
cad-ai/
├── engineering.py              # Main application
├── demo_arm.mp4               # Demo video
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── LICENSE                    # MIT License
```

---

## 🎯 Capabilities Summary

| Feature | Status | Details |
|---------|--------|---------|
| AI Interpretation | ✅ | DeepSeek 3B with JSON output |
| Local Processing | ✅ | No cloud/API dependency |
| 15+ CAD Shapes | ✅ | Full parametric support |
| Voice Feedback | ✅ | Offline TTS with pyttsx3 |
| FreeCAD Integration | ✅ | Direct Python API automation |
| GUI Interface | ✅ | Tkinter-based user interface |
| Real-time Rendering | ✅ | Live 3D visualization |
| Export Support | ✅ | FreeCAD native formats |

---

## 🔧 Troubleshooting

### FreeCAD Not Found
Ensure FreeCAD path is correct:
```bash
# Windows
C:\Users\[Username]\AppData\Local\Programs\FreeCAD 1.0\bin\FreeCAD.exe
```

### Ollama Connection Error
```bash
# Check Ollama is running
ollama serve

# Verify model is installed
ollama list | grep deepseek
```

### Voice Not Working
```python
# Reinstall pyttsx3
pip install --upgrade pyttsx3
```

---

## 📝 System Prompts

The AI uses a sophisticated system prompt to ensure consistent JSON output:

```
"You are Jarvis, a CAD assistant. The user describes a 3D part.
Reply ONLY with a JSON object — no markdown, no explanation."
```

This ensures reliable parameter extraction for all shapes.

---

## 🌟 Future Enhancements

- [ ] Support for STL/STEP export
- [ ] Advanced material properties
- [ ] Assembly constraint automation
- [ ] Multi-part design capability
- [ ] Web-based interface
- [ ] Real-time parameter optimization
- [ ] Design history/undo stack

---

## 📄 License

This project is licensed under the **MIT License** - see LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit pull requests

---

## 📧 Support

For issues, questions, or feature requests:
- **GitHub Issues**: [Open an issue](https://github.com/rufuspitta-ux/cad-ai/issues)
- **Contact**: [Your Contact Info]

---

## 🙏 Acknowledgments

- **FreeCAD** - Open-source CAD platform
- **Ollama** - Local LLM inference engine
- **DeepSeek** - Efficient 3B model
- **JARVIS Concept** - Inspired by intelligent assistants

---

**Made with ❤️ by Rufus Pitta**


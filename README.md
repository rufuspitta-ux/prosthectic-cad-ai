# 🦾 Prosthetic CAD AI

**Intelligent Prosthetic Design Generation Using Natural Language and AI**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![AI-Powered](https://img.shields.io/badge/AI%20Powered-LLM%2FCAD-ff69b4.svg)

---

## 🎯 Overview

**Prosthetic CAD AI** bridges the gap between clinical requirements and CAD engineering using **natural language and artificial intelligence** to automatically generate 3D prosthetic models.

Instead of manual CAD design workflows where clinicians describe prosthetics and engineers manually design them, this system allows doctors and prosthetists to describe prosthetic specifications in plain English, and the AI generates production-ready 3D models in FreeCAD format.

### 💡 The Problem We Solve

- ⏱️ **Time-Consuming:** Manual CAD design takes hours per prosthetic
- 💰 **Expensive:** Requires specialized CAD engineers
- 📞 **Communication Gap:** Clinicians and engineers often miscommunicate
- 🔄 **Repetitive:** Similar designs are redesigned from scratch
- 🌍 **Access:** Limited CAD expertise in developing regions

### ✅ Our Solution

- 🤖 **AI-Powered:** Local LLM processes natural language descriptions
- ⚡ **Fast:** Generate designs in minutes instead of hours
- 💻 **Automated:** Minimal human intervention required
- 📚 **Learnable:** System improves with usage patterns
- 🌍 **Accessible:** Works offline with local LLM (Ollama)

---

## 🚀 Key Features

- ✅ **Natural Language Processing:** Describe prosthetics in plain English
- ✅ **Automated CAD Generation:** Direct integration with FreeCAD
- ✅ **3D Model Output:** Production-ready prosthetic designs
- ✅ **Local LLM Support:** Privacy-first using Ollama
- ✅ **Customization:** Adjust parameters easily
- ✅ **Scalable:** Handle batch designs
- ✅ **Version Control:** Track design iterations
- ✅ **Open Source:** MIT licensed, community-driven

---

## 🔬 Technology Stack

### Core Technologies
- **Python 3.9+** - Primary language
- **Ollama** - Local LLM inference (privacy-first)
- **FreeCAD API** - 3D modeling and CAD automation
- **LangChain** - LLM orchestration
- **FastAPI** - REST API backend

### AI & Machine Learning
- **Language Models:** Mistral, Llama 2 (via Ollama)
- **Embeddings:** Local embeddings for semantic understanding
- **Prompt Engineering:** Specialized prompts for CAD generation

### Supporting Libraries
- **numpy** - Numerical computing
- **pydantic** - Data validation
- **pytest** - Testing framework
- **docker** - Containerization

---

## 📋 Example Usage

### Basic Example

**Input:**
```
"Generate a right-hand prosthetic with finger-length of 75mm, 
wrist circumference of 170mm, with carbon fiber material properties"
```

**Output:**
```
✓ Design generated in 45 seconds
✓ Model exported to: designs/prosthetic_right_hand_20260523.step
✓ Weight estimate: 150g
✓ Material: Carbon Fiber Reinforced Polymer
```

### API Example

```python
from prosthetic_cad_ai import ProstheticDesigner

# Initialize
designer = ProstheticDesigner(model="mistral")

# Generate design
result = designer.generate_prosthetic(
    description="Left transtibial prosthetic for 45-year-old male, 
                athletic activity level, energy-return foot",
    parameters={
        "material": "composite",
        "activity_level": "high",
        "weight_limit": 500  # grams
    }
)

# Access results
print(f"Design ID: {result.design_id}")
print(f"File Path: {result.file_path}")
print(f"Estimated Weight: {result.weight_estimate}g")
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- FreeCAD 0.21+
- Ollama (or access to LLM API)
- 4GB RAM minimum (8GB recommended)
- 5GB disk space

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/rufuspitta-ux/prosthectic-cad-ai.git
cd prosthectic-cad-ai
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install FreeCAD
```bash
# Ubuntu/Debian
sudo apt-get install freecad

# macOS
brew install freecad

# Windows: Download from https://www.freecad.org/
```

#### 5. Install & Run Ollama
```bash
# Download from: https://ollama.ai/

# Pull model (e.g., Mistral)
ollama pull mistral

# Start Ollama server
ollama serve
```

#### 6. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### First Run

```bash
# Test setup
python setup_check.py

# Generate sample prosthetic
python examples/generate_sample.py

# Start API server
python api/main.py
```

---

## 📁 Project Structure

```
prosthectic-cad-ai/
├── README.md                          # Documentation
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── requirements.txt                   # Dependencies
├── setup.py                           # Package setup
│
├── src/
│   ├── prosthetic_designer.py         # Main designer class
│   ├── llm_interface.py               # LLM integration (Ollama)
│   ├── cad_generator.py               # FreeCAD automation
│   ├── parameter_extractor.py         # NLP → CAD parameters
│   ├── validator.py                   # Design validation
│   └── utils.py                       # Helper functions
│
├── api/
│   ├── main.py                        # FastAPI application
│   ├── routes.py                      # API endpoints
│   ├── schemas.py                     # Pydantic models
│   └── middleware.py                  # Auth & logging
│
├── prompts/
│   ├── base_prompt.txt                # Core prompt template
│   ├── prosthetic_prompts.txt         # Prosthetic-specific
│   └── extraction_prompts.txt         # Parameter extraction
│
├── examples/
│   ├── generate_sample.py
│   ├── batch_generation.py
│   └── api_client.py
│
├── tests/
│   ├── test_llm_interface.py
│   ├── test_cad_generator.py
│   └── test_integration.py
│
└── docs/
    ├── ARCHITECTURE.md
    └── API_REFERENCE.md
```

---

## 🔌 API Endpoints

### Generate Prosthetic Design
```
POST /api/v1/generate
Content-Type: application/json

{
  "description": "Right hand prosthetic with finger joints",
  "parameters": {
    "material": "carbon_fiber",
    "weight_limit": 200
  }
}

Response:
{
  "design_id": "prosthetic_20260523_001",
  "status": "completed",
  "file_path": "/outputs/prosthetic_20260523_001.step",
  "estimated_weight": 185,
  "processing_time_seconds": 45,
  "confidence_score": 0.92
}
```

### Get Design Status
```
GET /api/v1/designs/{design_id}
```

### List Designs
```
GET /api/v1/designs?limit=10&offset=0
```

### Download Design File
```
GET /api/v1/designs/{design_id}/download
```

See [API_REFERENCE.md](docs/API_REFERENCE.md) for full documentation.

---

## 🔐 Security & Privacy

- ✅ **Local Processing:** All LLM processing happens locally (Ollama)
- ✅ **No Cloud Upload:** Designs never leave your system
- ✅ **Data Encryption:** Optional encryption for sensitive designs
- ✅ **Access Control:** Role-based authentication
- ✅ **Audit Logging:** Track all design generations
- ✅ **HIPAA Compatible:** Design ready for healthcare compliance

---

## 📊 Supported Prosthetic Types

| Type | Status | Details |
|------|--------|---------|
| Upper Limb (Hand) | ✅ Supported | Transcarpal, transradial, transhumeral |
| Upper Limb (Arm) | ✅ Supported | Various attachment points |
| Lower Limb (Foot) | ✅ Supported | SACH, dynamic response, microprocessor |
| Lower Limb (Leg) | ✅ Supported | Transtibial, transfemoral |
| Hybrid | 🔄 Planned | Multi-component designs |
| Modular | 🔄 In Development | Mix-and-match components |

---

## 🧪 Testing

Run tests:

```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_cad_generator.py -v

# With coverage
pytest --cov=src tests/
```

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - System design
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup
- [Usage Guide](docs/USAGE_GUIDE.md) - How to use the system
- [API Reference](docs/API_REFERENCE.md) - API endpoints

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report issues
- Feature request guidelines
- Code contribution workflow
- Testing requirements

### Areas Seeking Contributions
- [ ] Additional prosthetic types
- [ ] Material database expansion
- [ ] Web UI development
- [ ] Mobile app
- [ ] Performance optimization
- [ ] Additional LLM support
- [ ] Documentation improvements

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🏥 Medical & Ethical Considerations

**Important:** This is an AI-assisted design tool. Clinical adoption requires:

- [ ] Medical professional review
- [ ] Clinical validation studies
- [ ] Regulatory approval (FDA/CE)
- [ ] Integration with certified manufacturing
- [ ] Proper documentation and QA
- [ ] Patient consent and safety protocols

**Disclaimer:** Not approved for autonomous clinical decision-making.

---

## 🙏 Acknowledgments

- FreeCAD community
- Ollama and local LLM initiatives
- Prosthetics research community
- Healthcare AI innovators

---

## 📮 Support & Contact

- 🐛 **Report Issues:** [GitHub Issues](https://github.com/rufuspitta-ux/prosthectic-cad-ai/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/rufuspitta-ux/prosthectic-cad-ai/discussions)
- 📧 **Email:** rufuspitta@gmail.com
- 💼 **LinkedIn:** [Connect with me](https://linkedin.com/in/rufus-pitta)

---

## 🗺️ Roadmap

**Q3 2026:**
- [ ] Web interface
- [ ] Real-time preview
- [ ] Material library expansion

**Q4 2026:**
- [ ] Mobile app (iOS/Android)
- [ ] Batch processing engine
- [ ] Performance optimization

**2027:**
- [ ] Multi-language support
- [ ] Advanced customization
- [ ] Integration with 3D printers
- [ ] Clinical validation partnership

---

**Revolutionizing Prosthetic Design with AI | Built for Clinicians & Engineers**

---

*Last Updated: May 2026 | Status: Active Development | Version: 1.0.0*

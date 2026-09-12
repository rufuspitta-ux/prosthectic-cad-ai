# Prosthetic CAD AI

A desktop engineering prototype that converts short **natural-language design requests into parameterized FreeCAD geometry** using a local Ollama model, with a deterministic keyword fallback when the LLM is unavailable.

> **Research / engineering prototype:** This project does not generate clinically validated, patient-specific, or manufacturing-ready prostheses. Generated geometry requires qualified engineering review, dimensional verification, material analysis, fit assessment, mechanical testing, and appropriate regulatory controls before real-world use.

## Why this project is interesting

The core idea is to reduce the gap between a human design request and a CAD prototype:

```text
Natural-language request
          ↓
Local Ollama LLM
          ↓
Structured shape + parameters
          ↓
Parameter validation
          ↓
FreeCAD Python script
          ↓
Parameterized 3D geometry
```

If Ollama is unavailable or cannot produce a supported response, the application uses a keyword-based fallback.

## Current implementation

The checked-in application is currently centered on:

- `engineering.py` — Tkinter desktop application
- A 15-shape parameterized geometry library
- Local Ollama integration
- Structured response parsing
- Parameter bounds/checks in the application
- FreeCAD script generation
- Keyword fallback
- Optional offline speech output

Supported shape names include:

`arm` • `box` • `sphere` • `cylinder` • `cone` • `gear` • `bolt` • `bracket` • `tube` • `spring` • `wheel` • `frame` • `hex` • `pipe` • `plate`

## Example requests

```text
arm 150
gear 80
box 100x60x40
```

The current prototype focuses on demonstrating the **natural language → local AI → CAD automation** workflow rather than producing finished prosthetic designs.

## Requirements

- Python 3.9+
- Tkinter
- FreeCAD
- Optional: Ollama for local LLM generation

Python dependencies declared in `requirements.txt` include `requests` and `pyttsx3`.

FreeCAD is an external system dependency and is not installed by pip.

## Configuration

The application supports:

| Variable | Purpose |
|---|---|
| `FREECAD_BIN` | Full path to the FreeCAD executable |
| `OLLAMA_MODEL` | Local Ollama model name |
| `OLLAMA_URL` | Ollama generation endpoint |

Example Windows PowerShell configuration:

```powershell
$env:FREECAD_BIN = "C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
$env:OLLAMA_MODEL = "deepseek-r1:3b"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"
python engineering.py
```

Start Ollama separately if you want LLM-assisted generation:

```bash
ollama serve
ollama pull deepseek-r1:3b
```

## Run

```bash
python engineering.py
```

Inspect generated geometry in FreeCAD before treating it as an engineering artifact.

## Engineering safeguards and limitations

This prototype intentionally does **not** claim to solve patient-specific prosthetic design. It currently lacks:

- Automated geometric validation
- Patient-specific anatomical fitting
- Finite-element analysis
- Material/mechanical analysis
- Manufacturability checks
- Clinical validation
- Regulatory controls
- Automated end-to-end tests
- A persistent design catalog/API
- Reliable capture of FreeCAD process completion/results

FreeCAD is launched as a separate process, so failures may require inspection of the FreeCAD application/process.

The application also generates temporary Python scripts under the user's home directory. Those scripts should be reviewed before execution, especially in sensitive environments.

## Development roadmap

The next engineering improvements are:

1. Introduce a typed design schema for shapes and parameters.
2. Validate model output against that schema before generating CAD scripts.
3. Add automated geometry/parameter tests.
4. Capture FreeCAD process completion and errors.
5. Add reproducible example designs and screenshots.
6. Separate runtime and development dependencies.
7. Add export validation before allowing generated geometry to be saved.

## License

MIT License. See [LICENSE](LICENSE).

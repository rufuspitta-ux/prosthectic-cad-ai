# Jarvis CAD — Local AI → FreeCAD Automation

A desktop engineering prototype that turns short **natural-language design requests into bounded FreeCAD geometry** using a local Ollama model, with a deterministic keyword fallback when the LLM is unavailable.

**Core idea:** natural language → local AI → validated shape parameters → controlled FreeCAD script → 3D geometry.

> **Research / engineering prototype:** this project does not generate clinically validated, patient-specific, or manufacturing-ready prostheses. Generated geometry requires qualified engineering review, dimensional verification, material analysis, fit assessment, mechanical testing, and appropriate regulatory controls before real-world use.

## Demo

A recorded end-to-end demonstration is included in the repository:

**[▶ Watch the CAD generation demo (`demo_arm.mp4`)](./demo_arm.mp4)**

The demo shows the desktop workflow from a user command to generated FreeCAD geometry.

## How it works

```text
┌─────────────────────────┐
│ Natural-language request│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Local Ollama model      │
│ JSON command generation │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Validation + bounds     │
│ allowlisted shape types │
└────────────┬────────────┘
             │
             ├───────────────┐
             │               │
             ▼               ▼
┌─────────────────┐   ┌──────────────────┐
│ Shape generator │   │ Keyword fallback │
└────────┬────────┘   └────────┬─────────┘
         └──────────────┬──────┘
                        ▼
              ┌──────────────────┐
              │ FreeCAD script   │
              │ generation       │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ FreeCAD geometry │
              └──────────────────┘
```

A key engineering constraint is that the model does **not** directly generate arbitrary FreeCAD Python. The application validates the model response and routes it only to predefined geometry generators.

## What is implemented

- `engineering.py` — Tkinter desktop application
- 15 allowlisted geometry generators
- Local Ollama integration through the local generation endpoint
- Structured JSON extraction and response validation
- Positive, bounded dimension handling
- Deterministic keyword fallback when the LLM is unavailable
- FreeCAD script generation and separate-process launch
- Thread-safe Tkinter status/log updates
- Optional offline speech output with `pyttsx3`
- Unit tests covering validation, fallback parsing, and all shape generators

### Supported shapes

`arm` • `box` • `sphere` • `cylinder` • `cone` • `gear` • `bolt` • `bracket` • `tube` • `spring` • `wheel` • `frame` • `hex` • `pipe` • `plate`

## Example commands

```text
arm 150
gear 80
box 100x60x40
plate 120
```

The prototype demonstrates the **natural language → local AI → CAD automation** workflow. The generated shapes are illustrative engineering geometry, not finished prosthetic designs.

## Project structure

```text
prosthectic-cad-ai/
├── engineering.py       # Desktop application + CAD generators
├── test_engineering.py  # Unit tests
├── demo_arm.mp4         # Recorded workflow demonstration
├── requirements.txt     # Python dependencies
├── CHANGELOG.md         # Project history
├── CONTRIBUTING.md      # Contribution guidelines
└── LICENSE              # MIT license
```

## Requirements

- Windows-friendly Python environment
- Python 3.9+
- Tkinter
- FreeCAD
- Optional: Ollama for local LLM generation

Python dependencies declared in `requirements.txt` include `requests` and `pyttsx3`.

FreeCAD is an external system dependency and is not installed by pip.

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FreeCAD

Set `FREECAD_BIN` to the full path of the FreeCAD executable. For example:

```powershell
$env:FREECAD_BIN = "C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
```

### 3. Optional: enable local AI generation

Start Ollama and pull a local model:

```bash
ollama serve
ollama pull deepseek-r1:3b
```

The application defaults to:

```text
OLLAMA_MODEL=deepseek-r1:3b
OLLAMA_URL=http://localhost:11434/api/generate
```

These can also be overridden with environment variables.

## Run

```bash
python engineering.py
```

Example PowerShell configuration:

```powershell
$env:FREECAD_BIN = "C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
$env:OLLAMA_MODEL = "deepseek-r1:3b"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"
python engineering.py
```

## Test

The repository includes smoke/unit tests for core application logic:

```bash
pytest -q
```

The tests cover dimension validation, supported-shape vocabulary, fallback parsing, and CAD-code generation across all currently allowlisted shapes.

## Engineering safeguards

The project deliberately keeps the LLM inside a constrained command layer:

1. User text is sent to the local Ollama endpoint.
2. The returned JSON is parsed and validated.
3. Shape names are restricted to a fixed allowlist.
4. Dimensions are normalized to bounded positive values.
5. Only predefined Python geometry generators are used to create the FreeCAD script.
6. If the model path fails, a deterministic keyword parser can still produce a supported shape.

This keeps the prototype focused on **AI-assisted CAD orchestration** rather than executing arbitrary model-generated code.

## Current limitations

This prototype does **not** provide:

- Automated geometric correctness validation
- Patient-specific anatomical fitting
- Finite-element analysis
- Material or mechanical analysis
- Manufacturability validation
- Clinical validation
- Regulatory controls
- Patient/device outcome validation
- Persistent design storage or a design API
- Full verification of FreeCAD process completion/results
- A manufacturing-ready prosthesis workflow

FreeCAD runs as a separate process, so the user may need to inspect the FreeCAD window/process when generation fails.

The application creates temporary Python scripts under the user's home directory for FreeCAD execution. Those generated scripts are based on the application's predefined generators and should still be reviewed before use in sensitive environments.

## Roadmap

- Expand typed parameter schemas for individual shape families.
- Add stronger geometric invariants and parameter-level tests.
- Detect and report FreeCAD process completion/failure more reliably.
- Add reproducible example designs with saved screenshots.
- Separate runtime and development dependencies.
- Add export-time validation for generated geometry.

## License

MIT License. See [LICENSE](LICENSE).

# Prosthetic CAD AI

A desktop prototype that converts short natural-language shape requests into parameterized FreeCAD geometry using a local Ollama model, with a keyword fallback when Ollama is unavailable.

> **Research prototype:** This project does not generate clinically validated or manufacturing-ready prostheses. Every design requires qualified engineering review, geometric verification, material analysis, fit assessment, and appropriate regulatory controls before real-world use.

## Current implementation

The checked-in application is a single Tkinter program: `engineering.py`. It currently provides a local GUI, a 15-shape parameterized geometry library, Ollama JSON parsing, FreeCAD script generation, keyword fallback, and optional offline speech output. The repository does not currently contain the FastAPI service, Python package, `src/` layout, examples, or automated tests previously described in older documentation.

## Requirements

The prototype requires Python 3.9 or newer, Tkinter, FreeCAD, and optionally Ollama. The Python dependencies declared in `requirements.txt` are `requests` and `pyttsx3`. FreeCAD is an external system dependency and is not installed by pip.

## Configuration

The application reads the following environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `FREECAD_BIN` | A Windows FreeCAD path | Full path to the FreeCAD executable |
| `OLLAMA_MODEL` | `deepseek-r1:3b` | Local Ollama model name |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama generation endpoint |

On Linux or macOS, set `FREECAD_BIN` to the actual executable before starting the program. For example:

```bash
export FREECAD_BIN=/usr/bin/freecad
export OLLAMA_MODEL=deepseek-r1:3b
python engineering.py
```

On Windows PowerShell:

```powershell
$env:FREECAD_BIN = "C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
$env:OLLAMA_MODEL = "deepseek-r1:3b"
python engineering.py
```

To use the local LLM, start Ollama separately and ensure the selected model is available:

```bash
ollama serve
ollama pull deepseek-r1:3b
```

## Usage

Start the GUI with:

```bash
python engineering.py
```

Supported shape names include `arm`, `box`, `sphere`, `cylinder`, `cone`, `gear`, `bolt`, `bracket`, `tube`, `spring`, `wheel`, `frame`, `hex`, `pipe`, and `plate`. Example requests include `arm 150`, `gear 80`, and `box 100x60x40`.

The model response is restricted to a known shape vocabulary and numeric parameters are bounded by the application. The generated geometry is still only a prototype: inspect it in FreeCAD and do not treat the output as a validated prosthetic design.

## Known limitations

The current implementation launches FreeCAD as a separate process and reports that it was launched before the process has completed. FreeCAD-side failures therefore require inspection of the FreeCAD process. The prototype does not yet provide a persistent design catalog, API server, authentication, geometry validation, finite-element analysis, manufacturability checks, patient-specific fitting, or automated tests.

The application generates temporary Python scripts under the user's home directory. These files should be treated as temporary artifacts and reviewed before execution in sensitive environments.

## Development priorities

The next engineering priorities are to add schema-based tests, capture FreeCAD process results, validate geometry before export, separate runtime and development dependencies, and introduce a typed design model so geometry is produced from validated parameters rather than loosely parsed model output.

## License

MIT License. See [LICENSE](LICENSE).

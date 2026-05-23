# Contributing to Prosthetic CAD AI

Thank you for your interest in contributing to this innovative healthcare AI project! We're excited to work with you.

## 📋 Code of Conduct

- Be respectful and inclusive
- Appreciate diverse perspectives
- Focus on constructive feedback
- Remember: we're building tools to help people

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- FreeCAD knowledge (helpful)
- Understanding of CAD design basics
- Git proficiency

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/prosthectic-cad-ai.git
cd prosthectic-cad-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Ollama and pull model
ollama pull mistral

# Verify setup
python scripts/setup_check.py
```

## 🐛 Bug Reports

Report bugs with:

- **Title:** Clear, specific description
- **Description:** What went wrong?
- **Steps to Reproduce:** Exact steps to trigger
- **Expected vs Actual:** What should happen vs what happened
- **Environment:** Python version, OS, FreeCAD version
- **Logs/Screenshots:** Attach relevant information

**Example:**
```
Title: FreeCAD export fails with special characters in design name

Description:
When generating a prosthetic with special characters in the description,
the STEP export fails with an encoding error.

Steps:
1. Create design with description: "Right hand prosthetic (high-tech)"
2. Generate design
3. STEP export fails with UnicodeEncodeError

Environment: Python 3.10, Linux Ubuntu 22.04, FreeCAD 0.21.2
Error Log: [attach log file]
```

## ✨ Feature Requests

Suggest features with:

- **Title:** Feature name
- **Motivation:** Why is this needed?
- **Implementation:** How should it work?
- **Benefits:** Who benefits and how?
- **Alternatives:** Other approaches?

**Example:**
```
Title: Support for modular prosthetic components

Motivation:
Many prosthetists need to create modular designs where components
can be swapped based on patient needs.

Implementation:
Add module library system where individual components (joints, sockets, feet)
can be combined using natural language: "Create modular hand with three
joint types and quick-connect interface"

Benefits:
- Faster design for practitioners
- Better patient customization
- Reduced waste (reusable components)
```

## 🛠️ Development Workflow

### 1. Branch Naming

```bash
git checkout -b feature/description       # New feature
git checkout -b fix/bug-description       # Bug fix
git checkout -b docs/topic               # Documentation
git checkout -b test/feature-name        # Tests
git checkout -b refactor/component       # Code improvements
```

### 2. Code Style

Follow PEP 8 + these project standards:

```python
# Functions: descriptive names, type hints, docstrings
def extract_prosthetic_parameters(
    description: str,
    llm_model: str = "mistral"
) -> dict:
    """
    Extract prosthetic design parameters from natural language description.
    
    Args:
        description: Natural language prosthetic specification
        llm_model: LLM model to use for extraction. Default: mistral
        
    Returns:
        Dictionary with extracted parameters:
        {
            'type': 'hand' | 'foot' | etc,
            'side': 'right' | 'left',
            'material': str,
            'constraints': dict
        }
        
    Raises:
        ValueError: If description is empty
        LLMError: If LLM processing fails
        
    Examples:
        >>> desc = "Left carbon fiber hand prosthetic"
        >>> params = extract_prosthetic_parameters(desc)
        >>> params['side']
        'left'
    """
    # Implementation
```

### 3. Testing

**Every feature needs tests:**

```python
# tests/test_parameter_extractor.py
import pytest
from src.parameter_extractor import extract_prosthetic_parameters

class TestParameterExtraction:
    """Test parameter extraction from natural language."""
    
    def test_extract_hand_prosthetic(self):
        """Test extraction of hand prosthetic specification."""
        desc = "Right hand prosthetic with carbon fiber"
        result = extract_prosthetic_parameters(desc)
        
        assert result['type'] == 'hand'
        assert result['side'] == 'right'
        assert 'carbon_fiber' in result['material'].lower()
    
    def test_extract_leg_prosthetic(self):
        """Test extraction of leg prosthetic specification."""
        desc = "Left transtibial prosthetic, sports grade"
        result = extract_prosthetic_parameters(desc)
        
        assert result['type'] == 'leg'
        assert result['side'] == 'left'
        assert result['grade'] == 'sports'
    
    def test_empty_description_raises_error(self):
        """Test that empty description raises ValueError."""
        with pytest.raises(ValueError):
            extract_prosthetic_parameters("")
    
    def test_ambiguous_description_handled(self):
        """Test handling of ambiguous descriptions."""
        desc = "prosthetic with metal"
        result = extract_prosthetic_parameters(desc)
        
        assert result is not None
        assert 'confidence' in result
```

Run tests:
```bash
pytest tests/ -v
pytest tests/test_parameter_extractor.py -v
pytest --cov=src tests/
```

### 4. Commits

Write clear, descriptive commits:

```bash
git commit -m "feat: Add support for modular prosthetic components"
git commit -m "fix: Resolve FreeCAD export encoding issues"
git commit -m "docs: Update API reference with new endpoints"
git commit -m "test: Add tests for material library expansion"
git commit -m "perf: Optimize LLM prompt processing"
```

**Format:** `type: brief description`

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `ci:` - CI/CD changes

### 5. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Create PR with:

- **Title:** Clear, descriptive
- **Description:** What, why, how
- **Related Issues:** Links to related issues
- **Checklist:** Completion status

**PR Template:**
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Breaking change

## Related Issues
Fixes #123

## Changes
- Item 1
- Item 2
- Item 3

## Testing
- [ ] Tests added
- [ ] All tests passing
- [ ] Manual testing completed
- [ ] No regressions detected

## Documentation
- [ ] README updated
- [ ] Docstrings added
- [ ] API docs updated
- [ ] CHANGELOG updated

## Screenshots (if applicable)
[Add any screenshots]
```

## 📝 Documentation Guidelines

### Docstrings (Google Style)

```python
def generate_cad_model(
    parameters: dict,
    template: str = "default"
) -> str:
    """
    Generate 3D CAD model from prosthetic parameters.
    
    Converts parameter dictionary into FreeCAD model and exports
    as STEP file for manufacturing.
    
    Args:
        parameters: Prosthetic design parameters dict with:
            - 'type': Prosthetic type ('hand', 'foot', etc)
            - 'side': 'left' or 'right'
            - 'material': Material specification
            - 'dimensions': Dict with measurements in mm
        template: Template to use. Default: 'default'
            Options: 'default', 'sports', 'activity'
    
    Returns:
        Path to generated STEP file (str)
        
    Raises:
        ValueError: If parameters invalid or incomplete
        FreeCADError: If CAD generation fails
        
    Examples:
        >>> params = {
        ...     'type': 'hand',
        ...     'side': 'right',
        ...     'material': 'carbon_fiber',
        ...     'dimensions': {'length': 200, 'width': 80}
        ... }
        >>> filepath = generate_cad_model(params)
        >>> print(filepath)
        '/output/prosthetic_hand_right_20260523.step'
    """
```

### README Sections

- Keep clear and concise
- Use examples liberally
- Link to detailed documentation
- Update for new features

### Comments

```python
# Good: Explains WHY
# Use local LLM to avoid sending patient data to cloud
response = ollama_client.generate(prompt)

# Avoid: States the obvious
# Get response from ollama
response = ollama_client.generate(prompt)
```

## 🎯 Areas Seeking Contributions

**High Priority:**
- [ ] Web user interface
- [ ] Additional prosthetic types
- [ ] Performance optimization
- [ ] Docker containerization

**Medium Priority:**
- [ ] Material database expansion
- [ ] Mobile app prototype
- [ ] Advanced customization
- [ ] Unit test coverage increase

**Documentation:**
- [ ] Tutorial videos
- [ ] Beginner's guide
- [ ] Clinical use cases
- [ ] Deployment guides

## ✅ Review Process

1. **Code Review:**
   - Functionality correctness
   - Code quality and style
   - Test coverage
   - Documentation completeness

2. **Feedback:**
   - Constructive suggestions
   - Request for revisions if needed

3. **Revisions:**
   - Address feedback
   - Push updates to same branch

4. **Approval:**
   - Once approved, maintainer merges

5. **Closure:**
   - Feature branch deleted
   - Merged to main

## 🔒 Security Guidelines

- No hardcoded API keys
- Don't commit secrets
- Validate all inputs
- Consider data privacy (patient data handling)
- Document security implications

## 🚀 Performance Considerations

- Profile code before optimizing
- Document performance impacts
- Test with realistic datasets
- Consider resource constraints

## 📚 Useful Resources

- [FreeCAD Python API](https://wiki.freecad.org/Python_scripting_tutorial)
- [Ollama Documentation](https://ollama.ai/docs)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## ❓ Need Help?

- Open a GitHub Discussion
- Check existing issues
- Ask in the PR comments
- Contact maintainers

---

**Thank you for contributing! Together we're making prosthetic design more accessible and efficient! 🦾❤️**

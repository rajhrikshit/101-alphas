# Contributing to 101 Alphas Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Provide detailed descriptions and reproduction steps
- Include system information and error messages

### Adding New Alphas

To implement additional alphas (61-101):

1. Add the formula to `alphas/formulas.py`
2. Update the metadata in `alphas/metadata.py`
3. Add tests in `tests/test_alphas.py`
4. Update documentation in `docs/alpha_descriptions.md`

Example:

```python
def alpha_061(data):
    """
    Alpha#61: Your formula description here
    """
    close = data['close']
    # Your implementation
    return result
```

### Improving Operators

If you find bugs in operators or want to add new ones:

1. Modify `alphas/operators.py`
2. Add comprehensive tests
3. Update API documentation

### Enhancing the Dashboard

For dashboard improvements:

1. Modify `dashboard/app.py` or create new components in `dashboard/components/`
2. Test thoroughly with sample data
3. Ensure responsive design and good UX

## Development Setup

```bash
# Clone repository
git clone https://github.com/rajhrikshit/101-alphas.git
cd 101-alphas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run tests
python -m unittest tests.test_alphas
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.test_alphas.TestOperators
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add/update tests
5. Update documentation
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code Review

- Be respectful and constructive
- Respond to feedback promptly
- Make requested changes or explain why not

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

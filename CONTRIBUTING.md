# Contributing to JAM WiFi Speaker Control

Thank you for your interest in contributing! This project aims to provide an open-source alternative to the discontinued JAM WiFi app.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your speaker model and firmware version
- Python version and operating system

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- The feature and why it would be useful
- Any examples of how it might work
- Whether you're willing to help implement it

### Contributing Code

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Keep functions focused and simple

4. **Test your changes**
   - Test with actual hardware if possible
   - Verify no passwords or personal data in code
   - Check that examples use generic data

5. **Commit with clear messages**
   ```bash
   git commit -m "Add support for XYZ feature"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/my-new-feature
   ```

## Code Guidelines

### Python Style
- Use Python 3.6+ compatible code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings for functions

### Security
- **Never commit passwords, API keys, or personal data**
- Use generic examples in documentation (e.g., "MyWiFi", "MyPassword123")
- Replace specific IPs with examples (e.g., "192.168.1.100")
- Check `.gitignore` covers sensitive files

### Documentation
- Update README.md if adding features
- Add comments for non-obvious code
- Include usage examples
- Update SETUP_GUIDE.md if changing setup process

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/jam-wifi-control.git
cd jam-wifi-control

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# No dependencies to install (uses standard library only!)

# Make changes and test
python3 your_script.py
```

## Testing

### With Hardware
- Test with actual JAM WiFi speakers
- Verify pairing mode setup works
- Test network discovery
- Confirm playback controls work

### Without Hardware
- Verify code runs without errors
- Check documentation is clear
- Ensure no hardcoded credentials
- Validate examples work conceptually

## Areas Needing Help

- **Device Support**: Testing with different JAM models
- **Platform Support**: Windows testing and compatibility
- **Features**: Web interface, streaming integrations
- **Documentation**: Translations, video tutorials
- **Testing**: Automated tests, CI/CD

## Questions?

- Open a GitHub Discussion for questions
- Check existing issues and PRs first
- Be patient - this is a community project!

## Code of Conduct

- Be respectful and inclusive
- Help others learn
- Focus on what's best for the project
- Accept constructive criticism gracefully

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

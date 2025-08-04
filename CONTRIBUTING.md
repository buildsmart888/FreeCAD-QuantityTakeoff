# Contributing to FreeCAD Quantity Takeoff Module

Thank you for your interest in contributing to the FreeCAD Quantity Takeoff Module! 🎉

## 🤝 How to Contribute

### 1. **Reporting Bugs**
- Use the [GitHub Issues](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/issues) page
- Search existing issues first to avoid duplicates
- Provide detailed information:
  - Operating System and version
  - FreeCAD version
  - Python version
  - Steps to reproduce the bug
  - Expected vs actual behavior
  - Screenshots if applicable

### 2. **Suggesting Features**
- Open a [Feature Request](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/issues/new?template=feature_request.md)
- Describe the feature clearly
- Explain why it would be useful
- Consider implementation details if possible

### 3. **Code Contributions**

#### **Setup Development Environment**
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/FreeCAD-QuantityTakeoff.git
cd FreeCAD-QuantityTakeoff

# Create a development branch
git checkout -b feature/your-feature-name
```

#### **Development Guidelines**
- Follow [PEP 8](https://pep8.org/) Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include error handling where appropriate
- Test your changes thoroughly

#### **File Structure**
```
QuantityTakeoff/
├── dialogs/          # All dialog-related code
├── utils/            # Utility functions and classes
├── resources/        # Icons and assets
├── tests/           # Unit tests (future)
└── README.md        # Documentation
```

#### **Coding Standards**
```python
# Good example
def calculate_material_total(quantity, material_per_unit):
    """
    Calculate total material cost.
    
    Args:
        quantity (float): Number of items
        material_per_unit (float): Cost per unit
        
    Returns:
        float: Total material cost
    """
    try:
        return float(quantity) * float(material_per_unit)
    except (ValueError, TypeError):
        return 0.0
```

### 4. **Pull Request Process**
1. **Update** your branch with latest main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Test** your changes:
   - Test in FreeCAD environment
   - Verify no import errors
   - Test UI functionality
   - Check calculation accuracy

3. **Commit** with clear messages:
   ```bash
   git commit -m "feat: add material cost calculator
   
   - Implement QTOCalculator.calculate_material_total()
   - Add error handling for invalid inputs
   - Update documentation"
   ```

4. **Push** and create Pull Request:
   ```bash
   git push origin your-feature-branch
   ```

5. **Pull Request Guidelines**:
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - Keep changes focused and atomic

## 🧪 Testing

### **Manual Testing Checklist**
- [ ] Module loads without errors
- [ ] All three buttons work in workbench
- [ ] BOQ dialog opens and calculates correctly
- [ ] Object info dialog displays data properly
- [ ] CSV export functionality works
- [ ] Real-time calculations update properly
- [ ] No console errors or warnings

### **Future: Automated Testing**
We plan to add:
- Unit tests for calculations
- Integration tests for dialogs
- CI/CD pipeline

## 📝 Documentation

### **Code Documentation**
- Add docstrings to all public functions
- Include type hints where possible
- Comment complex algorithms
- Update README.md for new features

### **User Documentation**
- Update README.md for user-facing changes
- Add screenshots for UI changes
- Update CHANGELOG.md

## 🎯 Priority Areas for Contribution

### **High Priority**
- 🐛 Bug fixes and stability improvements
- 📊 Enhanced calculation algorithms
- 🎨 UI/UX improvements
- 📱 Better error messages

### **Medium Priority**
- 🌐 Internationalization (more languages)
- 📈 Additional export formats (Excel, PDF)
- 🔧 Advanced filtering options
- ⚡ Performance optimizations

### **Future Features**
- 🧮 Cost database integration
- 📋 Report templates
- 🔄 Integration with other CAD software
- 📊 Advanced analytics

## 🏷️ Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

Examples:
```
feat: add material cost calculator
fix: resolve PySide2 import errors
docs: update installation instructions
refactor: separate dialog classes into modules
```

## 🚀 Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Create GitHub release
6. Update documentation

## 📞 Getting Help

- 💬 [GitHub Discussions](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/discussions)
- 📖 [Wiki](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/wiki)
- 🐛 [Issues](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/issues)

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Added to GitHub contributors list

Thank you for making this project better! 🎉

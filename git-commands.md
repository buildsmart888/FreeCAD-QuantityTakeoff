# Git Commands for GitHub Repository Setup

## Step 1: Initialize Git Repository
```bash
git init
```

## Step 2: Add all files
```bash
git add .
```

## Step 3: Create initial commit
```bash
git commit -m "feat: initial release of FreeCAD Quantity Takeoff module

- Add complete BOQ management system with 15-column table
- Add object information dialog with filtering capabilities  
- Add modular design with separated dialogs and utilities
- Add real-time calculation system for costs
- Add CSV export functionality
- Add PySide2/PyQt5 compatibility
- Add comprehensive documentation and GitHub setup"
```

## Step 4: Add remote repository
```bash
git remote add origin https://github.com/buildsmart888/FreeCAD-QuantityTakeoff.git
```

## Step 5: Create and push main branch
```bash
git branch -M main
git push -u origin main
```

## Optional: Create development branch
```bash
git checkout -b develop
git push -u origin develop
```

## Future workflow:
```bash
# For new features
git checkout -b feature/new-feature-name
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature-name
# Create pull request on GitHub

# For bug fixes
git checkout -b fix/bug-description
# ... make changes ...
git add .
git commit -m "fix: resolve bug description"
git push origin fix/bug-description
# Create pull request on GitHub
```

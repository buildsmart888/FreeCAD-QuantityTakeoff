# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [1.0.0] - 2025-08-04

### Added
- **Initial release** of Quantity Takeoff FreeCAD Module
- **Main BOQ Dialog** with 15-column table for construction quantity takeoff
- **Object Information Dialog** with filtering and search capabilities
- **Modular design** with separated dialogs and utilities
- **Real-time calculation** system for Material Total and Labor Total
- **Unit conversion** from mm to meters automatically
- **Editable pricing** columns (Material/unit, Labor/unit)
- **CSV export** functionality for both dialogs
- **Color-coded object types** in information dialog
- **Sorting capability** for all table columns
- **Error handling** and signal management
- **PySide2/PyQt5 compatibility**
- **Unicode support** for Thai language
- **Professional workbench** integration with 3 main commands:
  - Open BOQ Dialog
  - Show Object Information
  - Select Objects from 3D view

### Technical Features
- **QTOCalculator class** for all calculations
- **Absolute import system** to avoid Python import errors
- **Signal disconnect/reconnect** to prevent infinite loops
- **Fallback systems** for import failures
- **Professional table formatting** with currency and dimension formatting
- **Grand total calculation** with real-time updates

### Supported Platforms
- ✅ Windows (tested on Windows 10/11)
- ✅ Linux (Ubuntu, Fedora, openSUSE)
- ✅ macOS (10.14+)

### Requirements
- FreeCAD 0.20+ (recommended 1.0+)
- Python 3.8+
- PySide2 or PyQt5
- Standard Python libraries: csv, os, sys

[Unreleased]: https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/releases/tag/v1.0.0

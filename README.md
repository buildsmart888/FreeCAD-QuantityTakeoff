# Quantity Takeoff FreeCAD Module

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FreeCAD](https://img.shields.io/badge/FreeCAD-1.0+-blue.svg)](https://www.freecad.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

## 📖 **Overview**

A professional **Quantity Takeoff** module for FreeCAD that helps construction professionals calculate material quantities, costs, and generate Bill of Quantities (BOQ) directly from 3D models.

Perfect for:
- 🏗️ **Construction Engineers**
- 📐 **Architects** 
- 💰 **Cost Estimators**
- 📊 **Project Managers**

## 🚀 **Installation**

### **Method 1: Download ZIP**
1. Download the latest release from [Releases](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/releases)
2. Extract to FreeCAD's Mod directory:
   ```
   Windows: C:\Users\[username]\AppData\Roaming\FreeCAD\Mod\QuantityTakeoff\
   Linux: ~/.local/share/FreeCAD/Mod/QuantityTakeoff/
   macOS: ~/Library/Application Support/FreeCAD/Mod/QuantityTakeoff/
   ```
3. Restart FreeCAD
4. Select "Quantity Takeoff" workbench

### **Method 2: Git Clone**
```bash
# Navigate to FreeCAD Mod directory
cd ~/.local/share/FreeCAD/Mod/  # Linux
# cd ~/Library/Application Support/FreeCAD/Mod/  # macOS
# cd C:\Users\[username]\AppData\Roaming\FreeCAD\Mod\  # Windows

# Clone repository
git clone https://github.com/buildsmart888/FreeCAD-QuantityTakeoff.git QuantityTakeoff
```

## 📷 **Screenshots**

### Main BOQ Dialog
![BOQ Dialog](screenshots/boq-dialog.png)

### Object Information Dialog
![Object Info Dialog](screenshots/object-info-dialog.png)

## 🏗️ **โครงสร้างโปรแกรมแบบ Modular Design**

```
QuantityTakeoff/
├── Init.py                     # เริ่มต้น module
├── InitGui.py                  # เริ่มต้น GUI
├── QTOWorkbench.py            # หลัก Workbench ที่มี 3 ปุ่ม
├── qto_dialog.py              # Compatibility layer
├── dialogs/                   # โฟลเดอร์ Dialog ทั้งหมด
│   ├── __init__.py           
│   ├── main_dialog.py         # Dialog หลัก BOQ Management
│   └── object_info_dialog.py  # Dialog แสดงข้อมูลชิ้นงาน + กรอง
├── utils/                     # โฟลเดอร์ Utilities
│   ├── __init__.py
│   └── calculations.py        # คลาส QTOCalculator
└── resources/
    └── icons/
        └── qto.svg

```

## 🎯 **ฟีเจอร์หลัก**

### **1. Dialog หลัก BOQ (main_dialog.py)**
- ✅ ตาราง BOQ 15 คอลัมน์ สำหรับงานก่อสร้าง
- ✅ แก้ไขราคา Material/unit, Labor/unit ได้
- ✅ คำนวณแบบ Real-time: Material Total = QTY × Material/unit
- ✅ คำนวณแบบ Real-time: Labor Total = QTY × Labor/unit  
- ✅ Grand Total รวมทั้งหมด
- ✅ Export CSV ได้
- ✅ หน่วยเป็นเมตร (แปลงจาก mm อัตโนมัติ)

### **2. Dialog ข้อมูลชิ้นงาน (object_info_dialog.py)**
- ✅ แสดงข้อมูลชิ้นงานทั้งหมด 12 คอลัมน์
- ✅ ระบบกรองตาม Object Type
- ✅ ระบบค้นหาตามชื่อ  
- ✅ สีแยกประเภทชิ้นงาน
- ✅ Export ข้อมูลได้
- ✅ Sorting ได้ทุกคอลัมน์

### **3. ระบบคำนวณ (calculations.py)**
- ✅ QTOCalculator class
- ✅ แปลงหน่วยจาก mm เป็น m อัตโนมัติ
- ✅ คำนวณ Volume, Area, Weight
- ✅ Format ตัวเลขแบบมืออาชีพ

## 🔧 **วิธีใช้งาน**

### **ใน FreeCAD:**
1. เลือก Workbench "Quantity Takeoff"
2. จะมี **3 ปุ่ม**:
   - **"เปิด BOQ Dialog"** → เปิดตาราง BOQ หลัก
   - **"แสดงข้อมูลชิ้นงาน"** → เปิด Dialog ข้อมูลชิ้นงานพร้อมกรอง  
   - **"เลือกชิ้นงาน"** → เลือกใน 3D แล้วเพิ่มเข้าตาราง

### **การแก้ไขโค๊ด:**
- **แก้ไข BOQ Table** → `dialogs/main_dialog.py`
- **แก้ไข Object Info** → `dialogs/object_info_dialog.py`  
- **แก้ไขการคำนวณ** → `utils/calculations.py`
- **เพิ่มปุ่มใหม่** → `QTOWorkbench.py`

## 📊 **คอลัมน์ BOQ Table**

| คอลัมน์ | คำอธิบาย | แก้ไขได้ |
|---------|----------|----------|
| Object Name | ชื่อชิ้นงาน | ❌ |
| Object Type | ประเภทชิ้นงาน | ❌ |
| Material | วัสดุ | ❌ |
| Length (m) | ความยาว เมตร | ❌ |
| Width (m) | ความกว้าง เมตร | ❌ |
| Height (m) | ความสูง เมตร | ❌ |
| Volume (m³) | ปริมาตร | ❌ |
| Area (m²) | พื้นที่ | ❌ |
| Quantity | จำนวน | ❌ |
| Unit Weight (kg) | น้ำหนัก/หน่วย | ❌ |
| **Material/unit** | ราคาวัสดุ/หน่วย | ✅ **แก้ไขได้** |
| **Labor/unit** | ราคาแรงงาน/หน่วย | ✅ **แก้ไขได้** |
| Material Total | รวมวัสดุ | ❌ คำนวณอัตโนมัติ |
| Labor Total | รวมแรงงาน | ❌ คำนวณอัตโนมัติ |
| **Total** | **รวมทั้งหมด** | ❌ คำนวณอัตโนมัติ |

## 🔄 **การอัปเกรด**

สามารถอัปเกรดแต่ละส่วนแยกกันได้:

1. **อัปเกรด Dialog** → แก้ไขไฟล์ใน `dialogs/`
2. **อัปเกรด Calculator** → แก้ไข `utils/calculations.py`  
3. **เพิ่มปุ่ม** → แก้ไข `QTOWorkbench.py`
4. **Backward Compatible** → ไฟล์เก่ายังใช้ได้ผ่าน `qto_dialog.py`

## 📝 **ข้อมูลเพิ่มเติม**

- ✅ **Compatible** กับ PySide2 และ PyQt5
- ✅ **Error Handling** ครบถ้วน
- ✅ **Signal Management** ป้องกัน infinite loop
- ✅ **Unicode Support** ภาษาไทยใช้ได้
- ✅ **Modular Design** แก้ไขง่าย ขยายง่าย

## 🤝 **Contributing**

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Setup**
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/FreeCAD-QuantityTakeoff.git
cd FreeCAD-QuantityTakeoff

# Create development branch
git checkout -b develop
```

## 🐛 **Issue Reporting**

Found a bug? Please [create an issue](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/issues) with:
- 🖥️ **Operating System** (Windows/Linux/macOS)
- 🔧 **FreeCAD Version**
- 🐍 **Python Version**
- 📝 **Detailed Description**
- 📸 **Screenshots** (if applicable)

## 📞 **Support**

- 📖 **Documentation**: [Wiki](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/discussions)
- 🐛 **Bug Reports**: [Issues](https://github.com/buildsmart888/FreeCAD-QuantityTakeoff/issues)

## 📄 **License**

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- [FreeCAD](https://www.freecad.org/) - Amazing open-source CAD software
- [PySide2/PyQt5](https://doc.qt.io/qtforpython/) - GUI framework
- Community contributors and testers

## ⭐ **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=buildsmart888/FreeCAD-QuantityTakeoff&type=Date)](https://star-history.com/#buildsmart888/FreeCAD-QuantityTakeoff&Date)

---

**Made with ❤️ for the construction industry**

# -*- coding: utf-8 -*-
"""
qto_dialog_tkinter.py - Quantity Takeoff Dialog UI using tkinter
This file contains a tkinter version for testing without Qt dependencies
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class QuantityTakeoffDialog:
    """
    Main dialog for Quantity Takeoff functionality using tkinter
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบ Quantity Takeoff สำหรับงานก่อสร้าง")
        self.root.geometry("1200x700")
        
        self.setup_ui()
        self.load_sample_data()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(title_frame, text="ระบบ Quantity Takeoff", 
                              font=("Arial", 18, "bold"), fg="#2196F3")
        title_label.pack()
        
        # Toolbar
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(toolbar_frame, text="รีเฟรช", command=self.refresh_data, 
                 bg="#f0f0f0", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, text="คำนวณ", command=self.calculate_quantities, 
                 bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, text="เพิ่มรายการ", command=self.add_new_row, 
                 bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, text="ลบรายการ", command=self.delete_selected_row, 
                 bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, text="ส่งออก CSV", command=self.export_data, 
                 bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=2)
        
        # Main table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Table headers
        headers = [
            "หมวดงานหลัก", "รหัส", "รายการงานย่อย", "QTY", "UNIT",
            "Material/unit", "Material Total", "Labor/unit", "Labor Total", "Total", "หมายเหตุ"
        ]
        
        # Create treeview
        self.tree = ttk.Treeview(table_frame, columns=headers, show='headings', height=15)
        
        # Configure headers
        for i, header in enumerate(headers):
            self.tree.heading(f'#{i+1}', text=header)
            if i in [3, 5, 6, 7, 8, 9]:  # Numeric columns
                self.tree.column(f'#{i+1}', width=100, anchor='e')
            else:
                self.tree.column(f'#{i+1}', width=120, anchor='w')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("พร้อมใช้งาน")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_sample_data(self):
        """Load sample data into the table"""
        sample_data = [
            # หมวดงานโครงสร้าง
            ["งานโครงสร้าง", "1.2", "แบบหล่อคอนกรีต", "96.18", "ตร.ม.", "100.00", "9,618.00", "30.00", "2,885.40", "12,503.40", ""],
            ["", "", "คอนกรีต 240 ksc", "10.64", "ลบ.ม.", "1,800.00", "19,152.00", "300.00", "3,192.00", "22,344.00", ""],
            ["", "", "เหล็กเสริม (RB12)", "56.77", "กก.", "22.00", "1,249.00", "10.00", "567.70", "1,816.70", ""],
            ["", "", "Wiremesh 4 มม. @20 ซม.", "57.37", "ตร.ม.", "55.00", "3,155.35", "25.00", "1,434.25", "4,589.60", ""],
            ["Subtotal: โครงสร้าง", "", "", "", "", "", "33,174.35", "", "8,079.35", "41,253.70", "รวมงานโครงสร้าง"],
            
            # หมวดงานสถาปัตย์
            ["งานสถาปัตย์", "2.1", "ผนังอิฐมอญฉาบปูน", "372.38", "ตร.ม.", "280.00", "104,266.40", "90.00", "33,514.20", "137,780.60", ""],
            ["", "", "กระเบื้องบุผนังห้องน้ำ", "21.25", "ตร.ม.", "420.00", "8,925.00", "150.00", "3,187.50", "12,112.50", ""],
            ["Subtotal: สถาปัตย์", "", "", "", "", "", "113,191.40", "", "36,701.70", "149,893.10", "รวมงานสถาปัตย์"],
            
            # งานระบบไฟฟ้า
            ["งานระบบไฟฟ้า", "3.1", "สายไฟ THW 2.5 ตร.มม.", "450.00", "ม.", "15.00", "6,750.00", "8.00", "3,600.00", "10,350.00", ""],
            ["", "", "หลอดไฟ LED 12W", "24.00", "ดวง", "250.00", "6,000.00", "50.00", "1,200.00", "7,200.00", ""],
            ["Subtotal: ไฟฟ้า", "", "", "", "", "", "12,750.00", "", "4,800.00", "17,550.00", "รวมงานไฟฟ้า"],
            
            # รวมทั้งหมด
            ["GRAND TOTAL", "", "", "", "", "", "159,115.75", "", "49,581.05", "208,696.80", "รวมทั้งโครงการ"]
        ]
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert sample data
        for i, row_data in enumerate(sample_data):
            item_id = self.tree.insert('', 'end', values=row_data)
            
            # Style subtotal and grand total rows
            if "Subtotal:" in row_data[0] or "GRAND TOTAL" in row_data[0]:
                self.tree.set(item_id, 0, row_data[0])
                # Note: tkinter treeview styling is limited, but we can at least organize the data
        
        self.status_var.set("โหลดข้อมูลตัวอย่างเสร็จสิ้น")
        
    def refresh_data(self):
        """Refresh data"""
        self.load_sample_data()
        self.status_var.set("รีเฟรชข้อมูลแล้ว")
        
    def calculate_quantities(self):
        """Calculate quantities and totals"""
        self.status_var.set("กำลังคำนวณ...")
        
        try:
            total_material = 0
            total_labor = 0
            total_grand = 0
            
            for item_id in self.tree.get_children():
                values = self.tree.item(item_id)['values']
                
                # Skip subtotal and grand total rows
                if len(values) > 0 and ("Subtotal:" in str(values[0]) or "GRAND TOTAL" in str(values[0])):
                    continue
                
                try:
                    qty = float(str(values[3]).replace(',', '')) if len(values) > 3 and values[3] else 0
                    material_unit = float(str(values[5]).replace(',', '')) if len(values) > 5 and values[5] else 0
                    labor_unit = float(str(values[7]).replace(',', '')) if len(values) > 7 and values[7] else 0
                    
                    # Calculate totals
                    material_total = qty * material_unit
                    labor_total = qty * labor_unit
                    total = material_total + labor_total
                    
                    # Update the row
                    new_values = list(values)
                    if len(new_values) > 6:
                        new_values[6] = f"{material_total:,.2f}"
                    if len(new_values) > 8:
                        new_values[8] = f"{labor_total:,.2f}"
                    if len(new_values) > 9:
                        new_values[9] = f"{total:,.2f}"
                    
                    self.tree.item(item_id, values=new_values)
                    
                    # Add to grand totals
                    total_material += material_total
                    total_labor += labor_total
                    total_grand += total
                    
                except (ValueError, IndexError):
                    continue
            
            self.status_var.set(f"คำนวณเสร็จสิ้น - รวมทั้งหมด: {total_grand:,.2f} บาท")
            
        except Exception as e:
            self.status_var.set(f"เกิดข้อผิดพลาด: {str(e)}")
    
    def add_new_row(self):
        """Add new row"""
        new_data = ["", "", "รายการใหม่", "0", "หน่วย", "0", "0", "0", "0", "0", ""]
        self.tree.insert('', 'end', values=new_data)
        self.status_var.set("เพิ่มแถวใหม่แล้ว")
    
    def delete_selected_row(self):
        """Delete selected row"""
        selected = self.tree.selection()
        if selected:
            # Check if it's a subtotal or grand total
            values = self.tree.item(selected[0])['values']
            if len(values) > 0 and ("Subtotal:" in str(values[0]) or "GRAND TOTAL" in str(values[0])):
                messagebox.showwarning("คำเตือน", "ไม่สามารถลบแถวรวมได้")
                return
            
            if messagebox.askyesno("ยืนยันการลบ", "คุณต้องการลบแถวที่เลือกหรือไม่?"):
                self.tree.delete(selected[0])
                self.status_var.set("ลบแถวแล้ว")
        else:
            messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกแถวที่ต้องการลบ")
    
    def export_data(self):
        """Export data to CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="บันทึกไฟล์ CSV"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    headers = [
                        "หมวดงานหลัก", "รหัส", "รายการงานย่อย", "QTY", "UNIT",
                        "Material/unit", "Material Total", "Labor/unit", "Labor Total", "Total", "หมายเหตุ"
                    ]
                    writer.writerow(headers)
                    
                    # Write data
                    for item_id in self.tree.get_children():
                        values = self.tree.item(item_id)['values']
                        writer.writerow(values)
                
                self.status_var.set(f"ส่งออกข้อมูลเรียบร้อย: {file_path}")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการส่งออก: {str(e)}")

def main():
    root = tk.Tk()
    app = QuantityTakeoffDialog(root)
    root.mainloop()

if __name__ == "__main__":
    main()

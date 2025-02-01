import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image
import threading

class PDFCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 壓縮工具")
        self.root.geometry("600x700")
        
        # 主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 檔案選擇區域
        file_frame = ttk.LabelFrame(main_frame, text="PDF檔案選擇", padding="5")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 檔案列表
        self.file_listbox = tk.Listbox(file_frame, height=10)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 檔案操作按鈕
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="添加檔案", command=self.add_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清除所有", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="移除選中", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        
        # 設定區域
        settings_frame = ttk.LabelFrame(main_frame, text="設定", padding="5")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 輸出資料夾
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(output_frame, text="輸出資料夾:").pack(side=tk.LEFT)
        self.output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="瀏覽", command=self.browse_output).pack(side=tk.LEFT)
        
        # DPI 設定
        dpi_frame = ttk.Frame(settings_frame)
        dpi_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(dpi_frame, text="DPI 設定:").pack(side=tk.LEFT)
        self.dpi = tk.IntVar(value=150)  # 預設 DPI
        dpi_scale = ttk.Scale(dpi_frame, from_=72, to=300, variable=self.dpi, orient=tk.HORIZONTAL)
        dpi_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.dpi_label = ttk.Label(dpi_frame, text="150")
        self.dpi_label.pack(side=tk.LEFT, padx=5)
        dpi_scale.configure(command=self.update_dpi_label)
        
        # 目標檔案大小
        self.target_size = 4 * 1024  # 4MB in KB
        
        # 自動模式選項
        self.auto_mode = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="自動調整DPI以達到目標大小", variable=self.auto_mode).pack(side=tk.LEFT, padx=5)
        
        # 進度顯示區域
        progress_frame = ttk.LabelFrame(main_frame, text="處理進度", padding="5")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 進度條
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # 狀態顯示
        self.status_text = tk.Text(progress_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 開始按鈕
        self.start_button = ttk.Button(main_frame, text="開始轉換", command=self.start_conversion)
        self.start_button.pack(pady=10)
        
        # 儲存檔案路徑
        self.pdf_files = []

    def update_dpi_label(self, value):
        self.dpi_label.configure(text=str(int(float(value))))

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="選擇PDF檔案",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.pdf_files.clear()
    
    def remove_selected(self):
        selection = self.file_listbox.curselection()
        for index in reversed(selection):
            self.file_listbox.delete(index)
            self.pdf_files.pop(index)
    
    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
    
    def convert_pdf_to_jpg(self, input_path, dpi):
        images = convert_from_path(input_path, dpi=dpi)
        jpg_files = []
        
        for i, image in enumerate(images):
            jpg_path = f"temp_page_{i}.jpg"
            image = image.convert("RGB")
            image.save(jpg_path, 'JPEG')  # 不調整品質
            jpg_files.append(jpg_path)
        
        return jpg_files

    def create_pdf_from_jpg(self, jpg_files, output_path):
        images = [Image.open(jpg_file) for jpg_file in jpg_files]
        images[0].save(output_path, save_all=True, append_images=images[1:])
        
        for jpg_file in jpg_files:
            os.remove(jpg_file)

    def process_files(self):
        output_folder = self.output_path.get()
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        total_files = len(self.pdf_files)
        if total_files == 0:
            self.update_status("請選擇要轉換的PDF檔案！")
            return
        
        self.update_status(f"開始處理 {total_files} 個檔案")
        
        for input_path in self.pdf_files:
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_folder, f"converted_{filename.replace('.pdf', '.pdf')}")
            
            if self.auto_mode.get():
                current_dpi = self.dpi.get()
                while True:
                    jpg_files = self.convert_pdf_to_jpg(input_path, current_dpi)
                    self.create_pdf_from_jpg(jpg_files, output_path)
                    
                    # 檢查輸出檔案大小
                    output_size = os.path.getsize(output_path) / 1024  # 轉換為 KB
                    if output_size <= self.target_size:
                        self.update_status(f"檔案 {filename} 轉換完成，大小: {output_size:.2f} KB")
                        break
                    else:
                        # 計算與目標大小的差距
                        size_difference = output_size - self.target_size
                        # 根據差距調整 DPI
                        adjustment_factor = max(1, int(size_difference / 100))  # 每 100KB 調整一次
                        current_dpi -= adjustment_factor
                        if current_dpi < 72:  # 最小 DPI 限制
                            self.update_status(f"無法達到目標大小，最小DPI為72，檔案大小: {output_size:.2f} KB")
                            break
            else:
                self.update_status(f"\n處理檔案: {filename}")
                jpg_files = self.convert_pdf_to_jpg(input_path, self.dpi.get())
                self.create_pdf_from_jpg(jpg_files, output_path)
                self.update_status(f"檔案 {filename} 轉換完成")
        
        self.update_status("\n所有檔案處理完成！")
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("完成", "PDF轉換完成！")
    
    def start_conversion(self):
        if not self.pdf_files:
            messagebox.showerror("錯誤", "請選擇要轉換的PDF檔案！")
            return
        
        if not self.output_path.get():
            messagebox.showerror("錯誤", "請選擇輸出資料夾！")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.status_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        threading.Thread(target=self.process_files, daemon=True).start()

def main():
    root = tk.Tk()
    app = PDFCompressorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
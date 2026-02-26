import tkinter as tk
from tkinter import filedialog, messagebox
import os

from main import run


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Сравнение прайсов")
        self.root.geometry("650x500")
        self.root.resizable(True, True)

        self.reference_path = None
        self.supplier_paths = []
        self.output_path = None

        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # --- ЭТАЛОН ---
        ref_frame = tk.LabelFrame(main_frame, text="Эталонный файл", padx=10, pady=10)
        ref_frame.pack(fill="x", pady=5)

        self.reference_label = tk.Label(ref_frame, text="Не выбран", fg="gray")
        self.reference_label.pack(anchor="w")

        tk.Button(ref_frame, text="Выбрать эталон", command=self.choose_reference).pack(
            anchor="w", pady=5
        )

        # --- ПОСТАВЩИКИ ---
        sup_frame = tk.LabelFrame(
            main_frame, text="Файлы поставщиков", padx=10, pady=10
        )
        sup_frame.pack(fill="both", expand=True, pady=5)

        self.suppliers_listbox = tk.Listbox(sup_frame, height=6)
        self.suppliers_listbox.pack(fill="both", expand=True)

        btn_frame = tk.Frame(sup_frame)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame, text="Выбрать поставщиков", command=self.choose_suppliers
        ).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Очистить список", command=self.clear_suppliers).pack(
            side="left", padx=5
        )

        # --- СОХРАНЕНИЕ ---
        save_frame = tk.LabelFrame(
            main_frame, text="Сохранение результата", padx=10, pady=10
        )
        save_frame.pack(fill="x", pady=5)

        self.output_label = tk.Label(save_frame, text="Не выбран", fg="gray")
        self.output_label.pack(anchor="w")

        tk.Button(
            save_frame, text="Выбрать место сохранения", command=self.choose_output
        ).pack(anchor="w", pady=5)

        # --- КНОПКА ЗАПУСКА ---
        self.generate_button = tk.Button(
            main_frame,
            text="Сформировать файл",
            bg="#4CAF50",
            fg="white",
            height=2,
            command=self.generate
        )
        self.generate_button.pack(fill="x", pady=15)

    def choose_reference(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.reference_path = path
            self.reference_label.config(text=os.path.basename(path), fg="black")

    def choose_suppliers(self):
        paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
        if paths:
            self.supplier_paths = list(paths)
            self.suppliers_listbox.delete(0, tk.END)
            for path in paths:
                self.suppliers_listbox.insert(tk.END, os.path.basename(path))

    def choose_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
        )
        if path:
            self.output_path = path
            self.output_label.config(text=os.path.basename(path), fg="black")

    def clear_suppliers(self):
        self.supplier_paths = []
        self.suppliers_listbox.delete(0, tk.END)

    def generate(self):
        if not self.reference_path:
            messagebox.showwarning("Ошибка", "Выберите эталонный файл")
            return

        if not self.supplier_paths:
            messagebox.showwarning("Ошибка", "Выберите файлы поставщиков")
            return

        if len(self.supplier_paths) < 2:
            messagebox.showwarning(
                "Ошибка",
                "Необходимо выбрать минимум 2 файла поставщиков"
            )
            return

        if not self.output_path:
            messagebox.showwarning("Ошибка", "Выберите место сохранения")
            return

        self.generate_button.config(state="disabled", text="Обработка...")
        self.root.update_idletasks()

        try:
            run(self.reference_path, self.supplier_paths, self.output_path)

            # возвращаем кнопку ДО показа сообщения
            self.generate_button.config(state="normal", text="Сформировать файл")

            messagebox.showinfo("Готово", "Файл успешно создан!")

        except Exception as e:
            self.generate_button.config(state="normal", text="Сформировать файл")
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

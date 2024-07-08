import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_path.set(directory)

def replace_filenames():
    directory = directory_path.get()
    if not directory:
        messagebox.showerror("Error", "ディレクトリを選択してください。")
        return
    
    old_text = old_text_var.get()
    new_text = new_text_var.get()
    if not old_text:
        messagebox.showerror("Error", "置換前の文字列を入力してください。")
        return
    if not new_text:
        messagebox.showerror("Error", "置換後の文字列を入力してください。")
        return

    success_count = 0
    fail_count = 0
    errors = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if old_text in filename:
                new_filename = filename.replace(old_text, new_text)
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    errors.append(f"Error renaming {old_path} to {new_path}: {e}")
    
    message = f"ファイル名の置換が完了しました。\n成功: {success_count} 件\n失敗: {fail_count} 件"
    if errors:
        message += "\n\nエラー詳細:\n" + "\n".join(errors)
    
    messagebox.showinfo("結果", message)

# GUIの設定
root = tk.Tk()
root.title("FileNameReplacer")

directory_path = tk.StringVar()
old_text_var = tk.StringVar()
new_text_var = tk.StringVar()

tk.Label(root, text="ディレクトリ:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=directory_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="選択", command=select_directory).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="置換前の文字列:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=old_text_var, width=50).grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="置換後の文字列:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=new_text_var, width=50).grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="置換開始", command=replace_filenames).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

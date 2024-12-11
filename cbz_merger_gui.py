import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Function to merge CBZ files into volumes
def merge_cbz_to_volumes(input_dir, output_dir, chapters_per_volume=20):
    chapter_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".cbz")])
    volume_counter = 1
    chapter_counter = 0

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merged_cbz = zipfile.ZipFile(os.path.join(output_dir, f"Volume_{volume_counter}.cbz"), 'w', zipfile.ZIP_STORED)

    for chapter_file in chapter_files:
        with zipfile.ZipFile(os.path.join(input_dir, chapter_file), 'r') as chapter_cbz:
            for image in sorted(chapter_cbz.namelist()):
                image_path = f"{chapter_file.replace('.cbz', '')}/{image}"
                merged_cbz.writestr(image_path, chapter_cbz.read(image))

        chapter_counter += 1

        # Save and start new volume if limit is reached
        if chapter_counter >= chapters_per_volume:
            merged_cbz.close()
            volume_counter += 1
            chapter_counter = 0
            merged_cbz = zipfile.ZipFile(os.path.join(output_dir, f"Volume_{volume_counter}.cbz"), 'w', zipfile.ZIP_STORED)

    merged_cbz.close()
    messagebox.showinfo("Success", "All volumes have been created successfully!")

# GUI for the CBZ Merger
def start_gui():
    def browse_input_dir():
        path = filedialog.askdirectory()
        input_dir_entry.delete(0, tk.END)
        input_dir_entry.insert(0, path)

    def browse_output_dir():
        path = filedialog.askdirectory()
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, path)

    def run_merging():
        input_dir = input_dir_entry.get()
        output_dir = output_dir_entry.get()
        chapters_per_volume = chapters_limit_entry.get()

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select input and output directories.")
            return

        try:
            chapters_per_volume = int(chapters_per_volume)
            merge_cbz_to_volumes(input_dir, output_dir, chapters_per_volume)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for chapters per volume.")

    # Initialize main window
    window = tk.Tk()
    window.title("CBZ Merger")

    # Input Directory
    tk.Label(window, text="Select Input Directory (CBZ files):").pack(pady=5)
    input_dir_entry = tk.Entry(window, width=50)
    input_dir_entry.pack()
    tk.Button(window, text="Browse", command=browse_input_dir).pack(pady=5)

    # Output Directory
    tk.Label(window, text="Select Output Directory:").pack(pady=5)
    output_dir_entry = tk.Entry(window, width=50)
    output_dir_entry.pack()
    tk.Button(window, text="Browse", command=browse_output_dir).pack(pady=5)

    # Chapters per Volume
    tk.Label(window, text="Chapters per Volume:").pack(pady=5)
    chapters_limit_entry = tk.Entry(window, width=10)
    chapters_limit_entry.insert(0, "20")
    chapters_limit_entry.pack()

    # Run Button
    tk.Button(window, text="Merge CBZ Files", command=run_merging).pack(pady=20)

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    start_gui()

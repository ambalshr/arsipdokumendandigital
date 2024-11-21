import sqlite3
import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from tkinter import ttk
from datetime import datetime
from tkinter import PhotoImage

# Fungsi untuk meng-upload dokumen
def upload_dokumen():
    try:
        file_path = filedialog.askopenfilename(title="Pilih file untuk di-upload")
        
        if not file_path:
            messagebox.showwarning("Peringatan", "Tidak ada file yang dipilih.")
            return
        
        # Mengambil nama file, kategori, deskripsi, dan tanggal upload
        nama_dokumen = os.path.basename(file_path)
        kategori = kategori_entry.get()
        deskripsi = deskripsi_entry.get()
        tanggal_upload = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = file_path

        # Menyimpan data ke database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO dokumen (nama_dokumen, kategori, deskripsi, tanggal_upload, path) 
            VALUES (?, ?, ?, ?, ?)
        """, (nama_dokumen, kategori, deskripsi, tanggal_upload, path))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Dokumen berhasil di-upload!")
        tampilkan_dokumen()  # Memperbarui tampilan setelah upload
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi untuk membuka dokumen
def buka_dokumen():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih dokumen yang ingin dibuka.")
            return

        dokumen_id = tree.item(selected_item)["values"][-1]

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT path FROM dokumen WHERE id = ?", (dokumen_id,))
        dokumen = cursor.fetchone()

        conn.close()

        if dokumen:
            file_path = dokumen[0]
            if os.path.exists(file_path):
                os.startfile(file_path)
            else:
                messagebox.showwarning("Peringatan", "Dokumen tidak ditemukan.")
        else:
            messagebox.showwarning("Peringatan", "Dokumen tidak ditemukan di database.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi untuk menampilkan dokumen di tabel dengan filter kategori
def tampilkan_dokumen(kategori_filter=None):
    try:
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "SELECT * FROM dokumen WHERE 1=1"
        params = []

        if kategori_filter:
            query += " AND kategori LIKE ?"
            params.append('%' + kategori_filter + '%')

        cursor.execute(query, tuple(params))
        dokumen_list = cursor.fetchall()

        for dokumen in dokumen_list:
            tree.insert("", "end", values=(dokumen[1], dokumen[2], dokumen[3], dokumen[4], dokumen[0]))

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi untuk mencari dokumen berdasarkan kategori
def cari_dokumen():
    kategori = kategori_filter_combobox.get()

    tampilkan_dokumen(kategori_filter=kategori)

# Fungsi untuk clear filter kategori
def clear_filter():
    kategori_filter_combobox.set('')
    tampilkan_dokumen()

# Fungsi untuk menghapus dokumen yang dipilih
def hapus_dokumen():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih dokumen yang ingin dihapus.")
            return

        dokumen_id = tree.item(selected_item)["values"][-1]

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus dokumen ini?")
        if confirm:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM dokumen WHERE id = ?", (dokumen_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Dokumen berhasil dihapus!")
            tampilkan_dokumen()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Setup window
root = Tk()
root.title("Aplikasi Arsip Dokumen Digital")
root.geometry("1200x800")
root.minsize(800, 600)
root.config(bg='#ececec')

# Menambahkan logo kantor di bagian kiri atas dan teks moto perusahaan
logo_image = PhotoImage(file="logo.png")  # Pastikan logo.png berada di folder yang sama dengan script Anda

# Ubah ukuran logo agar lebih kecil
logo_image = logo_image.subsample(8, 8) # Mengubah ukuran logo, sesuaikan angka ini untuk ukuran yang diinginkan

# Label untuk logo
logo_label = Label(root, image=logo_image, bg='#ececec')
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Label untuk moto perusahaan di bawah logo
moto_label = Label(root, text="Mengelola Dokumen dengan Profesionalisme", font=("Times New Roman", 10), bg='#ececec')
moto_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

# Header label untuk Aplikasi Arsip Dokumen Digital
header_label = Label(root, text="APLIKASI ARSIP DOKUMEN DIGITAL", font=("Arial", 18, "bold"), bg='#4CAF50', fg="white", padx=20, pady=10)
header_label.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

# Entry untuk kategori dan deskripsi
Label(root, text="Kategori", font=("Arial", 12), bg='#ececec').grid(row=3, column=0, padx=15, pady=10, sticky="e")
kategori_entry = Entry(root, font=("Arial", 12), width=30)
kategori_entry.grid(row=3, column=1, padx=15, pady=10, sticky="w")

Label(root, text="Deskripsi", font=("Arial", 12), bg='#ececec').grid(row=4, column=0, padx=15, pady=10, sticky="e")
deskripsi_entry = Entry(root, font=("Arial", 12), width=30)
deskripsi_entry.grid(row=4, column=1, padx=15, pady=10, sticky="w")

# Combobox untuk filter kategori
Label(root, text="Filter Kategori", font=("Arial", 12), bg='#ececec').grid(row=5, column=0, padx=15, pady=10, sticky="e")
kategori_filter_combobox = ttk.Combobox(root, values=["", "Kategori 1", "Kategori 2", "Kategori 3"], font=("Arial", 12), width=28)
kategori_filter_combobox.grid(row=5, column=1, padx=15, pady=10, sticky="w")

# Frame untuk tombol-tombol horizontal
button_frame = ttk.Frame(root)
button_frame.grid(row=6, column=0, columnspan=4, pady=15, sticky="ew")

# Button untuk upload dokumen
upload_button = Button(button_frame, text="Upload Dokumen", command=upload_dokumen, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", height=2)
upload_button.grid(row=0, column=0, padx=5, sticky="ew")

# Button untuk mencari dokumen
cari_button = Button(button_frame, text="Cari Dokumen", command=cari_dokumen, font=("Arial", 12), bg="#2196F3", fg="white", relief="solid", height=2)
cari_button.grid(row=0, column=1, padx=5, sticky="ew")

# Button untuk clear filter
clear_button = Button(button_frame, text="Clear Filter", command=clear_filter, font=("Arial", 12), bg="#FFC107", fg="white", relief="solid", height=2)
clear_button.grid(row=0, column=2, padx=5, sticky="ew")

# Button untuk hapus dokumen
hapus_button = Button(button_frame, text="Hapus Dokumen", command=hapus_dokumen, font=("Arial", 12), bg="#F44336", fg="white", relief="solid", height=2)
hapus_button.grid(row=0, column=3, padx=5, sticky="ew")

# Button untuk membuka dokumen
buka_button = Button(button_frame, text="Buka Dokumen", command=buka_dokumen, font=("Arial", 12), bg="#009688", fg="white", relief="solid", height=2)
buka_button.grid(row=0, column=4, padx=5, sticky="ew")

# Treeview untuk menampilkan dokumen
tree = ttk.Treeview(root, columns=("Nama Dokumen", "Kategori", "Deskripsi", "Tanggal Upload", "ID"), show="headings", height=8)
tree.grid(row=7, column=0, columnspan=4, padx=15, pady=10, sticky="nsew")

tree.heading("Nama Dokumen", text="Nama Dokumen")
tree.heading("Kategori", text="Kategori")
tree.heading("Deskripsi", text="Deskripsi")
tree.heading("Tanggal Upload", text="Tanggal Upload")
tree.heading("ID", text="ID")

# Grid weight untuk menyesuaikan ukuran elemen
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=2)
root.grid_columnconfigure(3, weight=2)

# Menampilkan dokumen yang sudah ada
tampilkan_dokumen()

# Menjalankan aplikasi
root.mainloop()

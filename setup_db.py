import sqlite3

# Membuat atau membuka database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Membuat tabel dokumen jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS dokumen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_dokumen TEXT NOT NULL,
    kategori TEXT NOT NULL,
    deskripsi TEXT,
    tanggal_upload TEXT,
    path TEXT NOT NULL
)
""")

# Commit dan tutup koneksi
conn.commit()
conn.close()

print("Database dan tabel dokumen berhasil dibuat.")

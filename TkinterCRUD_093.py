from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

# Fungsi untuk membuat database
def create_database():
    conn = sqlite3.connect("siswa.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS siswa (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama_siswa TEXT,
                        biologi INTEGER,
                        fisika INTEGER,
                        inggris INTEGER,
                        prediksi_fakultas TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect("siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM siswa")
    data = cursor.fetchall()
    conn.close()
    return data

# Fungsi untuk mengisi tabel
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk menambahkan data
def submit():
    nama = nama_var.get()
    biologi = biologi_var.get()
    fisika = fisika_var.get()
    inggris = inggris_var.get()

    if not nama or not biologi or not fisika or not inggris:
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    try:
        # Prediksi Fakultas berdasarkan nilai tertinggi
        prediksi_fakultas = ""
        biologi = int(biologi)
        fisika = int(fisika)
        inggris = int(inggris)
        if biologi >= fisika and biologi >= inggris:
            prediksi_fakultas = "Fakultas Biologi/Kedokteran"
        elif fisika >= biologi and fisika >= inggris:
            prediksi_fakultas = "Fakultas Teknik/Fisika"
        elif inggris >= biologi and inggris >= fisika:
            prediksi_fakultas = "Fakultas Sastra/Bahasa Inggris"

        conn = sqlite3.connect("siswa.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)", 
                       (nama, biologi, fisika, inggris, prediksi_fakultas))
        conn.commit()
        conn.close()
        populate_table()
        clear_inputs()
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Fungsi untuk memperbarui data
def update():
    record_id = selected_record_id.get()
    nama = nama_var.get()
    biologi = biologi_var.get()
    fisika = fisika_var.get()
    inggris = inggris_var.get()

    if not record_id:
        messagebox.showerror("Error", "Pilih data yang ingin diperbarui!")
        return

    try:
        # Prediksi Fakultas berdasarkan nilai tertinggi
        prediksi_fakultas = ""
        biologi = int(biologi)
        fisika = int(fisika)
        inggris = int(inggris)
        if biologi >= fisika and biologi >= inggris:
            prediksi_fakultas = "Fakultas Biologi/Kedokteran"
        elif fisika >= biologi and fisika >= inggris:
            prediksi_fakultas = "Fakultas Teknik/Fisika"
        elif inggris >= biologi and inggris >= fisika:
            prediksi_fakultas = "Fakultas Sastra/Bahasa Inggris"

        conn = sqlite3.connect("siswa.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE siswa SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=? WHERE id=?", 
                       (nama, biologi, fisika, inggris, prediksi_fakultas, record_id))
        conn.commit()
        conn.close()
        populate_table()
        clear_inputs()
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Fungsi untuk menghapus data
def delete():
    record_id = selected_record_id.get()

    if not record_id:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
        return

    try:
        conn = sqlite3.connect("siswa.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM siswa WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        populate_table()
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk membersihkan input
def clear_inputs():
    selected_record_id.set("")
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")

# Fungsi untuk mengisi input dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()

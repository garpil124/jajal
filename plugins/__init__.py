import glob
from os.path import dirname, isfile


def __list_all_modules():
    """
    Fungsi untuk menemukan semua modul Python dalam folder, kecuali file init.py.
    """
    work_dir = dirname(file)  # Mengambil path direktori saat ini
    mod_paths = glob.glob(work_dir + "/*/*.py")  # Mencari semua file .py dalam folder dan subfolder

    all_modules = [
        (((f.replace(work_dir, "")).replace("/", "."))[:-3])  # Mengubah path file menjadi modul Python
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("init.py")  # Menyaring file init.py
    ]

    return all_modules


ALL_MODULES = sorted(__list_all_modules())  # Menyusun modul-modul yang ditemukan
all = ALL_MODULES + ["ALL_MODULES"]  # Menambahkan modul-modul ke all untuk diimpor

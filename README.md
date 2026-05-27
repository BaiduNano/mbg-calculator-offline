# Kalkulator MBG

Aplikasi desktop untuk menghitung konversi Rupiah/USD ke hari MBG (Makan Bergizi Gratis).

## Fitur

- Konversi IDR atau USD ke hari MBG
- Perhitungan otomatis (tanpa tombol hitung)
- Pembaruan kurs USD/IDR secara live dari API
- Format angka Indonesia (titik sebagai pemisah ribuan, koma sebagai desimal)
- Multi mata uang (IDR / USD)

## Cara Menjalankan

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --name mbg_app --onefile main.py
```

Hasil build ada di folder `dist/`.

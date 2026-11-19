# Toko Buku API

Video YouTube (Unlisted): GANTI_DENGAN_LINK_VIDEO_ANDA

## Deskripsi
REST API toko buku menggunakan FastAPI, SQLite melalui aiosqlite, BackgroundTasks, dan asyncio.Lock.

## Persyaratan
Python 3.10 atau lebih baru.

## Instalasi (Windows PowerShell)
```powershell
cd "D:\UAS KPT\uts_toko_buku"
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Jika PowerShell memblokir aktivasi:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Menyiapkan database dan data awal
```powershell
python seed.py
```
Perintah seed aman dijalankan berulang kali; buku dengan judul yang sama tidak diduplikasi.

## Menjalankan server
```powershell
python -m uvicorn main:app --reload --port 8000
```
Buka http://127.0.0.1:8000/docs

## Endpoint Buku
- GET `/books/?skip=0&limit=10`
- GET `/books/{book_id}`
- POST `/books/`
- PUT `/books/{book_id}`
- DELETE `/books/{book_id}` (hard delete)

Contoh JSON POST:
```json
{
  "title": "Belajar Python",
  "author": "Budi",
  "category": "Teknologi",
  "price": 100000,
  "stock": 10
}
```

## Endpoint Transaksi
- POST `/transactions/` (HTTP 202, diproses di BackgroundTasks)
- GET `/transactions/?status=pending`
- GET `/transactions/{transaction_id}`

Contoh JSON POST:
```json
{
  "book_id": 1,
  "quantity": 1
}
```

Status: `pending` -> `processing` -> `completed`, atau `failed`.

## Uji race condition
Jalankan server dengan satu worker. Atur stok buku uji menjadi 1 melalui database/endpoint yang sesuai, lalu jalankan:
```powershell
python test_race.py
```
Dengan lock aktif, satu request berhasil dan request lain seharusnya menerima HTTP 409.

Untuk simulasi tanpa lock, hentikan server lalu jalankan:
```powershell
$env:LOCK_ENABLED="0"
python -m uvicorn main:app --port 8000
```
Reset stok buku uji menjadi 1 sebelum menguji ulang. Tanpa lock, dua request dapat sama-sama lolos pemeriksaan stok dan menyebabkan overselling. Aktifkan kembali dengan `$env:LOCK_ENABLED="1"` atau buka terminal baru.

**Catatan penting:** `asyncio.Lock` hanya berlaku dalam satu proses Python. Lock ini tidak dibagikan antar 4 worker Uvicorn. Untuk perlindungan lintas proses/worker, gunakan transaksi database atomik atau distributed lock.

## Benchmark Locust
Jalankan server, lalu di terminal kedua:
```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```
Buka http://localhost:8089. Catat hasil pengujian sesuai skenario tugas: GET 100 request dengan concurrency 20 dan POST 50 request dengan concurrency 10. Ulangi server dengan 1 worker dan 4 workers, lalu bandingkan hasil aktual pada laporan.

Contoh 4 workers:
```powershell
python -m uvicorn main:app --workers 4 --port 8000
```
Jangan mengklaim hasil benchmark sebelum benar-benar menjalankan pengujian.

## Laporan
Kerangka laporan tersedia di `docs/README_LAPORAN.md`. Lengkapi dengan diagram, hasil benchmark aktual, analisis, dan dokumentasi video.

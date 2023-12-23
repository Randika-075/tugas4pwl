# Cara menjalankan

1. buat database dengan nama `tugas_4_ra`
2. buka terminal dan arahkan ke folder ini
3. jalankan perintah sebagai berikut
 - python -m venv env
    - .\env\Scripts\activate
    - .\env\Scripts\pip install -e .
    - .\env\Scripts\alembic -c .\development.ini upgrade head
    - .\env\Scripts\pserve .\development.ini --reload
4. buka browser dan akses `http://localhost:6543/`
- list api
    - `http://localhost:6543/api/v1/movie`
    - `http://localhost:6543/api/v1/movie/{id}`
    - `http://localhost:6543/api/v1/movie/create`
    - `http://localhost:6543/api/v1/movie/update/{id}`
    - `http://localhost:6543/api/v1/movie/delete/{id}`
    - `http://localhost:6543/api/v1/login`
    - `http://localhost:6543/api/v1/register`
- contoh penggunaan api ada di file api.rest
5. untuk menghentikan server tekan `ctrl + c` pada terminal

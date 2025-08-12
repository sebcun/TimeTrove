![TimeTrove](https://i.imgur.com/2c2VcI4.png)
TimeTrove is a web application for creating, storing, and opening digital time capsules. Users can write messages, upload files, and set a future date for their capsule to be opened. When the time arrives, the capsule becomes accessible, and users can retrieve their memories or files.

## Features

- Ability to create digital time capsules with messages, and files.
- Set a future date to open the time capsule.
- Email notifications for when time capsules are ready.
- No account needed, and all data is encrypted.

## Installation

1. **Clone the repo**

   ```powershell
   git clone https://github.com/sebcun/TimeTrove.git
   cd TimeTrove
   ```

2. **Install dependencies**

Make sure you have Python 3.13+ installed.

```powershell
pip install -r requirements.txt
```

3. **Setup environment variables:**  
   Create a `.env` file in the project root with the following content (replace values as needed):

   ```
   # FLASK
   FLASK_RUN_HOST=0.0.0.0
   FLASK_RUN_PORT=5000
   FLASK_DEBUG=True

   # EMAIL
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True

   # MISC
   DOMAIN=http://localhost:5000/
   SECRET_KEY=your-secret-key
   SQLLITE_DB=capsules.db
   ENCRYPTION_KEY=
   ```

- If `SQLLITE_DB` is left empty, the app will use JSON files for database storage instead of SQLite.
- If any of the EMAIL-related `.env` options or `DOMAIN` is empty, the app will **not** send email notifications.

4. **Setup Encryption** (optional)
   If you would like to have encryption enabled, you must set the `ENCRYPTION_KEY` option in the .env. This must be a Fernet key. There is a script to create one and copy it to the clipboard. Just simply Run

```powershell
python generateKey.py
```

5. **Run the application:**

   ```powershell
   python app.py
   ```

6. **Access the app:**  
   Open your browser and go to [http://localhost:5000](http://localhost:5000)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

Made with ❤️ by [sebcun](https://github.com/sebcun)

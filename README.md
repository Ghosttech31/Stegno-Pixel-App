---
## 🔐 Secure Communication Using Image Steganography with AES Encryption

This is a beginner-friendly **web application** that allows users to
**securely encode and decode secret messages**
within images using a combination of **Image Steganography** and **AES encryption**.
It also includes user authentication and logs for accountability.
---

## Login

- username = "admin"
- password = "admin123"

### 📸 Key Features

- ✅ **User Registration & Login**
- 🔐 **AES Encryption** of messages
- 🖼️ **Steganography**: Embed encrypted messages into images
- 🔍 **Decoding**: Extract and decrypt messages from images
- 💾 **File Upload & Download Support**
- 📜 **User Logs**: Tracks login and activity
- 🎨 Clean, responsive front-end design

---

### 🧠 Technologies Used

- **Python (Flask)** — Backend web framework
- **HTML, CSS, JavaScript** — Frontend
- **Pillow** — Image processing
- **Cryptography (AES)** — Encryption module
- **JSON** — For lightweight user database
- **Bootstrap** — Styling (optional)
- **Render** — Deployment platform (optional)

---

### 🚀 How to Run Locally

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-steg.git
cd secure-steg
```

#### 2. Set up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the App

```bash
python secure_steg/app.py
```

---

### 🌐 Live Demo (Optional)

If hosted (e.g. on [Render](https://render.com)):

> 🔗 [https://your-app-name.onrender.com](https://your-app-name.onrender.com)

---

### 🛡️ Security Note

- Passwords are hashed using `Werkzeug`.
- Messages are encrypted using **AES** before being embedded into images.

---

### 📁 Project Structure

```
secure_steg/
├── app.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── encode.html
│   └── decode.html
├── static/
│   ├── uploads/
│   └── encoded/
├── steg_crypto.py
├── users.json
└── logs.txt
```

---

### 👤 Author

- **Vishal Sai**
- GitHub : https://github.com/Ghosttech31/Stegno-Pixel-App.git

---

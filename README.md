# Fake Certificate Detection System 🛡️

A secure and robust system to detect fake certificates using digital hashing and QR code verification. This project ensures the authenticity of documents by storing their cryptographic hashes in a secure database.

## 🚀 Features

- **Immutable Verification**: Uses SHA-256 hashing to create unique digital fingerprints for every certificate.
- **QR Code Integration**: Automatically extracts and verifies metadata (Issuer ID, Certificate UID) from embedded QR codes.
- **Tamper Detection**: Instantly detects if a certificate has been altered by even a single pixel.
- **Dual-Layer Validation**: Checks validity through both file hash and QR code data.
- **User-Friendly Interface**: Simple web interface for easy uploading and verification.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL / SQLite (via SQLAlchemy)
- **Image Processing**: Pillow, pdf2image
- **QR Decoding**: Pyzbar
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.8+**
2.  **System Dependencies** (required for image & QR processing):
    *   **Ubuntu/Debian**: `sudo apt-get install libzbar0 poppler-utils`
    *   **MacOS**: `brew install zbar poppler`
    *   **Windows**: Install [Poppler](http://blog.alivate.com.au/poppler-windows/) and add to PATH.

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd fakecertificate_detection
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    Create a `.env` file in the root directory and add your database URL:
    ```env
    DATABASE_URL=sqlite:///./sql_app.db
    # For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

## 🏃‍♂️ Running the Application

### 1. Start the Backend Server
Run the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 2. Launch the Frontend
Simply open `frontend/index.html` in your web browser. 
*(No separate server required for this static frontend, but you can use `python -m http.server` inside the `frontend` folder if preferred).*

## 🔌 API Endpoints

-   `GET /`: Health check.
-   `POST /upload`: Upload a certificate to register it.
    -   **Input**: File (PDF/Image)
    -   **Process**: Hashes file, extracts QR, saves to DB.
    -   **Output**: JSON with status and extracted data.
-   `POST /verify`: Upload a certificate to verify it.
    -   **Input**: File (PDF/Image)
    -   **Process**: Hashes file, compares with DB.
    -   **Output**: `VALID` or `TAMPERED / NOT FOUND`.

## 📂 Project Structure

```
fakecertificate_detection/
├── app/
│   ├── database.py    # Database connection & session
│   ├── main.py        # API routes & logic
│   ├── models.py      # Database models (Certificate)
│   ├── qr_utils.py    # QR code extraction logic
│   └── utils.py       # Hashing utilities
├── frontend/
│   ├── index.html     # Landing page
│   └── action.html    # Upload/Verify interface
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

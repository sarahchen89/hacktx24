# ReSplit

A full-stack HackTX project that helps users scan grocery or restaurant receipts, identify individual line items using OCR and AI, and split costs with friends. Ideal for roommates or group outings where splitting the bill fairly is essential.

## Features

- **Scan Receipts**: Upload or take a photo of a receipt to automatically detect line items and prices using the [Mindee OCR API](https://www.mindee.com/).
- **Smart Item Detection**: Uses the [OpenAI API](https://openai.com/) to intelligently guess unclear or ambiguous line items (e.g., generic terms or abbreviations).
- **Split Costs**: Users can assign items to individuals and calculate who owes what.
- **Frontend Access**: Built with React Native for cross-platform support on iOS, Android, and web.
- **Backend**: Flask server with SQLAlchemy for persistent storage and a RESTful API for managing receipts and users.

## Tech Stack

- **Frontend**: React Native
- **Backend**: Flask, SQLAlchemy
- **OCR**: Mindee Receipt OCR API
- **AI Assistance**: OpenAI GPT 3.5 Turbo
- **Payments**: Attempted integration with the Venmo API to auto-generate payment requests, but API limitations prevented full implementation

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sarahchen89/hacktx24.git
cd hacktx24
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py
flask run
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 4. Environment Variables

Create a `.env` file in both `/frontend` and `/backend` folders and add your API keys:

```env
MINDEE_API_KEY=your_mindee_api_key
OPENAI_API_KEY=your_openai_api_key
VENMO_CLIENT_ID=your_venmo_id (not used)
VENMO_CLIENT_SECRET=your_venmo_secret (not used)
```

### Limitations

- Venmo API is restricted and does not allow arbitrary money requests without special permissions; thus, this feature is stubbed in the UI.
- OCR accuracy may vary depending on receipt quality; OpenAI is used to enhance unclear results.

# Excel Translation Service - Backend

FastAPI backend for Excel translation service with async processing and Pydantic validation.

## Features

- 📤 **File Upload**: Upload Excel files (.xlsx, .xls)
- 🔄 **Async Translation**: Batch translation with async processing
- ✅ **Validation**: Pydantic models for request/response validation
- 🌍 **Multi-language**: Support for multiple languages
- 🎯 **Mock Mode**: Test without external API (set `USE_MOCK_TRANSLATION=True`)

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env` file and update settings:
- Set `TRANSLATION_API_KEY` for real translation API
- Set `USE_MOCK_TRANSLATION=False` to use real API

### 3. Run Server

```bash
uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

## API Documentation

### Swagger UI
Visit `http://localhost:8000/docs` for interactive API documentation

### Endpoints

#### POST `/api/v1/upload`
Upload Excel file

**Request:**
- `file`: Excel file (.xlsx or .xls)

**Response:**
```json
{
  "success": true,
  "file_id": "abc123",
  "filename": "sample.xlsx",
  "file_size": 12345,
  "upload_time": "2024-01-01T12:00:00",
  "sheet_names": ["Sheet1"],
  "row_count": 100,
  "column_count": 5
}
```

#### POST `/api/v1/translate`
Translate Excel column

**Request:**
```json
{
  "file_id": "abc123",
  "column_index": 0,
  "source_lang": "ko",
  "target_lang": "en",
  "sheet_name": "Sheet1"
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "original": "안녕하세요",
      "translated": "[EN] 안녕하세요",
      "source_lang": "ko",
      "target_lang": "en"
    }
  ],
  "total_count": 1
}
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Configuration
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   └── middleware/       # Middleware
├── requirements.txt
└── .env
```

## Supported Languages

- English (en)
- Korean (ko)
- Japanese (ja)
- Chinese (zh)
- Spanish (es)
- French (fr)
- German (de)

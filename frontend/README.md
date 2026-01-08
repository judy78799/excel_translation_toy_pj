# Excel Translation Service - Frontend

React frontend for Excel translation service with modern UI and drag-and-drop file upload.

## Features

- 🎨 **Modern UI**: Beautiful dark theme with smooth animations
- 📤 **Drag & Drop**: Easy file upload with drag-and-drop support
- 🔄 **Real-time Translation**: See results as they're processed
- 📊 **Result Table**: View original and translated text side-by-side
- 💾 **Export**: Download results as CSV
- 🌍 **Multi-language**: Support for 7+ languages

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL (Optional)

Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm start
```

App will start at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── common/          # Button, Input, Alert
│   │   ├── FileUpload/      # File upload component
│   │   └── ResultTable/     # Results display
│   ├── pages/               # HomePage, TranslationPage
│   ├── services/            # API integration
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utilities
│   ├── constants/           # App constants
│   ├── App.jsx              # Main app with routing
│   ├── index.js             # Entry point
│   └── index.css            # Global styles
└── package.json
```

## Key Technologies

- ⚛️ **React 18**: Latest React with hooks
- 🎨 **Styled Components**: CSS-in-JS styling
- 🚀 **React Router**: Client-side routing
- 📡 **Axios**: HTTP client for API calls

## Features Showcase

### File Upload
- Drag-and-drop or click to upload
- File validation (type, size)
- Real-time feedback

### Translation Controls
- Select source and target languages
- Choose which column to translate
- View file metadata

### Results Display
- Professional table layout
- Export to CSV
- Smooth animations

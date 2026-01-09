# 📝 엑셀 번역 토이 프로젝트 (Excel Translation Toy Project)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

FastAPI(백엔드)와 React + Tailwind CSS(프론트엔드)로 구축된 엑셀/CSV 파일 자동 번역 웹 애플리케이션입니다. Google Cloud Translation API를 사용하여 파일을 업로드하면 자동으로 내용을 추출하고 번역합니다.

![Project Preview](https://via.placeholder.com/800x400?text=Project+Screenshot)

## 🚀 주요 기능 (Features)

### Backend (FastAPI + Pandas)
- ⚡ **비동기 처리**: `async/await`를 활용한 논블로킹 번역 처리 속도 최적화.
- 📊 **Excel & CSV 지원**: `pandas`를 활용하여 `.xlsx`, `.xls`, `.csv` 파일을 강력하게 파싱.
- 🌍 **Google Cloud Translation API**: 고품질 번역 지원 (HTML 엔티티 디코딩 처리 완료: `&#39;` → `'`).
- ✅ **원스텝 프로세스**: 파일 업로드, 파싱, 번역이 단일 요청으로 한 번에 처리됨.
- 🛠️ **설정 가능**: 실제 API 모드와 테스트용 Mock 모드 간 쉬운 전환.

### Frontend (React + Tailwind CSS)
- 🎨 **모던 UI**: **Tailwind CSS v3**를 사용한 깔끔하고 반응형인 디자인.
- 📤 **드래그 앤 드롭**: 직관적인 파일 업로드 인터페이스.
- ⚡ **실시간 피드백**: 로딩 상태 표시 및 명확한 에러 핸들링.
- 💾 **CSV 내보내기**: 번역된 결과를 즉시 CSV로 다운로드 가능.

## 📋 기술 스택 (Tech Stack)

### Backend
- **Framework**: FastAPI
- **Data Processing**: Pandas, OpenPyXL
- **HTTP Client**: HTTPX (Async)
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS v3
- **Icons**: Lucide React
- **HTTP**: Native Fetch API

## 🛠️ 빠른 시작 (Quick Start)

### 사전 요구 사항
- Python 3.9 이상
- Node.js 16 이상
- Google Cloud Translation API Key

### 1. 백엔드 설정 (Backend Setup)

```bash
cd backend
# 가상 환경 생성 (권장 사항)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 의존성 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 TRANSLATION_API_KEY 항목에 본인의 키를 입력하세요.
```

서버 실행:
```bash
uvicorn app.main:app --reload
```
백엔드 주소: `http://localhost:8000`

### 2. 프론트엔드 설정 (Frontend Setup)

```bash
cd frontend
# 의존성 패키지 설치
npm install

# 개발 서버 시작
npm start
```
프론트엔드 주소: `http://localhost:3000`

## 🎯 사용 흐름 (Usage Flow)

1.  **설정**: 소스 언어(예: 한국어)와 타겟 언어(예: 영어)를 선택합니다.
2.  **업로드**: `.xlsx` 또는 `.csv` 파일을 드래그 앤 드롭하여 업로드합니다.
3.  **처리**: 시스템이 자동으로 다음 작업을 수행합니다:
    *   파일 업로드 및 저장.
    *   지정된 컬럼(기본값: `text`)에서 텍스트 추출.
    *   Google API를 통해 일괄 번역.
4.  **결과**: 테이블에서 원문과 번역문을 비교하고 CSV로 다운로드합니다.

## 🔧 환경 설정 (.env)

| 변수명 | 설명 | 기본값 |
|----------|-------------|---------|
| `TRANSLATION_API_KEY` | Google Cloud API Key (실제 번역 시 필수) | `""` |
| `USE_MOCK_TRANSLATION` | API 키 없이 테스트하려면 `True`로 설정 | `False` |
| `MAX_FILE_SIZE` | 최대 파일 업로드 크기 (바이트) | `10MB` |

## 📂 프로젝트 구조 (Project Structure)

```
excel-translation-toy-pj/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API 라우트 (upload.py, translation.py)
│   │   ├── core/              # 설정 (config.py)
│   │   ├── services/          # 비즈니스 로직 (file_service, external_api_service)
│   │   └── main.py            # 앱 진입점
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── App.jsx            # 메인 컴포넌트
    │   ├── index.css          # Tailwind 지시어 포함 CSS
    │   └── index.js           # 프론트엔드 진입점
    ├── tailwind.config.js     # Tailwind 설정 파일
    └── package.json
```

## 📄 라이선스 (License)
MIT License

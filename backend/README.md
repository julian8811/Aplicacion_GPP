# Backend - GPP Application

FastAPI backend for the GPP (Gestión de Pequeñas Empresas) application.

## Architecture

The backend follows a modular architecture:

```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── auth/          # Authentication logic
│   ├── core/          # Core business logic
│   ├── config.py      # Configuration management
│   ├── supabase.py    # Supabase client
│   ├── pdf_generator.py  # PDF generation
│   └── recomendaciones.py # Recommendations engine
├── main.py            # FastAPI application entry point
├── requirements.txt    # Python dependencies
└── legacy/            # Archived Streamlit app
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth + Google OAuth
- **Server**: Uvicorn

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret

### Running

Development:
```bash
uvicorn main:app --reload --port 8000
```

Production:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user
- `GET /auth/google` - Initiate Google OAuth
- `GET /auth/google/callback` - Google OAuth callback

### Profiles
- `GET /api/profiles/me` - Get current user's profile
- `PUT /api/profiles/me` - Update profile

### Matrices
- `GET /api/matrices` - Get PA/PO matrix questions

### Evaluations
- `GET /api/evaluations` - List evaluations
- `POST /api/evaluations` - Create evaluation
- `GET /api/evaluations/{id}` - Get evaluation
- `PUT /api/evaluations/{id}` - Update evaluation
- `DELETE /api/evaluations/{id}` - Delete evaluation

### Results
- `POST /api/results/calculate` - Calculate evaluation results

### Action Plans
- `GET /api/action-plans` - List action plans
- `POST /api/action-plans` - Create action plan
- `PUT /api/action-plans/{id}` - Update action plan
- `DELETE /api/action-plans/{id}` - Delete action plan

### PDF
- `GET /api/pdf/{evaluation_id}` - Generate PDF report

### Invites
- `POST /api/invites` - Send invite
- `GET /api/invites` - List invites
- `PUT /api/invites/accept` - Accept invite

## Legacy Code

The original Streamlit application has been archived to `legacy/app_streamlit.py`.
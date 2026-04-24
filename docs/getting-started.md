# Komma igång med SäkerSite

## Förutsättningar

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/) v2+
- Git
- (Valfritt) Python 3.11+ för lokal edge-utveckling
- (Valfritt) Node.js 20+ för lokal webbutveckling

## Snabbstart (Docker Compose)

```bash
# 1. Klona repot
git clone https://github.com/your-org/sakersite.git
cd sakersite

# 2. Konfigurera miljövariabler
cp .env.example .env
# Redigera .env med era verkliga hemligheter om det behövs
# Standard-konfigurationen fungerar för lokal utveckling

# 3. Starta alla tjänster
docker compose -f infra/docker-compose.yml up

# 4. Vänta på att alla tjänster startar (~30 sekunder)
# Se att "sakersite-api_1 | sakersite_api_started" visas i loggen

# 5. Öppna webbläsaren
open http://localhost:3000

# 6. Logga in
# E-post:    admin@sakersite.se
# Lösenord:  changeme
```

## Lokal utveckling

### API (FastAPI)

```bash
cd apps/api

# Skapa virtualenv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installera beroenden
pip install -r requirements-dev.txt

# Kör PostgreSQL (behöver Docker)
docker compose -f ../../infra/docker-compose.yml up postgres minio -d

# Kör migrationer
DATABASE_URL=postgresql+asyncpg://sakersite:changeme_postgres@localhost:5432/sakersite \
  alembic upgrade head

# Seed-data
DATABASE_URL=postgresql+asyncpg://sakersite:changeme_postgres@localhost:5432/sakersite \
  python -m api.seed

# Starta API
DATABASE_URL=postgresql+asyncpg://sakersite:changeme_postgres@localhost:5432/sakersite \
  uvicorn api.main:app --reload --port 8000

# API-dokumentation: http://localhost:8000/docs
```

### Web (Next.js)

```bash
cd apps/web

# Installera beroenden
npm install

# Starta dev-server
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev

# Öppna: http://localhost:3000
```

### Edge Worker

```bash
cd apps/edge

# Installera beroenden
pip install -r requirements-dev.txt

# Kör i mock-läge (ingen kamera behövs)
MOCK_MODE=true \
INGEST_API_URL=http://localhost:8000/events/ingest \
INGEST_API_KEY=dev_edge_key \
python -m edge.main --mock
```

## Köra tester

### API-tester

```bash
cd apps/api
pip install -r requirements-dev.txt
pytest -v
```

### Edge-tester

```bash
cd apps/edge
pip install -r requirements-dev.txt
pytest -v
```

### Web-linting och typkontroll

```bash
cd apps/web
npm install
npm run lint
npm run typecheck
```

## Konfigurera en riktig kamera

1. Redigera `.env`:
```bash
MOCK_MODE=false
RTSP_URL=rtsp://användarnamn:lösenord@192.168.1.100:554/stream1
```

2. Starta om edge-workern:
```bash
docker compose -f infra/docker-compose.yml restart edge
```

3. Kontrollera loggarna:
```bash
docker compose -f infra/docker-compose.yml logs -f edge
```

## Miljövariabler

Se `.env.example` för fullständig lista. Viktiga variabler:

| Variabel | Beskrivning | Standard |
|---|---|---|
| `POSTGRES_PASSWORD` | Databaslösenord | `changeme_postgres` |
| `JWT_SECRET_KEY` | JWT-signeringsnyckel | `dev_secret_change_in_prod` |
| `API_KEY_EDGE` | Edge worker API-nyckel | `dev_edge_key` |
| `MOCK_MODE` | Kör edge i mock-läge | `true` |
| `RTSP_URL` | RTSP-kamera URL | — |
| `RETENTION_DAYS` | Datalagringstid (GDPR) | `30` |

## Viktiga säkerhetsnoteringar

> ⚠️ **Ändra alltid dessa i produktion:**
> - `POSTGRES_PASSWORD`
> - `MINIO_ROOT_PASSWORD`
> - `JWT_SECRET_KEY` (generera med `openssl rand -hex 32`)
> - `API_KEY_EDGE`
> - Adminlösenord (`changeme` → starkt lösenord)

## Felsökning

### Docker Compose startar inte

```bash
# Kontrollera att portarna är lediga
lsof -i :3000 -i :8000 -i :5432 -i :9000

# Se detaljerade loggar
docker compose -f infra/docker-compose.yml logs
```

### API ger 500-fel

```bash
# Kontrollera att migrationer körts
docker compose -f infra/docker-compose.yml exec api alembic current

# Kontrollera databasanslutning
docker compose -f infra/docker-compose.yml exec api python -c "from api.database import engine; print('OK')"
```

### Edge worker ansluter inte till API

```bash
# Kontrollera att API är uppe
curl http://localhost:8000/health

# Kontrollera API-nyckelkonfiguration
grep API_KEY_EDGE .env
```

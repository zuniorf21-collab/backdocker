# Telemed Backend

Backend Django 5 + DRF com PostgreSQL, Redis, Celery, armazenamento S3 e vídeo via Twilio.

## Rodar local com Docker
1. Crie/ajuste `.env` na raiz (exemplos abaixo).
2. Suba os containers: `docker-compose up --build`.
3. Aplique migrações: `docker-compose exec web python manage.py migrate`.
4. Crie um superusuário: `docker-compose exec web python manage.py createsuperuser`.
5. Docs: `http://localhost:8000/docs` (Swagger) ou `http://localhost:8000/redoc`.
6. Celery worker/beat já sobem como serviços `worker` e `beat`.

## Variáveis de ambiente úteis
- Django: `DEBUG`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOW_ALL_ORIGINS`.
- Banco (Postgres): `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.
- Redis/Celery/Cache: `REDIS_HOST`, `REDIS_PORT`.
- JWT/rate limit: `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS`, `RATE_LIMIT`.
- S3 (opcional): `USE_S3_STORAGE=1`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`, `AWS_S3_ENDPOINT_URL` (para MinIO/compatíveis), `AWS_S3_CUSTOM_DOMAIN`.
- Twilio Video (opcional): `TWILIO_ENABLED=1`, `TWILIO_ACCOUNT_SID`, `TWILIO_API_KEY_SID`, `TWILIO_API_KEY_SECRET`, `TWILIO_AUTH_TOKEN` (se usar Account SID/Auth Token para REST), `TWILIO_ROOM_TYPE` (ex.: `go`).

## Apps principais
- `accounts`: usuário customizado (paciente, médico, admin) com JWT (SimpleJWT)
- `patients`, `doctors`: perfis detalhados e cadastro de médico pelo admin
- `payments`: simulação de gateway e liberação de fila após pagamento aprovado
- `queueapp`: fila FIFO de espera, endpoints `/queue/join` e `/queue/next`
- `consultations`: ciclo da consulta (start/end), geração de token/sala Twilio (fallback aleatório em dev)
- `prescriptions`, `certificates`: geração de receita/atestado com QR base64 e registro em prontuário
- `documents`: upload de arquivos (S3 se habilitado)
- `audit`: middleware de auditoria armazenando requisições

## Estrutura de diretórios
- `backend/` código Django
- `docker-compose.yml` orquestra web, worker, beat, Postgres e Redis
- `Dockerfile` imagem web/worker
- `requirements.txt` dependências Python
- `deploy/aws/` scripts e guia para subir em EC2 (Docker Compose)

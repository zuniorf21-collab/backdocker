# Deploy rápido em EC2 (Docker Compose)

DNS público informado: `ec2-3-144-24-228.us-east-2.compute.amazonaws.com`.

Passo a passo:
1. Conecte por SSH (ex.: `ssh -i /caminho/sua-chave.pem ubuntu@ec2-3-144-24-228.us-east-2.compute.amazonaws.com`).
2. Instale Docker/Docker Compose plugin: `sudo bash deploy/aws/bootstrap.sh` (ou copie o conteúdo e execute).
3. Clone o repositório ou sincronize os arquivos do projeto para a instância.
4. Crie `.env` na raiz a partir de `.env.aws.example`, ajustando:
   - `DJANGO_SECRET_KEY` forte.
   - `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` com seu domínio ou DNS público.
   - Credenciais S3 (`USE_S3_STORAGE=1`) e Twilio, se for usar vídeo.
   - Ajuste senhas de Postgres/Redis conforme desejar.
5. Suba os containers: `docker compose up -d --build`.
6. Aplique migrações e crie admin:
   - `docker compose exec web python manage.py migrate`
   - `docker compose exec web python manage.py createsuperuser`
7. Certifique-se de abrir as portas de segurança na AWS (SG) para 80/443 ou 8000/5050 conforme necessário. Para produção, prefira um ALB/Nginx na frente e HTTPS.

Notas:
- O arquivo `docker-compose.yml` já orquestra web, worker e beat Celery, Postgres e Redis.
- Armazenamento de mídia: habilite S3 via `USE_S3_STORAGE=1`. Para estáticos, você pode usar o mesmo bucket rodando `python manage.py collectstatic` e configurando CDN/CloudFront.
- Para TLS, coloque um proxy (Nginx/ALB) com certificado (ACM) em frente ao serviço web.

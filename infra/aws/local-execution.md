docker build -f infra/aws/Dockerfile -t taskmgmt-api:local .

docker run --rm --env-file .env.local -p 8000:80 taskmgmt-api:local
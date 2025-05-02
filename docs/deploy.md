WINDOWS:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

LINUX:
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
ou
gunicorn -w ${WEB_CONCURRENCY:-$(($(nproc)*2+1))} -k uvicorn.workers.UvicornWorker main:app

## Configuração Recomendada
- `WEB_CONCURRENCY`: Define o número de workers (padrão: 2 * núcleos_CPU + 1)
- Usar variáveis de ambiente para configurações específicas de ambiente
- Requer Bash 4+ ou shell compatível para cálculo automático
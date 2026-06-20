FROM python:3.12-slim

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --no-create-home appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY --chown=appuser:appgroup . .

EXPOSE 8010

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]

# ---- Builder stage ----
FROM python:3.11-slim as builder

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Final stage ----
FROM python:3.11-slim

# ---- Copy installed packages ----
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# ---- Copy project ----
COPY . .

# ---- Flask config ----
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# ---- Expose port ----
EXPOSE 5000

# ---- Health check ----
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# ---- Run app ----
CMD ["flask", "run"]
ENV FLASK_ENV=development

# ---- Expose port ----
EXPOSE 5000

# ---- Run app ----
CMD ["flask", "run"]

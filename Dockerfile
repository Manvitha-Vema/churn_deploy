# ---------- 1️⃣  Use a stable Python base image ----------
FROM python:3.11-slim

# ---------- 2️⃣  Set working directory ----------
WORKDIR /app

# ---------- 3️⃣  Copy your files ----------
COPY . .

# ---------- 4️⃣  Install dependencies ----------
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ---------- 5️⃣  Expose the web port ----------
EXPOSE 10000

# ---------- 6️⃣  Start Flask with gunicorn ----------
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]

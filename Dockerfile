# Force Python 3.11 base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
COPY churn.py .
COPY sample.csv .
COPY runtime.txt .
COPY render.yaml .

# Install system build tools (for XGBoost/SHAP)
RUN apt-get update && apt-get install -y build-essential

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Start command
CMD ["python", "churn.py", "sample.csv", "--min_features", "5"]

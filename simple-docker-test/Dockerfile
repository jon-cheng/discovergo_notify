FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dataframe_job.py .

CMD ["python", "dataframe_job.py"]
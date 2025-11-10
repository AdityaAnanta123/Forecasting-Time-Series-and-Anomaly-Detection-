# Gunakan base image python
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Set PYTHONPATH agar folder src dikenali sebagai root package
ENV PYTHONPATH="/app/src"

# Copy semua file proyek
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan aplikasi (sesuaikan entry point-nya)
CMD ["python", "src/main.py"]
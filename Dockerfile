FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create output and template folders if needed
RUN mkdir -p templates output

# Expose port
EXPOSE 5110

# Start with Gunicorn
CMD ["gunicorn", "templateR:app", "--bind", "0.0.0.0:5110", "--workers", "4"]


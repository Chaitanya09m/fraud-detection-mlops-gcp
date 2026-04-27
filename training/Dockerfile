FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only training code
COPY train_model.py .

# Create artifacts folder
RUN mkdir -p /app/artifacts

# Run training
CMD ["python", "train_model.py"]

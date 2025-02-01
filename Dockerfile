# Use official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies using pyproject.toml (or requirements.txt if applicable)
RUN pip install --upgrade pip && pip install .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI with the correct module path
CMD ["uvicorn", "src.backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the app port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

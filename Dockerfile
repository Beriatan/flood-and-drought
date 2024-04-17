# Stage 1: Build the React frontend
FROM node:16 as frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup the Python environment for Flask
FROM python:3.9.18-slim
WORKDIR /app

# Copy the frontend build from the previous stage
COPY --from=frontend /app/frontend/build ./frontend/build

# Copy the backend code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]

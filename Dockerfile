FROM python:3.9-slim

WORKDIR /app

# Set HOME environment so Streamlit writes to /app/.streamlit
ENV HOME=/app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY src/ ./src/

# Create and set permissions for the .streamlit folder
RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit

COPY .streamlit /app/.streamlit

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

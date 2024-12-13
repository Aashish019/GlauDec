FROM python:3.9-slim as builder

RUN python3 -m venv /opt/venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends wkhtmltopdf && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . /app

ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "GlauDec.py"]

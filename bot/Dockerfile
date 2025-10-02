FROM python:3.12-slim

WORKDIR app/

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY database/ ./database/
COPY config.py .
COPY app.py .

CMD python app.py
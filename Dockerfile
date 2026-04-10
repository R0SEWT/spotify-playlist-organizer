FROM python:3.11.12-slim

RUN useradd -m app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "index:app"]

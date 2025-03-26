FROM python:3.11-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie plików aplikacji
COPY . /app

# Instalacja zależności
RUN pip install --no-cache-dir fastapi uvicorn perc pydantic pyahocorasick

# Otworzenie portu dla aplikacji
EXPOSE 8000

# Uruchomienie aplikacji FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8800"]
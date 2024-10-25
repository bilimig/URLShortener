
# **Instrukcja konfiguracji środowiska deweloperskiego oraz uruchomienia aplikacji**

---

## **Opis projektu**
Aplikacja jest prostym systemem skracania URL, który wykorzystuje FastAPI jako backend, Celery do obsługi zadań asynchronicznych oraz PostgreSQL i Redis jako bazy danych. Aplikacja jest uruchamiana w środowisku kontenerowym za pomocą Docker Compose.

## **Spis treści**
1. Wymagania
2. Konfiguracja środowiska
3. Uruchomienie aplikacji
4. Korzystanie z aplikacji
5. Testowanie aplikacji

## **Wymagania**
- **Docker**: https://www.docker.com/get-started
- **Docker Compose**: https://docs.docker.com/compose/install/

## **Konfiguracja środowiska**

1. **Klonowanie repozytorium**:
   
   Skopiuj repozytorium projektu na lokalny komputer:

## **Uruchomienie aplikacji**

1. **Uruchomienie aplikacji za pomocą Docker Compose**:

   Aby uruchomić aplikację, użyj następującego polecenia:

   ``` docker-compose up --build ```

   Polecenie to uruchomi wszystkie niezbędne kontenery:
   
   - **PostgreSQL** jako baza danych.
   - **Redis** jako broker dla Celery.
   - **Web** - aplikacja FastAPI dostępna na http://localhost:8000.
   - **Celery Worker** - do obsługi zadań asynchronicznych.

2. **Zatrzymanie aplikacji**:

   Aby zatrzymać aplikację, użyj polecenia:

   ``` docker-compose down ```

## **Korzystanie z aplikacji**

- **Strona główna aplikacji** znajduje się pod adresem: http://localhost:8000.
- **Swagger UI** dla testowania endpointów API jest dostępny pod adresem: http://localhost:8000/docs

## **Testowanie aplikacji**
- Testy napisne w pytescie do uruchomienia trzeba wejść w kontener Celery Worker.
- Użyć komendy: ``` pytest app/tests.py ```

## **Dodatkowe informacje**
- Aplikacja wykorzystuje FastAPI do komunikacji z użytkownikiem.
- Celery obsługuje zadania asynchroniczne takie jak tworzenie skróconych URL-i.
- PostgreSQL pełni rolę głównej bazy danych, a Redis jest używany jako broker do Celery.

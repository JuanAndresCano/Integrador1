FROM python:3.10.12
ENV PYTHONNONBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y netcat-openbsd

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /code/

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
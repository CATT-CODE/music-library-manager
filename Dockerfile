FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "run.py"]

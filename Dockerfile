FROM python:3.8
# RUN apk add --no-cache --update python3 py3-pip bash

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 5000

# RUN adduser -D myuser
# USER myuser

CMD gunicorn --bind 0.0.0.0:$PORT app

# CMD ["python", "app.py"]
FROM python:3.12.1

RUN apt-get update && \
    apt-get install -y default-jdk
        

WORKDIR /Vor-kio

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

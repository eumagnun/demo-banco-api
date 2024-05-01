FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

CMD ["python", "demo-banco.py", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080


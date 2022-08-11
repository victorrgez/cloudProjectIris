FROM python:3

ADD . .

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8080

CMD ["python3", "main.py"]
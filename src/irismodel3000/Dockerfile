FROM python:3

ADD . .

RUN pip3 install -r requirements.txt --no-cache-dir
RUN mkdir -p src/irismodel3000 && mv *.py src/irismodel3000 && mv iris.h5 src/irismodel3000

EXPOSE 3000

CMD ["python3", "src/irismodel3000/main.py"]

FROM python:3.6-alpine
ADD . /code
WORKDIR /code
ENV http_proxy http://10.0.2.2:3128
ENV https_proxy https://10.0.2.2:3128
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

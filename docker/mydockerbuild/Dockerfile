FROM docker/whalesay:latest

ENV http_proxy http://10.0.2.2:3128
ENV https_proxy https://10.0.2.2:3128

RUN apt-get -y update && apt-get install -y fortunes

CMD /usr/games/fortune -a | cowsay

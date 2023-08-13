FROM ubuntu:22.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y nginx \
    git 

RUN git clone https://github.com/jordanistan/iamjordanrobison

COPY . /var/www/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
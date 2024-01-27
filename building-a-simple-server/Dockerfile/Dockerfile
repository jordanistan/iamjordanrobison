FROM golang:alpine AS build-env

WORKDIR /go/src/github.com/iamjordanrobison/building-a-web-server

COPY . .

RUN go build -o main

FROM alpine:3.18.6

RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk*

WORKDIR /go/src/github.com/iamjordanrobison/building-a-web-server

COPY --from=build-env /go/src/github.com/iamjordanrobison/building-a-web-server/* /go/src/github.com/iamjordanrobison/building-a-web-server

EXPOSE 8080

ENTRYPOINT [ "./main" ]
FROM golang:alpine AS build-env

WORKDIR /go/src/github.com/iamjordanrobison/building-a-web-server

COPY . .

RUN go build -o main

FROM alpine:3.23.6@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0

RUN apk add --no-cache ca-certificates

WORKDIR /go/src/github.com/iamjordanrobison/building-a-web-server

COPY --from=build-env /go/src/github.com/iamjordanrobison/building-a-web-server/* /go/src/github.com/iamjordanrobison/building-a-web-server

EXPOSE 8080

ENTRYPOINT [ "./main" ]

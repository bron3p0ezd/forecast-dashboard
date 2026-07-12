FROM node:22-alpine AS builder
WORKDIR /frontend

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_BACKEND_URL

ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

RUN npm run build

FROM alpine:3.20
WORKDIR /out

COPY --from=builder /frontend/dist /dist

CMD ["sh", "-c", "cp -r /dist/* /out/"]

FROM nginx:alpine

RUN apk add --no-cache curl \
  && rm -f /etc/nginx/conf.d/default.conf \
  && mkdir -p /web-server/logs

COPY nginx/nginx.conf /etc/nginx/
COPY nginx/conf.d/ /etc/nginx/conf.d/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:7777/health || exit 1

CMD ["nginx", "-g", "daemon off;"]

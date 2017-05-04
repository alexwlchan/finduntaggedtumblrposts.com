# We need Python 3.6, which is only available for Edge right now.
FROM alpine:edge

LABEL maintainer "Alex Chan alex@alexwlchan.net"
LABEL version="3.0"
LABEL description="An application for finding untagged posts on Tumblr"

# Install base dependencies
RUN apk update && \
    apk add nginx supervisor python3 uwsgi uwsgi-python3 && \
    rm -rf /var/lib/apk

# NGINX config: don't run as a daemonised process.  If it were to run as
# a daemon, supervisor would think it had died immediately.
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /run/nginx

# Install Python requirements
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

EXPOSE 80

RUN adduser -D -u 501 celery

# Copy in files right at the end.  These are the most likely to change,
# but they're also fairly fast.
COPY nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY config.py /config.py
COPY untagged /untagged

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

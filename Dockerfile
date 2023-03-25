FROM python:3.7.9-alpine

LABEL maintainer="foo@bar.com"
ARG TZ='Asia/Shanghai'

ARG CHATGPT_ON_WECHAT_VER

ENV BUILD_PREFIX=/app \
    BUILD_OPEN_AI_API_KEY='YOUR OPEN AI KEY HERE'

COPY chatgpt-on-wechat.tar.gz ./chatgpt-on-wechat.tar.gz

RUN apk add --no-cache \
        bash \
    && tar -xf chatgpt-on-wechat.tar.gz \
    && mv chatgpt-on-wechat ${BUILD_PREFIX} \
    && cd ${BUILD_PREFIX} \
    && cp config-template.json ${BUILD_PREFIX}/config.json \
    && sed -i "2s/YOUR API KEY/${BUILD_OPEN_AI_API_KEY}/" ${BUILD_PREFIX}/config.json \
    && /usr/local/bin/python -m pip install --no-cache --upgrade pip \
    && pip install --no-cache   \
        itchat-uos==1.5.0.dev0  \
        openai

WORKDIR ${BUILD_PREFIX}

ADD ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && adduser -D -h /home/noroot -u 1000 -s /bin/bash noroot \
    && chown noroot:noroot ${BUILD_PREFIX}

USER noroot

ENTRYPOINT ["/entrypoint.sh"]

FROM python:3.13-bookworm

ARG TARGETARCH
# Fallback to amd64 if TARGETARCH is not set or empty
ENV ARCH=${TARGETARCH:-amd64}

WORKDIR /usr/app

COPY ./backend/energy_efficiency_scorecard.py /usr/app/energy-service/
COPY ./backend/pyproject.toml /usr/app/energy-service/

RUN apt-get update \
    && apt-get install -y wget \
    && wget -O /usr/app/gg.deb "https://github.com/grft-dev/graftcode-gateway/releases/latest/download/gg_linux_${ARCH}.deb" \
    && dpkg -i /usr/app/gg.deb \
    && rm /usr/app/gg.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80
EXPOSE 81

CMD ["gg", "--modules", "./energy-service/"]

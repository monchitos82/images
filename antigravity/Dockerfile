FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install system prerequisites, compilers, build tools, runtimes, Java 25, and utilities
RUN apt update && apt dist-upgrade -y && apt install -y \
    build-essential \
    ca-certificates \
    cargo \
    chromium \
    cmake \
    curl \
    gcc \
    git \
    golang-go \
    meson \
    ninja-build \
    nodejs \
    npm \
    podman \
    prometheus-node-exporter \
    python3 \
    python3-pip \
    python3-venv \
    screen \
    ssh \
    traceroute \
    tree \
    vim \
    wget

# Install Java JDK 25 (Eclipse Temurin OpenJDK build)
RUN mkdir -p /opt/java && \
    wget -O /tmp/openjdk.tar.gz https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25%2B36/OpenJDK25U-jdk_x64_linux_hotspot_25_36.tar.gz && \
    tar -xzf /tmp/openjdk.tar.gz -C /opt/java --strip-components=1 && \
    rm /tmp/openjdk.tar.gz

# Set global environment variables
ENV JAVA_HOME=/opt/java
ENV PATH="/usr/local/bin:/opt/java/bin:${PATH}"
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV CHROME_PATH=/usr/bin/chromium

# 2. Install 'uv' globally
RUN wget -qO- https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz \
    | tar -xz -C /usr/local/bin/ --strip-components=1

# 3. Install VS Code in the browser (code-server) globally
RUN curl -fsSL https://code-server.dev/install.sh | sh

# 4. Install the Antigravity CLI (agy) and make it globally available
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash && \
    if [ -f /root/.local/bin/agy ]; then mv /root/.local/bin/agy /usr/local/bin/agy; fi && \
    chmod +x /usr/local/bin/agy

# 5. Create the 'antigravity' non-root user and set up permissions
RUN useradd -ms /bin/bash antigravity && \
    mkdir /home/antigravity/local && \
    chown antigravity:antigravity /home/antigravity/local

# 6. Create an entrypoint script to run background services and hand off to agy as the user
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo '/usr/sbin/node_exporter &> /tmp/node_exporter.log &' >> /entrypoint.sh && \
    echo 'exec code-server --bind-addr 0.0.0.0:8099 --auth none' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Switch to the non-root antigravity user
USER antigravity
WORKDIR /home/antigravity

# Expose ports: 9100 (Prometheus), 8099 (Code-Server IDE)
EXPOSE 9100 8099

ENTRYPOINT ["/entrypoint.sh"]

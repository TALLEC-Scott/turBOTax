FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install qwen CLI
RUN npm install -g @anthropic-ai/claude-code @qwen-code/qwen-code

# Create directories
RUN mkdir -p /app/docs /app/vault /app/logs

# Copy scripts
COPY scripts/*.sh /app/scripts/
RUN chmod +x /app/scripts/*.sh

# Set working directory
WORKDIR /app

# Default command
CMD ["bash"]

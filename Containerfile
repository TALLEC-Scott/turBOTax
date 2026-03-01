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

# Set working directory first
WORKDIR /app

# Copy project files for dependency resolution
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen || uv sync

# Create directories
RUN mkdir -p docs vault logs scripts

# Copy scripts
COPY scripts/*.sh scripts/
COPY scripts/*.py scripts/
RUN chmod +x scripts/*.sh

# Default command
CMD ["bash"]

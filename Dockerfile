FROM python:3.13-slim

WORKDIR /app
COPY . /app



# Install uv
RUN pip install --no-cache-dir uv

# Sync uv environment
RUN uv sync
RUN uv run playwright install chromium --with-deps



ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/

CMD ["uv", "run", "run_bot_once.py"]
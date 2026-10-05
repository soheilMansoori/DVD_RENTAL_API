FROM python:3.14.3-alpine AS builder

# install uv first
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# set UV configs for better performance in docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# copy packages names
COPY pyproject.toml ./

# install python packages
RUN uv sync --frozen --no-install-project

# add python as runner
FROM python:3.14.3-alpine AS runner

# add packages
RUN apk add --no-cache libpq

WORKDIR /app

# copy .venv
COPY --from=builder /app/.venv /app/.venv

# and .venv path
ENV PATH="/app/.venv/bin:$PATH"

# copy sourse code
COPY . .

# create user for securety
RUN addgroup -S appuser && adduser -S appuser -G appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

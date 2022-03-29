FROM python:3.10-alpine

COPY . .
RUN pip install --no-cache-dir . && \
    rm -r coverage_gh* Dockerfile MANIFEST.in pyproject.toml setup.cfg

ENTRYPOINT ["python", "-m", "coverage_gh"]

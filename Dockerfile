FROM python:3.10-alpine

LABEL "com.github.actions.name"="Integrate Python coverage & GitHub Actions"
LABEL "com.github.actions.description"="Add a check and annotations on a GitHub PR based on Python coverage results."
LABEL "com.github.actions.icon"="shield"
LABEL "com.github.actions.color"="yellow"
LABEL "com.github.actions.repository"="https://github.com/khaeru/coverage-dh"
LABEL "com.github.actions.homepage"="https://github.com/khaeru/coverage-dh"
LABEL "com.github.actions.maintainer"="Paul Natsuo Kishimoto"

COPY . .
RUN pip install --no-cache-dir . && \
    rm -r coverage_gh* Dockerfile MANIFEST.in pyproject.toml setup.cfg

ENTRYPOINT ["python", "-m", "coverage_gh"]

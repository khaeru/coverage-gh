FROM python:3.10-alpine

LABEL "com.github.actions.name"="Integrate Python coverage & GitHub Actions"
LABEL "com.github.actions.description"="Add a check and annotations on a GitHub PR based on Python coverage results."
LABEL "com.github.actions.icon"="shield"
LABEL "com.github.actions.color"="yellow"
LABEL "com.github.actions.repository"="https://github.com/khaeru/coverage-dh"
LABEL "com.github.actions.homepage"="https://github.com/khaeru/coverage-dh"
LABEL "com.github.actions.maintainer"="Paul Natsuo Kishimoto"

WORKDIR /coverage-gh
COPY coverage_gh pyproject.toml setup.cfg .
RUN pip install .

ENTRYPOINT ["python", "-m" "coverage_gh"]

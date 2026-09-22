# wordfreq-bench, hardened build. The grader and the oracle solution never enter this image:
# grading happens outside, after the agent exits (see grade.sh).
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --uid 1001 --shell /bin/bash agent
# exported tree only: no .git, so no history to mine
COPY --chown=agent:agent app /app
WORKDIR /app
USER agent
CMD ["sleep", "infinity"]

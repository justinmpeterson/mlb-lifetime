FROM python:3.7-alpine

ARG MSF_FANTASY_DRAFT_ORDER
ARG MSF_FANTASY_DRAFT_ROUNDS
ARG MSF_FANTASY_DRAFT_SNAKE
ARG MSF_FANTASY_LEAGUE
ARG MSF_FANTASY_OWNERS
ARG MSF_RESPONSE_FORMAT
ARG MSF_SEASON
ARG MSF_SEASON_TYPE
ARG MSF_VERSION
ARG SSH_PRIVATE_KEY

ENV MSF_API_KEY
ENV MSF_FANTASY_DRAFT_ORDER ${MSF_FANTASY_DRAFT_ORDER}
ENV MSF_FANTASY_DRAFT_ROUNDS ${MSF_FANTASY_DRAFT_ROUNDS}
ENV MSF_FANTASY_DRAFT_SNAKE ${MSF_FANTASY_DRAFT_SNAKE}
ENV MSF_FANTASY_LEAGUE ${MSF_FANTASY_LEAGUE}
ENV MSF_FANTASY_OWNERS ${MSF_FANTASY_OWNERS}
ENV MSF_PASSWORD
ENV MSF_RESPONSE_FORMAT ${MSF_RESPONSE_FORMAT}
ENV MSF_SEASON ${MSF_SEASON}
ENV MSF_SEASON_TYPE ${MSF_SEASON_TYPE}
ENV MSF_VERSION ${MSF_VERSION}
ENV PYTHONUNBUFFERED 1
ENV SSH_PRIVATE_KEY ${SSH_PRIVATE_KEY}

RUN apk add --update --no-cache openssh-client

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN mkdir data lib output results scripts src
RUN mkdir data/drafts data/seasons
RUN mkdir output/wwwhtml

COPY ./data/drafts/*.txt ./data/drafts/
COPY ./data/team_owners.json ./data/
COPY ./scripts/grab_html_output.sh ./scripts/
COPY ./src/ ./src/
COPY ./lib/ ./lib/
COPY ./__init__.py .
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid=2000 --system jedi
RUN adduser --ingroup jedi --system --disabled-password --uid 2001 luke
RUN chown -R luke:jedi /usr/src/app
USER luke
RUN mkdir -p ~/.ssh
RUN ssh-keyscan -H tilde.team >> ~/.ssh/known_hosts
RUN echo -e "${SSH_PRIVATE_KEY}\n" > ~/.ssh/tilde.team
RUN chmod 0400 ~/.ssh/tilde.team

RUN python -m src.mvp --run-type=draft --season=${MSF_SEASON} --season-type=${MSF_SEASON_TYPE}
RUN python -m src.mvp --run-type=season --season=${MSF_SEASON} --season-type=${MSF_SEASON_TYPE}

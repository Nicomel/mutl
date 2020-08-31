# MUTL
Multi-user prioritized task list

# Local environment

## Local Build Prerequisites

- Anaconda installed
- Docker installed

## Local build instructions for development environment

Install the dependencies (linux):

- `conda env create -n mutl -f env.yml`
- `source activate mutl`
- `pip install -r requirements.txt`

## Run the unit tests

At project root level:

- `py.test -v`

## Local run instructions

At project root level:

- Run the application server: `uvicorn app.main:app --reload`

Connect to : <http://localhost:8080/docs#/>.

# Docker

## Docker build instructions

`docker build -t perso/mutl . --rm`

## Docker run instructions

- Run one of the application service: 
    - `docker-compose up mutl`
- Connect to : <http://localhost:8080/docs#/>.
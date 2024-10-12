# Details App

## This branch is for creating a docker image, to be used in this project(helm): https://github.com/lavishay-technion/K3S_details_app.git

Applications that can store your personal details and list all the written users on html

### Requirements:

- Python: 3.11
- SQLite3
- Bash Shell
- Docker
    - Postgresql container needed
- Docker compose for multi container environment


### Install

- Run docker compose up -d
- Access the API on localhost port 8000


### Notes
- All data is stored in "Contacts" table in postgresql

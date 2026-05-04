# Docker Compose with Python, React, and Postgres
First I wanted to parse some data with Python, then I wanted to insert it into a Postgres database, which then lead to me messing with Docker Compose, and then I added on some React to give it a user interface.

## Windows Instructions:
1. Make a local clone of this repository via your preferred method.

2. Start the Docker Engine.  If you don't already have something that can do that, I've been using Docker Desktop, which you can get here:  https://www.docker.com/products/docker-desktop/

3. Open a command terminal from inside the repository's base directory and execute the command:

       docker compose build

4. Then execute:

       docker compose up -d
	   
5. If you want to, you can now check the backend's logs from within Docker Desktop to verify that Python connected to Postgres.

# PostgreSQL UI with Docker Compose, Flask, and React
I wanted to tinker with PostgreSQL, so I decided to use Docker Compose to get a simple Flask backend interfacing with a PostgreSQL container.  Then I added in a simple React frontend so that I could dynamically execute queries.  It's a fairly rudimentary tool, but in the process of getting it all working I learned a great deal about debugging and orchestrating multi-container applications.

## Windows Instructions:
1. Make a local clone of this repository via your preferred method.

2. Start the Docker Engine.  If you don't already have something that can do that, I've been using [`Docker Desktop`](https://www.docker.com/products/docker-desktop/).

3. Open a command terminal from inside the repository's base directory and execute the command:

       docker compose build

4. Then execute:

       docker compose watch
	   
5. Open your local web browser to `http://localhost:5173/`.

6. The interface allows you to write and execute one [`PostgreSQL`](https://www.postgresql.org/about/) statement at a time.  Several database tables are preloaded with some simple statistical data each time the program is run, in case you'd like to play around with that.

7. When you're ready to close it down, press CTRL+C in the command terminal, then execute the following command:

		docker compose down

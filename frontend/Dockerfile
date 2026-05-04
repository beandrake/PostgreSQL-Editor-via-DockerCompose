# =========================================
# Stage: Development (Vite React.js App)
# =========================================

# Set base image (host OS)
ARG NODE_VERSION=24.14.0-alpine
 
FROM node:${NODE_VERSION} AS devbuild

# Set the working directory in the container.
WORKDIR /app

# Copy dependencies file to the working directory.
COPY package*.json ./

# Install dependencies.
RUN npm install

# Copy local content to the container's working directory (except dockerignore)
COPY . .

# Ensure the built-in "node" user owns the application files
RUN chown -R node:node /app
 
# Switch to the built-in non-root "node" user
USER node

# Expose the port React frontend runs on
EXPOSE 5173

# Run this command, which starts the Vite development server.
#	Last 3 arguments make it accessible on all network interfaces
#		(i.e. - outside the container)
CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0" ]
# Use official Node.js image
FROM node:24-alpine AS build

# Accept build argument for API URL
# Note that VITE reads this at container build time, not run time
# hence passing this as an environment variable at runtime doesn't work
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the app
RUN npm run build

# Stage 2: Serve the app with a static server
FROM node:24-alpine AS serve

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy build output from previous stage
COPY --from=build /app/dist ./dist

# Expose port
EXPOSE 5173

# Start the SPA with fallback to index.html
CMD ["serve", "-s", "dist", "-l", "5173"]
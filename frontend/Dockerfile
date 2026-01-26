FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY frontend/public ./public
COPY frontend/src ./src

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]

# Build Stage
FROM node:22-alpine AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Final stage - just keep the build artifacts
FROM alpine:latest
WORKDIR /app
COPY --from=build-stage /app/dist /app/dist
CMD ["sleep", "infinity"]

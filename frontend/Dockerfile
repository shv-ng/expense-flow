# Stage 1: Build
FROM node:25.4-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx (Much smaller and faster for SPAs)
FROM nginx:alpine
# Copy the build output to nginx's serving directory
COPY --from=builder /app/dist /usr/share/nginx/html
# Expose port 80 (Standard for Nginx)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

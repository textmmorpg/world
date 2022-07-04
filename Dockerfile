FROM node:16
WORKDIR /app
# RUN printenv > .env
COPY . /app
RUN npm install
EXPOSE 3002
CMD node render/render.js

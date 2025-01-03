FROM node:16

WORKDIR /app

COPY . /app

RUN npm install

RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "build"]

EXPOSE 5000
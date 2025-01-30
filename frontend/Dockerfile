FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install react-router-dom && npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
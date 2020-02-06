FROM node

WORKDIR /code/frontend
COPY package.json /code/frontend

RUN npm install

EXPOSE 3000
CMD ["npm", "start"]
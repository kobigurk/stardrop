# specify the node base image with your desired version node:<version>
FROM node:16

RUN mkdir ./appFront

WORKDIR ./appFront

ADD ./package.json .

RUN mkdir public
ADD ./public ./public/

RUN mkdir src
ADD ./src ./src

RUN npm install

EXPOSE 3000
EXPOSE 5000
EXPOSE 5000

CMD npm start

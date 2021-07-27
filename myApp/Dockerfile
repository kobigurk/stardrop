# specify the node base image with your desired version node:<version>
FROM node:16

RUN mkdir ./appFront

WORKDIR ./appFront

ADD ./package.json .
ADD ./package-lock.json .
ADD ./yarn.lock .

RUN mkdir public
ADD ./public ./public/

RUN mkdir src
ADD ./src ./src

RUN yarn

EXPOSE 3000

CMD npm start

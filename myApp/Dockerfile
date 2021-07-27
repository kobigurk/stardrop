# specify the node base image with your desired version node:<version>
FROM node:16

ADD . /appFront

WORKDIR ./appFront

EXPOSE 3000

CMD yarn && yarn start

# specify the node base image with your desired version node:<version>
FROM node:16

WORKDIR ./appFront

EXPOSE 3000

CMD yarn install --frozen-lockfile  && yarn start

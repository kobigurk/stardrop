FROM python:3

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y libgmp-dev nodejs npm
RUN pip3 install ecdsa fastecdsa sympy contextvars flask flask_cors 

WORKDIR /server
ADD src/cairo-lang-0.4.0.zip /server

RUN npm install ethers
RUN pip3 install cairo-lang-0.4.0.zip

EXPOSE 5000

CMD python3 server.py

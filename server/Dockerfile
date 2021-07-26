FROM python:3

RUN apt-get update
RUN apt-get upgrade -y
RUN mkdir server

WORKDIR server
RUN mkdir contract
RUN mkdir proof_of_humanity
RUN mkdir src
RUN mkdir __pycache__
RUN mkdir signGestion


RUN apt-get install -y libgmp-dev nodejs npm
RUN npm install ethers axios fs
RUN pip3 install ecdsa fastecdsa sympy
ADD db.py end_commitment_phase.py end_vote_phase.py generate_vote_data.py server.py submit_key.py utils.py sign_token.py generate_keypair.py ./
ADD contract contract/
ADD proof_of_humanity proof_of_humanity/
ADD __pycache__ __pycache__/
ADD signGestion signGestion/
ADD src src/
RUN pip3 install src/cairo-lang-0.3.0.zip
RUN pip3 install contextvars
RUN pip install flask flask_cors

EXPOSE 5000

CMD python3 server.py ; ../bin/bash 

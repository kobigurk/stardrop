FROM python:3

RUN apt-get update
RUN apt-get upgrade -y
RUN mkdir local

WORKDIR local
RUN mkdir contract  
ADD blind.py commit.py Dockerfile local.py utils.py cairo-lang-0.3.0.zip generate_keypair.py unblind.py ./
ADD contract/contract_abi.json  contract/contract.cairo contract/contract_compiled.json contract/
RUN pip3 install contextvars
RUN pip install flask flask_cors
RUN pip3 install cairo-lang-0.3.0.zip
EXPOSE 4242

CMD python3 local.py  

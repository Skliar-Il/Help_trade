FROM python:3.12

RUN mkdir /bot_for_help_trade

WORKDIR /bot_for_help_trade

COPY req.txt .

RUN pip install -r req.txt 

COPY . . 

ENV PATH=/root/.local:$PATH

WORKDIR src

CMD python -u main.py


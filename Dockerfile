FROM python:3.10

RUN pip install update

RUN pip install requests

WORKDIR /root

COPY download_data.py /root/download_data.py
COPY graphic_of_historic_prices.py /root/graphic_of_historic_prices.py
COPY make_graphics.py /root/make_graphics.py
COPY update_csv.py /root/update_csv.py
COPY version.txt /root/version.txt
COPY Results /root/Results
COPY Data /root/Data
COPY Cronjobs /root/Cronjobs

EXPOSE 8000
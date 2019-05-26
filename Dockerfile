FROM ubuntu:16.04

COPY requirements.txt /code/requirements.txt

WORKDIR /code

RUN apt-get update
RUN apt-get install -y zbar-tools libzbar-dev python-zbar
RUN dpkg -L libzbar-dev; ls -l /usr/include/zbar.h
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN pip3 install -r requirements.txt

COPY . /code

CMD ["gunicorn", "app:app"]

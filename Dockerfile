FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y binutils libproj-dev gdal-bin
WORKDIR /django

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8011
CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8011











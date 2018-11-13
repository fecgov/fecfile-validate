FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/fecfile_validate
WORKDIR /opt/fecfile_validate
ADD . /opt/fecfile_validate
RUN pip3 install -r requirements.txt

EXPOSE 8085
CMD gunicorn FEC_validate.wsgi -b 8085

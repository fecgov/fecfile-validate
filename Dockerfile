FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/fecfile_validate
WORKDIR /opt/fecfile_validate
ADD . /opt/fecfile_validate
RUN pip3 install -r requirements.txt

#EXPOSE 8001
#CMD python manage.py runserver 0.0.0.0:8001

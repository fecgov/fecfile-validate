FROM python:3.6

# Ensure python output is sent unbuffered straight to the terminal so output
# is seen in real time.
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/fecfile_validate
WORKDIR /opt/fecfile_validate
ADD . /opt/fecfile_validate
RUN pip3 install -r requirements.txt

EXPOSE 8001

# Serve flask app using the gunicorn WSGI HTTP server
# See: https://gunicorn.org/
ENTRYPOINT ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8001", "run:app"]

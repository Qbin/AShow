FROM bbq/ashow_base:v1.0

COPY . /opt
WORKDIR /opt
CMD ["gunicorn", "-b", "0.0.0.0:80", "--timeout", "600", "server:app"]

EXPOSE 80
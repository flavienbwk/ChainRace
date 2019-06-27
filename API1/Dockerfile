FROM python:3.6

#RUN ["mkdir", "app"]
WORKDIR "app"

COPY "requirements.txt" .
RUN ["pip", "install", "-r", "requirements.txt"]

COPY "app.py" .
COPY "run.sh" .
COPY "build.ipynb" .
COPY "health-check-data.csv" .

ENV FLASH_APP app.py
RUN ["chmod", "+x", "./run.sh"]
EXPOSE 8080
ENTRYPOINT [ "./run.sh" ]
CMD [ "train" ]
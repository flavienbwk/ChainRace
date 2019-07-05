FROM python:3.6

#RUN ["mkdir", "app"]
WORKDIR "app"

COPY "requirements.txt" .
RUN ["pip", "install", "-r", "requirements.txt"]

COPY "app.py" .
COPY "run.sh" .
COPY "build.ipynb" .
COPY "health-check-data.csv" .
COPY "send.py" .

ENV FLASH_APP app.py
RUN ["chmod", "+x", "./run.sh"]
EXPOSE 8080
ENTRYPOINT [ "./run.sh" ]
RUN ["python", "send.py"]
CMD [ "train" ] 

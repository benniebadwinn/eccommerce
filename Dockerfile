# pull official base image
#FROM python:3.10-slim-buster

# set work directory
#WORKDIR /app

# install dependencies
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt

# copy project
#COPY . .

#CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
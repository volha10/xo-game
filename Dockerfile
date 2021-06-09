FROM python:3.8.8-buster

WORKDIR /code

ENV FLASK_APP=manage.py
ENV FLASK_RUN_HOST=0.0.0.0
#RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Copy project.
COPY . .

#CMD ["python", "./manage.py"]



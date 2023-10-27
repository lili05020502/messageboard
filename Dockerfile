FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install python-dotenv
EXPOSE 3333
CMD ["python", "app.py"]

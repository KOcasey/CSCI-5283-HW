FROM python:3.9



# choose the directory to use for everything that follows
WORKDIR /app

COPY pipeline.py pipeline.py

RUN pip install pandas sqlalchemy psycopg2 scikit-learn

ENTRYPOINT ["python", "pipeline.py"]
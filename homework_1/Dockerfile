FROM python:3.9

RUN pip install pandas

# choose the directory to use for everything that follows
WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
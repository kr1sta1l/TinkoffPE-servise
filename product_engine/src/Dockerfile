FROM python:3.10
LABEL authors="kr1sta1l"

WORKDIR /app

COPY . /app
# ! add requirements.txt to thif directory because COPY can't copy files from parent directory
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


# to build the image:
# docker build -t product_engine .

# to run the image:
# sudo docker run --network="fintech-network" -d -p 8000:8000 product_engine
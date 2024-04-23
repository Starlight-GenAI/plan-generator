FROM --platform=linux/amd64 python:3.12

WORKDIR /usr/src

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "--app-dir", "/usr/src" ,"main:app", "--host", "0.0.0.0", "--port", "8080"]
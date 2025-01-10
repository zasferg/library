FROM python:3.12-slim

WORKDIR /test_library

COPY requirements.txt /test_library/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src /test_library/src
#COPY .env /test_library/.env

ENV PYTHONPATH="${PYTHONPATH}:/test_library/src"
EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

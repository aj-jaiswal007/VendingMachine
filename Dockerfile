# Using python  3.9 Image
FROM python:3.9

# This is our working directory
WORKDIR /code

# requirements.txt are in our working directly
COPY ./requirements.txt /code/requirements.txt

# installing requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copiyfing our code
COPY ./alembic /code/alembic
COPY ./vendingmachine /code/vendingmachine

# Change the working directory to /code
WORKDIR /code

# running server
CMD ["uvicorn", "vendingmachine.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]

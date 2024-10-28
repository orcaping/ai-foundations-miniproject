FROM python:3.12-slim

RUN pip install pipenv

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app

COPY requirements.txt requirements.txt
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]

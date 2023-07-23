FROM python:3.11

# create and set working directory
RUN mkdir -p /app
WORKDIR /app

# copy requirements file
COPY requirements.txt /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the rest of the files
COPY . /app

# run the bot
CMD ["python3", "bot.py"]


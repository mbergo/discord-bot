# Use an official Python runtime as the base image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Set the environment variables for Discord bot token and OpenAI API key
ENV DISCORD_TOKEN=<discord_token>
ENV API_KEY=<api_key>

# Set the default command to run the script
CMD ["python", "tests.py", "$DISCORD_TOKEN", "$API_KEY"]

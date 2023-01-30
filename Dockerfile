FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN cd tests && pip install -r requirements.txt

ENV DISCORD_TOKEN=${{ env.DISCORD_TOKEN }}
ENV API_KEY=${{ env.API_KEY }}
ENV AUTH_KEY=${{ env.AUTH_KEY }}
ENV FROM_NUMBER=${{ env.FROM_NUMBER }}

CMD ["python", "test_bot.py", "$DISCORD_TOKEN", "$API_KEY", "$AUTH_KEY", "$FROM_NUMBER"]

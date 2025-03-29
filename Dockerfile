FROM python:3.11-slim-buster
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "python3 -m ubb & python3 /app/server.py"]

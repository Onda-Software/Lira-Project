FROM python:3.11.8

ENV TERM xterm

WORKDIR /home/viper/Desktop/LUNA/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "src/ServerSocket.py" ]

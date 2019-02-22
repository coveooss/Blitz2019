FROM python:3.7.1

COPY local_runner/run.sh run.sh

COPY __main__.py __main__.py
COPY requirements.txt requirements.txt
COPY game/ game/

COPY local_runner/bot_1/ bot_1/
COPY local_runner/bot_2/ bot_2/

RUN pip install -r requirements.txt
RUN pip install pyinstaller

RUN pyinstaller __main__.py --onefile --name game_executable --distpath .
RUN pyinstaller bot_1/MyBot.py --onefile --name bot_1_executable --distpath .
RUN pyinstaller bot_2/MyBot.py --onefile --name bot_2_executable --distpath .

RUN rm __main__.py
RUN rm -r game/
RUN rm -r bot_1/
RUN rm -r bot_2/

ENTRYPOINT [ "bash", "./run.sh" ]
#!/bin/bash

BOTS=() 
PORT=5000

for var in "$@"
do
    if [ $var = "BOT1" ]; then
        echo "Starting BOT1 on port $PORT ..."
        BOTS=("${BOTS[@]}" "http://localhost:"$PORT)
        ./bot_1_executable -p $PORT &
        PORT=$((PORT+1))
        continue
    fi

    if [ $var = "BOT2" ]; then
        echo "Starting BOT2 on port $PORT ..."
        BOTS=("${BOTS[@]}" "http://localhost:"$PORT)
        ./bot_2_executable -p $PORT &
        PORT=$((PORT+1))
        continue
    fi

    BOTS=("${BOTS[@]}" "$var")
done

sleep 2

echo "Starting game server with ${BOTS[@]}"
./game_executable --no-gui ${BOTS[@]}
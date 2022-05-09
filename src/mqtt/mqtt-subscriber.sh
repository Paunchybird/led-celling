#!/bin/bash

ROUTE="/opt/mypanel-conf"

SERVER=`cat $ROUTE/my-mqtt.json | jq '.server' -r`
PORT=`cat $ROUTE/my-mqtt.json | jq '.port' -r`
TOPIC=`cat $ROUTE/my-mqtt.json | jq '.topic' -r`
DEVICENAME=`cat $ROUTE/my-mqtt.json | jq '.devicename' -r`
USERNAME=`cat $ROUTE/my-mqtt.json | jq '.username' -r`
PASSWORD=`cat $ROUTE/my-mqtt.json | jq '.password' -r`
CLIENTID=`cat $ROUTE/my-mqtt.json | jq '.clientid' -r`
LOCATION=`cat $ROUTE/my-mqtt.json | jq '.location' -r`

ROUTE="/opt/led-matrix/bindings/python" 
echo "Listening to topic: " "$TOPIC/$DEVICENAME"
while read rawcmd;
do

    echo "Message recived: $rawcmd"
    data=(${rawcmd// + / })
    echo "${data[0]}.py" #Program
    echo "${data[1]}"    #Image
    echo "${data[2]%.*}"    #Rotation
    echo "${data[3]}"    #Speed
    echo "${data[4]}"    #Text
    pkill python
    
    
    ICONS="/opt/mypanel-icons/"
    case "${data[0]}.py" in
      Image-Blinking.py | Image-Scroller-Horizontal.py | Image-Scroller-Vertical.py)
        TMP="$ROUTE/${data[0]}.py -i $ICONS${data[1]} -R ${data[2]%.*} -s ${data[3]} " 
        $TMP > /dev/null 2>&1 &
        ;;

      Image-Display.py)
        TMP="$ROUTE/${data[0]}.py  -i $ICONS${data[1]} -R ${data[2]%.*}" 
        $TMP > /dev/null 2>&1 &
        ;;

      Runtext.py)
        TMP="$ROUTE/${data[0]}.py  -t  ${data[4]}" 
        $TMP > /dev/null 2>&1 &
        ;;
      
      Weather.py)
        TMP="$ROUTE/${data[0]}.py -L $LOCATION" 
        $TMP > /dev/null 2>&1 &
        ;;
      Clock.py)
        "$ROUTE/${data[0]}.py" > /dev/null 2>&1 &
        ;;
      *)
        echo -n "unknown"
        ;;
    esac
done < <(mosquitto_sub -h $SERVER -p $PORT -u "$USERNAME" -P "$PASSWORD" -i $CLIENTID -t "$TOPIC/$DEVICENAME" -q 1)

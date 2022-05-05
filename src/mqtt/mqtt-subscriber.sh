#!/bin/bash

ROUTE="/opt/mypanel-conf"

MQTT_SERVER=`cat $ROUTE/my-mqtt.json | jq '.server' -r`
MQTT_PORT=`cat $ROUTE/my-mqtt.json | jq '.port' -r`
MQTT_TOPIC=`cat $ROUTE/my-mqtt.json | jq '.topic' -r`
MQTT_DEVICENAME=`cat $ROUTE/my-mqtt.json | jq '.devicename' -r`
MQTT_USERNAME=`cat $ROUTE/my-mqtt.json | jq '.username' -r`
MQTT_PASSWORD=`cat $ROUTE/my-mqtt.json | jq '.password' -r`
MQTT_CLIENTID=`cat $ROUTE/my-mqtt.json | jq '.clientid' -r`

ROUTE="/opt/led-matrix/bindings/python" 
echo "Listening to topic: " "$MQTT_TOPIC/$MQTT_DEVICENAME"
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
        TMP="$ROUTE/${data[0]}.py  -i $ICONS${data[1]}" 
        $TMP > /dev/null 2>&1 &
        ;;

      Runtext.py)
        TMP="$ROUTE/${data[0]}.py  -t  ${data[4]}" 
        $TMP > /dev/null 2>&1 &
        ;;
      
      Weather.py | Clock.py)
        "$ROUTE/${data[0]}.py" > /dev/null 2>&1 &
        ;;

      *)
        echo -n "unknown"
        ;;
    esac
done < <(mosquitto_sub -h $MQTT_SERVER -p $MQTT_PORT -u "$MQTT_USERNAME" -P "$MQTT_PASSWORD" -i $MQTT_CLIENTID -t "$MQTT_TOPIC/$MQTT_DEVICENAME" -q 1)

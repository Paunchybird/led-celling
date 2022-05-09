
#!/bin/bash
export TERM=xterm
ln -s /usr/bin/python3 /usr/bin/python
echo "Starting Container"
echo "Testing Matrix"

/opt/led-matrix/bindings/python/boot.py 

#Ejecutamos el proceso subscriber en el background
echo "Executing mqtt-subscriber.sh"
/opt/mqtt/mqtt-subscriber.sh 

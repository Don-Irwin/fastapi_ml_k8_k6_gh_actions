#!/bin/bash
cd /app/api_consumer
git pull
chmod -R 777 ./*.*
./rd.sh
#sleep 25
echo "**************************"
echo "**************************"
echo "*  ACCESS FLASK APP AT:  *"
echo "* http://127.0.0.1:5001  *"
echo "**************************"
echo "**************************"
#cd /app/api_consumer
#jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="" --NotebookApp.password="" --port=8888

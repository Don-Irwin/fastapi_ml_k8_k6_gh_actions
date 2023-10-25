
#!/bin/bash

echo "*********************************"
echo "*                               *"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "*********************************"

#export REDIS_SERVER=localhost
#echo $REDIS_SERVER

#return

good_return_codes=0
bad_return_codes=0

eval_return () {
  my_code="$1"
  

if [ "$my_code" == "200" ]; then
    let "good_return_codes = good_return_codes+1"
else
    let "bad_return_codes = bad_return_codes+1"
fi

}

echo "*********************************"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "* We are doing 200 iterations   *"
echo "*********************************"


for i in {1..200}

do
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984126984126984,"AveBedrms":1.0238095238095237,"Population":322.0,"AveOccup":2.5555555555555554,"Latitude":37.88,"Longitude":-122.23 },{"MedInc":8.3014,"HouseAge":21.0,"AveRooms":6.238137082601054,"AveBedrms":0.9718804920913884,"Population":2401.0,"AveOccup":2.109841827768014,"Latitude":37.86,"Longitude":-122.22 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":8.3014,"HouseAge":21.0,"AveRooms":6.238137082601054,"AveBedrms":0.9718804920913884,"Population":2401.0,"AveOccup":2.109841827768014,"Latitude":37.86,"Longitude":-122.22 },{"MedInc":3.6591,"HouseAge":52.0,"AveRooms":4.9319066147859925,"AveBedrms":0.9513618677042801,"Population":1094.0,"AveOccup":2.1284046692607004,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":7.2574,"HouseAge":52.0,"AveRooms":8.288135593220339,"AveBedrms":1.073446327683616,"Population":496.0,"AveOccup":2.8022598870056497,"Latitude":37.85,"Longitude":-122.24 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":4.0368,"HouseAge":52.0,"AveRooms":4.761658031088083,"AveBedrms":1.1036269430051813,"Population":413.0,"AveOccup":2.139896373056995,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.6591,"HouseAge":52.0,"AveRooms":4.9319066147859925,"AveBedrms":0.9513618677042801,"Population":1094.0,"AveOccup":2.1284046692607004,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.0804,"HouseAge":42.0,"AveRooms":4.294117647058823,"AveBedrms":1.1176470588235294,"Population":1206.0,"AveOccup":2.026890756302521,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.6912,"HouseAge":52.0,"AveRooms":4.970588235294118,"AveBedrms":0.9901960784313726,"Population":1551.0,"AveOccup":2.172268907563025,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.2031,"HouseAge":52.0,"AveRooms":5.477611940298507,"AveBedrms":1.0796019900497513,"Population":910.0,"AveOccup":2.263681592039801,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.2705,"HouseAge":52.0,"AveRooms":4.772479564032698,"AveBedrms":1.0245231607629428,"Population":1504.0,"AveOccup":2.0490463215258856,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.075,"HouseAge":52.0,"AveRooms":5.322649572649572,"AveBedrms":1.0128205128205128,"Population":1098.0,"AveOccup":2.3461538461538463,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":3.075,"HouseAge":52.0,"AveRooms":5.322649572649572,"AveBedrms":1.0128205128205128,"Population":1098.0,"AveOccup":2.3461538461538463,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6736,"HouseAge":52.0,"AveRooms":4.0,"AveBedrms":1.0977011494252873,"Population":345.0,"AveOccup":1.9827586206896552,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":2.6736,"HouseAge":52.0,"AveRooms":4.0,"AveBedrms":1.0977011494252873,"Population":345.0,"AveOccup":1.9827586206896552,"Latitude":37.84,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.9167,"HouseAge":52.0,"AveRooms":4.262903225806451,"AveBedrms":1.0096774193548388,"Population":1212.0,"AveOccup":1.9548387096774194,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":1.9167,"HouseAge":52.0,"AveRooms":4.262903225806451,"AveBedrms":1.0096774193548388,"Population":1212.0,"AveOccup":1.9548387096774194,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.125,"HouseAge":50.0,"AveRooms":4.242424242424242,"AveBedrms":1.071969696969697,"Population":697.0,"AveOccup":2.640151515151515,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":2.125,"HouseAge":50.0,"AveRooms":4.242424242424242,"AveBedrms":1.071969696969697,"Population":697.0,"AveOccup":2.640151515151515,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.775,"HouseAge":52.0,"AveRooms":5.9395770392749245,"AveBedrms":1.0483383685800605,"Population":793.0,"AveOccup":2.395770392749245,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":2.775,"HouseAge":52.0,"AveRooms":5.9395770392749245,"AveBedrms":1.0483383685800605,"Population":793.0,"AveOccup":2.395770392749245,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":2.1202,"HouseAge":52.0,"AveRooms":4.052805280528053,"AveBedrms":0.966996699669967,"Population":648.0,"AveOccup":2.1386138613861387,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.9911,"HouseAge":50.0,"AveRooms":5.343675417661098,"AveBedrms":1.0859188544152745,"Population":990.0,"AveOccup":2.3627684964200477,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":1.9911,"HouseAge":50.0,"AveRooms":5.343675417661098,"AveBedrms":1.0859188544152745,"Population":990.0,"AveOccup":2.3627684964200477,"Latitude":37.84,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6033,"HouseAge":52.0,"AveRooms":5.465454545454546,"AveBedrms":1.0836363636363637,"Population":690.0,"AveOccup":2.5090909090909093,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.6033,"HouseAge":52.0,"AveRooms":5.465454545454546,"AveBedrms":1.0836363636363637,"Population":690.0,"AveOccup":2.5090909090909093,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.725,"HouseAge":52.0,"AveRooms":5.096234309623431,"AveBedrms":1.1317991631799162,"Population":1015.0,"AveOccup":2.1234309623430963,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.1806,"HouseAge":52.0,"AveRooms":5.193846153846154,"AveBedrms":1.0369230769230768,"Population":853.0,"AveOccup":2.624615384615385,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.1806,"HouseAge":52.0,"AveRooms":5.193846153846154,"AveBedrms":1.0369230769230768,"Population":853.0,"AveOccup":2.624615384615385,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6,"HouseAge":52.0,"AveRooms":5.270142180094787,"AveBedrms":1.0355450236966826,"Population":1006.0,"AveOccup":2.3838862559241707,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.6,"HouseAge":52.0,"AveRooms":5.270142180094787,"AveBedrms":1.0355450236966826,"Population":1006.0,"AveOccup":2.3838862559241707,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"

done



echo "*********************************"
echo "* END OF GOOD 200 ZONE          *"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "*********************************"

echo "good_return_codes=${good_return_codes}"
echo "bad_return_codes=${bad_return_codes}"

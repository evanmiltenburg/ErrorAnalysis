# Use this script with Python 2. Python 3 does not play nice with the evaluation.

# This is my Anaconda command to activate Python 2.
source activate python2

# Evaluate all the files using the same script.
#python metrics.py ./satyrid/19-sept-2016-error-analysis.dev.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/baseline.metrics
#python metrics.py ./fixed/color-of-clothing_fixed.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/color-of-clothing.metrics
#python metrics.py ./fixed/activity_fixed.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/activity.metrics
#python metrics.py ./fixed/type-of-clothing_fixed.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/type-of-clothing.metrics
#python metrics.py ./fixed/gender_fixed.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/gender.metrics
python metrics.py ./fixed/scene-event-location_fixed.txt ./flickr30k_dev/reference0 ./flickr30k_dev/reference1 ./flickr30k_dev/reference2 ./flickr30k_dev/reference3 ./flickr30k_dev/reference4 > ./metrics/scene-event-location.metrics

# This is my Anaconda command to deactivate Python 2 again.
source deactivate

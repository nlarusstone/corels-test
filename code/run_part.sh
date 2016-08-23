for i in `seq 1 11`;
do
  python serial_priority.py -gc=False -part=$i -iter=5
done

for i in `seq 1 12`;
do
  python serial_priority.py -gc=False -part=$i
done

ctr=0
while [ $ctr -lt 20 ]
d
  python3 /home/cache/webserver.py $(($ctr+6969)) &
  ctr=$(($ctr+1))
done
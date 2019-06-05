ctr=0
while [ $ctr -lt 20 ]
do
  python3 /home/cache/ffmpeg_webserver/webserver.py $(($ctr+6969)) &
  ctr=$(($ctr+1))
done

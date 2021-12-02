#!/Document/ee250/final_project/ee250/final

#while [  ]; do
#
#// python audio.py
#// scp audio to server
#// wait for a few seconds
#// scp from server
#// if success, then file exist
## if fail, do again.

python3 audio.py
scp output.wav simon@52.143.125.62:~/
sleep 20



until scp simon@52.143.125.62:result.txt ~/Document/ee250/final_project/ee250/final
do
  sleep 1
done

ssh simon@52.143.125.62 "rm -f result.txt"
cat result.txt
#! /bin/bash

python3 randomFight.py

cd ps/

nb=0
for i in `ls`
do
	convert $i $i.jpg
	rm $i
	nb=$(($nb+1))
done
nb=$(($nb))

echo $nb "Conversion in png has ended"

for j in $(seq -f "%05g" 0 $(($nb-1)))
do
	montage -geometry 600x500 -tile 2x1 *-$j.ps.jpg together$j.jpg
	rm *-$j.ps.jpg
done

n=0

l=`ls ../gifCombat/` 
for file in $l
do
	v="%05g" $n
	if [ "final$v.gif" == $file ]
	then 
		n=$(($n+1))
	fi
done

#size= `identifify -format "%[fx:w]x%[fx:h]" "final$n.gif" `
#echo $size

echo "Writing ../gifCombat/final$1.gif"
convert  -delay 80 -loop 0 together*.jpg "../gifCombat/finalgif2.gif"

rm together*.jpg

cd ../

#animate "gifCombat/final$1.gif" &

exit 1

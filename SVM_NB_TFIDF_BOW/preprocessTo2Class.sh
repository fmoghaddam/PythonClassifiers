#separates different categories to different files

mkdir dataset
cd dataset
mkdir positive
mkdir negative
cd ..

cat positiveUniq.txt | awk -F "\t" '{
		print $2
}' > onlyPositive

cp onlyPositive dataset/positive
cd dataset/positive
csplit -b '%d.txt' -s -f text -- onlyPositive '//' '{*}'
rm text0.txt
rm onlyPositive
cd ../..

cat negativeUniq.txt | awk -F "\t" '{	
		print $2
}' > onlyNegative
cp onlyNegative dataset/negative
cd dataset/negative
csplit -b '%d.txt' -s -f text -- onlyNegative '//' '{*}'
rm text0.txt
rm onlyNegative
cd ../..
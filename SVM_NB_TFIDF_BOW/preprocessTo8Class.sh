#separates different categories to different files

mkdir dataset
cd dataset
mkdir CEO_N
mkdir CEO_P
mkdir PRESIDENT_N
mkdir PRESIDENT_P
mkdir POPE_N
mkdir POPE_P
mkdir MONARCH_N
mkdir MONARCH_P
cd ..

cat positiveUniq.txt | awk -F "\t" '{
	if($1 =="CHAIR_PERSON_TAG")
		print $2
}' > onlyCEOPositive

cp onlyCEOPositive dataset/CEO_P
cd dataset/CEO_P
csplit -b '%d.txt' -s -f text -- onlyCEOPositive '//' '{*}'
rm text0.txt
rm onlyCEOPositive
cd ../..



cat positiveUniq.txt | awk -F "\t" '{
	if($1 =="HEAD_OF_STATE_TAG")
		print $2
}' > onlyPresidentPositive
cp onlyPresidentPositive dataset/PRESIDENT_P
cd dataset/PRESIDENT_P
csplit -b '%d.txt' -s -f text -- onlyPresidentPositive '//' '{*}'
rm text0.txt
rm onlyPresidentPositive
cd ../..


cat positiveUniq.txt | awk -F "\t" '{
	if($1 =="POPE_TAG")
		print $2
}' > onlyPopePositive
cp onlyPopePositive dataset/POPE_P
cd dataset/POPE_P
csplit -b '%d.txt' -s -f text -- onlyPopePositive '//' '{*}'
rm text0.txt
rm onlyPopePositive
cd ../..




cat positiveUniq.txt | awk -F "\t" '{
	if($1 =="MONARCH_TAG")
		print $2
}' > onlyKingPositive
cp onlyKingPositive dataset/MONARCH_P
cd dataset/MONARCH_P
csplit -b '%d.txt' -s -f text -- onlyKingPositive '//' '{*}'
rm text0.txt
rm onlyKingPositive
cd ../..


cat negativeUniq.txt | awk -F "\t" '{
	if($1 =="CHAIR_PERSON_TAG")
		print $2
}' > onlyCEONegative
cp onlyCEONegative dataset/CEO_N
cd dataset/CEO_N
csplit -b '%d.txt' -s -f text -- onlyCEONegative '//' '{*}'
rm text0.txt
rm onlyCEONegative
cd ../..


cat negativeUniq.txt | awk -F "\t" '{
	if($1 =="HEAD_OF_STATE_TAG")
		print $2
}' > onlyPresidentNegative
cp onlyPresidentNegative dataset/PRESIDENT_N
cd dataset/PRESIDENT_N
csplit -b '%d.txt' -s -f text -- onlyPresidentNegative '//' '{*}'
rm text0.txt
rm onlyPresidentNegative
cd ../..

cat negativeUniq.txt | awk -F "\t" '{
	if($1 =="POPE_TAG")
		print $2
}' > onlyPopeNegative
cp onlyPopeNegative dataset/POPE_N
cd dataset/POPE_N
csplit -b '%d.txt' -s -f text -- onlyPopeNegative '//' '{*}'
rm text0.txt
rm onlyPopeNegative
cd ../..


cat negativeUniq.txt | awk -F "\t" '{
	if($1 =="MONARCH_TAG")
		print $2
}' > onlyKingNegative
cp onlyKingNegative dataset/MONARCH_N
cd dataset/MONARCH_N
csplit -b '%d.txt' -s -f text -- onlyKingNegative '//' '{*}'
rm text0.txt
rm onlyKingNegative
cd ../..

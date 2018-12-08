counter=1
while [ $counter -le 100 ]
do
echo $counter
((counter++))
python3 reversi.py --verify --depth=4 --result_path=results/random_depth4.txt
done

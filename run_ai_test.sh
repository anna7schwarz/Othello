counter=1
while [ $counter -le 100 ]
do
echo $counter
((counter++))
python3 reversi.py --test --depth=1 --timeout=1 --result_path=results/ai_depth1_timeout1.txt
done

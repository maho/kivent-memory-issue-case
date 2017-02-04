
set -x

for numvis in 1 2 3 4 5 6 7;do
    for single in 0 1;do
        mprof run python main.py $numvis $single &
        MPID=$!
        (sleep 600; pkill -P $MPID)&
        wait
        mprof plot -o plot-numvis$numvis-single$single-.png

    done
done

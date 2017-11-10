sq_res=`squeue`
regex='^_*([0-9]{5})'
regex_exempt='_PD_'
for job in ${sq_res// /_}
do
    if [[ $job =~ $regex_exempt ]]
    then
        continue
    fi
    if [[ $job =~ $regex ]]
    then
        jobid="${BASH_REMATCH[1]}"
        echo -n "$jobid | "
        hwres=`scontrol show job $jobid`
        username=`echo "$hwres" | grep 'UserId' | sed -e 's/^\s*UserId=//;s/(.*$//'`
        printf " %-15s |" $username
        plat=`echo "$hwres" | grep 'Partition' | sed -e 's/^\s*Partition=//;s/ AllocNode.*$//'`
        printf " %-10s |" $plat
        echo "$hwres" | grep 'TRES' | sed 's/^.*TRES=//'
    fi
done

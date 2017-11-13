A sh script to output each user's hardware resource allocation on slurm.

## Updates ##
* **v0.3** Add python script for grouping
* **v0.2** Jobs with 'PD' status are filtered
* **v0.1** Initial version
## Usage ##
* To show results contain specified string:
```
sh peeker.sh > output.txt
cat output.txt | grep Bigvideo
```
* To group results by Name and Platform:
```
sh peeker.sh > output.txt
python counter.py
```

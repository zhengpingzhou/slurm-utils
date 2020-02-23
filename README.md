# slurm-utils
Utils for creating and launching slurm jobs.

## Requirement
Ubuntu, Python 3.6+

## Example Usage
```bash
echo "alias sl='python /path/to/slurm.py'" >> ~/.bashrc
. ~/.bashrc
sl "python helloworld.py -id test_slurm" --node=<node>
```

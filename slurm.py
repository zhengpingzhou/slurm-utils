"""
Workflow:
sb "python train.py -id ..."
-> generate slurm/slurm/slurm-$RUNID.sh
			slurm/wrapper/wrapper-$RUNID.sh
			slurm/stdout/stdout-$RUNID.out
-> sbatch slurm/slurm/slurm-$RUNID.sh
"""
import argparse
import sys, os
import shlex
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str)
parser.add_argument('--node', type=str)
args = parser.parse_args()

CMD = args.cmd
PWD = os.getcwd()
print(CMD)
print(PWD)

parser = argparse.ArgumentParser()
parser.add_argument('-id', '--run_id', type=str, required=True)
opt, _ = parser.parse_known_args(shlex.split(CMD))
RUN_ID = opt.run_id + '-' + datetime.datetime.now().strftime('%b-%d-%y@%H:%M:%S')

root_dir = f'{PWD}/slurm'
slurm_dir = f'{root_dir}/slurm'
wrapper_dir = f'{root_dir}/wrapper'
stdout_dir = f'{root_dir}/stdout'

slurm_script = os.path.join(slurm_dir, f'slurm-{RUN_ID}.sh')
wrapper_script = os.path.join(wrapper_dir, f'wrapper-{RUN_ID}.sh')

os.system(f'mkdir -p {slurm_dir}')
os.system(f'mkdir -p {wrapper_dir}')
os.system(f'mkdir -p {stdout_dir}')

with open(wrapper_script, 'w') as fout:
    fout.write(CMD + '\n')

template = f"""#!/bin/bash
#SBATCH --partition=orion --qos=normal
#SBATCH --time=07-00:00:00
#SBATCH --nodes=1 
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --nodelist={args.node}

# only use the following on partition with GPUs
#SBATCH --gres=gpu:titanxp:1

#SBATCH --job-name={opt.run_id}
#SBATCH --output={stdout_dir}/{RUN_ID}-%j.txt
echo "RUN_ID={RUN_ID}"

# only use the following if you want email notification
####SBATCH --mail-user=[youremailaddress]
####SBATCH --mail-type=ALL

# list out some useful information (optional)
echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory = "$SLURM_SUBMIT_DIR

# sample process (list hostnames of the nodes you've requested)
NPROCS=`srun --nodes=${{SLURM_NNODES}} bash -c 'hostname' |wc -l`
echo NPROCS=$NPROCS

srun bash {wrapper_script}
echo "Done"

"""
with open(slurm_script, 'w') as fout:
	fout.write(template)

print('slurm script:', slurm_script)
print('wrapper script:', wrapper_script)
print('writing output to:', stdout_dir)

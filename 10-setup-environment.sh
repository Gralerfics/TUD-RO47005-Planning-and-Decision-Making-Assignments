# by default, we assume you have Linux:
wget -O miniforge.sh https://github.com/conda-forge/miniforge/releases/download/23.3.1-0/Miniforge3-23.3.1-0-$(uname)-$(uname -m).sh

bash miniforge.sh -b -p $PWD/miniforge3

source $PWD/miniforge3/bin/activate
printf "\n-----------\nminiforge3 is setup. The following should now point to a conda path:\n"
which conda
./00-setup.sh
./02-start-notebook.sh
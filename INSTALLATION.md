# Some help on the installation of required packages
There is a number of software dependences require installation. I suggest  creating a `conda environment` where all packages can be conveniently installed. Some information how to star with conda can be found [here](https://conda.io/docs/user-guide/getting-started.html) and on conda management [here](https://conda.io/docs/user-guide/tasks/manage-environments.html).
## Installing conda and creating an environment

1. [Download](https://www.anaconda.com/download/) and install Anaconda:selecting Python 3.7 option
	
2. Create own conda environment called **itt** with: `conda create -n itt python=3.5`

3. In a terminal (In Windows type `Anaconda Prompt` to initialise a terminal) activate the environment: `source activate itt` or `activate itt` for Windows
	
4. Now you're ready to install software into your **itt** environment, do:
	```
	conda install -c anaconda pillow
	conda install scikit-learn
	conda install matplotlib
	conda install -c anaconda cython
	conda install -c anaconda h5py
	conda install spyder
5. Install [TomoPhantom](https://github.com/dkazanc/TomoPhantom) software for tomographic data modelling and reconstruction  
`conda install -c tomophantom -c ccpi -c conda-forge`
6. Install [FISTA-tomo](https://github.com/dkazanc/FISTA-tomo) package where *normalisation* function might be needed for **Data alignment** challenge: `conda install -c dkazanc fista-tomo`
7. Install [CCPi Regularisation toolkit](https://github.com/vais-ral/CCPi-Regularisation-Toolkit) which might be helpful to run some denoising routines for **Objects tracking** and **Dynamic imaging** challenges. `
conda install ccpi-regulariser -c ccpi -c conda-forge`

# Other useful `conda` commands
- the list of environments: `conda info --envs`
- delete created **itt** environment: `conda remove --name itt --all`

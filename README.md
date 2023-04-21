# Geodesy 101 Resources

Source code and resources for the Geodesy 101 short course.
The recommended way to run the scripts is in a [conda](https://docs.conda.io/en/latest/index.html) environment:
```
conda create -n geodesy101
conda activate geodesy101
```
Then, install all dependencies:
```
conda install numpy scipy cartopy netcdf4 numpydoc sphinx pyyaml h5py
```
Clone the repository and install the included module:
```
git clone --recurse-submodules https://github.com/akvas/geodesy101.git
cd geodesy101/grates
python -m pip install .
cd ..
```

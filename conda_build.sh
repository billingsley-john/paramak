
# requires conda-build to be installed
# conda install conda-build
# conda install anaconda-client

# upload requires login with
# anaconda login --username fusion-energy --password


rm -rf /tmp/conda-build

conda-build conda/ -c cadquery -c conda-forge --croot /tmp/conda-build --python 3.8

anaconda upload --force /tmp/conda-build/linux-64/paramak-0.2.5-py3.8.tar.bz2

conda install --use-local -c fusion-energy paramak

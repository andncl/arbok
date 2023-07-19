# Arbok
Measurement framework based on the python module QCoDeS. Arbok is taylored for routines 
using the Quantum Machines OPX(+) quantum control hardware.

## Installation 
To install the arbok python module locally follow the steps below

### 1) Clone github repository
```bash
git clone https://github.com/andncl/arbok.git
```

### 2) Create new conda env 

```bash
conda create --name <your_env_name>
```

### 3) Go to repo folder and install local arbok module

```bash
pip install -e .
```
Arbok should now install all its requirements automatically. If you need additional
packages, install them in your new environment called <your_env_name>
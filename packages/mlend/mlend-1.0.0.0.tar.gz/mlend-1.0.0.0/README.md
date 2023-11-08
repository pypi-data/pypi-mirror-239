# MLEnd Datasets

### Links: **[Homepage](https://MLEndDatasets.github.io)** | **[Documentation](https://mlend.readthedocs.io/)** | **[Github](https://github.com/MLEndDatasets)**  |  **[PyPi - project](https://pypi.org/project/mlend/)** |     _ **Installation:** [pip install mlend](https://pypi.org/project/mlend/)
-----

-----

## Installation

**Requirement**:  numpy, matplotlib, scipy.stats, spkit

### with pip

```
pip install mlend
```

### update with pip

```
pip install mlend --upgrade
```


## Download data

```
import mlend
from mlend import download_spoken_numerals, spoken_numerals_readfiles


datadir = download_spoken_numerals(save_to = '../Data/MLEnd', subset = {},verbose=1,overwrite=False)

```

## Create Training and Testing Sets

```
TrainSet, TestSet, MAPs = spoken_numerals_readfiles(datadir_main = datadir, train_test_split = 'Benchmark_B', verbose=1,encode_labels=True)

```




# Contacts:
* **Jesús Requena Carrión**
* Queen Mary University of London

* **Nikesh Bajaj**
* Queen Mary University of London
* n.bajaj[AT]qmul.ac.uk, n.bajaj[AT]imperial[dot]ac[dot]uk

______________________________________

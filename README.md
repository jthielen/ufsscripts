# UFS SR Weather App/FV3-SAR Svr Wx Scripts

Python analysis scripts and utilities for working with post-processed and raw output from FV3-SAR for the purposes of severe weather investigations. Originally built for the 2020-21 DTC Visit of Dr. Bill Gallus and grad student Jon Thielen from Iowa State University.

Released under the terms of the Apache License Version 2.0, (c) 2020 Jon Thielen

## Getting Started

1) Download the git repo

```
git clone https://github.com/jthielen/ufsscripts
```

2) Create the Python Conda environment

(make sure that you have an active conda install working, either using the provided binaries on your system or your own miniconda install)

```
conda env create
conda activate ufs
```

This will automatically create (and then activate) an environment called `ufs`. Note that this environment also subsumes the `regional_workflow` environment used by the FV3-SAR regional workflow scripts (so you don't have to worry about switching back to that when running the workflow scripts).

3) Set up your configuration

Copy the template configuration (or copy from another user)

```
cp config_template.yml config.yml
```

Now you should be ready to go!

## Using these scripts

TODO

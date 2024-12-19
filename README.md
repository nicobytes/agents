### Create environment from scratch

```bash
conda create -n agents python=3.11
conda activate agents
conda install -c conda-forge poetry
conda env export --from-history > environment.yml
```

### Create environment from file
```bash
conda env create -f environment.yml
```
# mgi.tenormanagement

## Installing

Running in native environment requires user to have anaconda environment.

```shell
conda env create -f environment.yml
```

If user already created the environment and needs an update:

```shell

conda env update -n tenor -f environment.yml
```

## Executing

### Run under windows:

`app.cmd`

### Run inside docker:

`build_and_run_locally.cmd`

### Run manually:

**Windows**:

```shell
conda activate tenor
python main.py
```

**Linux**:

```shell
source activate tenor
python main.py
```



Build image and push to image repo:

`build_and_push.cmd`

Deploy to local kubernetes:

`deploy_kube.sh`

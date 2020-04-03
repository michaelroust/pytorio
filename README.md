

### Install requirements
```bash
    python3 -m venv env
```

### Activate venv (on UNIX)
```bash
    source env/bin/activate
```

### Install requirements
```bash

    pip install -r requirements.txt
```

### Run main
```python
    python src/main.py
```


### Running the tests
```bash
    export PYTHONPATH="./src:$PYTHONPATH"
    python3 -m unittest discover -v -s ./test -p *test*.py
```


### Export requirements
```bash
    `pip freeze > requirements.txt`
```

### Uninstall all but requirements.txt
https://stackoverflow.com/questions/13176968/how-can-i-use-a-pip-requirements-file-to-uninstall-as-well-as-install-packages

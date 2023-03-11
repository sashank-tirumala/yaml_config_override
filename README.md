# YAML CONFIG OVERRIDE
## Why?
YAML Config Override is an extremely lightweight command line interface to your YAML configuration file.
Just create a yaml config file, and yaml_config_override will add command line arguments to it automatically. No need to write hundreds of argparse lines!

## Installation:
```bash
pip install yaml_config_override
```

## Example?
Suppose you have a YAML file `test.yaml`:
```yaml
outer:
    x: 0
    inner:
        y: 1
        eveninner:
            z: abc
```
then you can use it in the code `main.py`:
```python
from yaml_config_override import add_arguments
import yaml
from pathlib import Path
my_config_path = 'test.yaml'
conf = yaml.safe_load(Path(my_config_path).read_text())
conf = add_arguments(conf)
print(conf)
```
Now you can call main.py as follows:
```
python main.py --outer.x 2 --outer.inner.eveninner.z hello
```
Your program output will be:
```
{'outer': {'x': 2, 'inner': {'y': 1, 'eveninner': {'z': 'hello'}}}}
```

Alternatively if you want to pass the config file as a command line argument you can modify the code as follows:
```python
from yaml_config_override import add_arguments
conf = add_arguments()
```

Now you call main.py as :
```
python main.py --config test.yaml --outer.x 2 --outer.inner.eveninner.z hello
```

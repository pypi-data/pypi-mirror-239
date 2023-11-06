# Maplewood

maplewood is a Python Library for creating logfiles in Plain Text(.txt) Format

## Compatibility

maplewood has been tested to work on Windows, but should work on Linux and MacOS as well

## Installing

maplewood can be installed using pip or any PyPI package managers
```sh
pip install maplewood
``` 

## Usage

```python
# import the chainsaw module 
# containing the 'Chainsaw' class
from maplewood import chainsaw as cs

# creates a log.txt file in ./logs/
example_log = cs.Chainsaw()

# To log an event, we open the file first
example_log.open()

# To write to the log file
example_log.write(success=True, message="Example Task Executed")
# OR
# if we define a default success or failure message
example_log.update(success="Example success",
                   failure="Example Failure",
                   module="example")
example.log(False) # writes default fail state
example.log(True)  # writes default pass state

# we can close the file if needed
example_log.close()
# and reopen
example_log.open()

# to check if log file is open
example_log.is_open() # -> bool

# remember to close the file
example_log.close()
```
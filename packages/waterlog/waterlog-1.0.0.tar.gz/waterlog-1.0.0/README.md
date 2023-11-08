# Waterlog
A thin wrapper around the Python `logging` module with sane defaults
and a simpler interface.  All symbols from `logging` are imported into
`waterlog`, so you can use them from `waterlog` without importing `logging`.

## Example Usage
```
import waterlog

waterlog.setup()
waterlog.set_level(waterlog.DEBUG)
log = waterlog.get(__name__)

if __name__ == '__main__':
   log.info("Hello, world!")
```

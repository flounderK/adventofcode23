# adventofcode23

## Usage
To use this repo, you will have to install the `aoc23_utils` python package contained in the repo:
```bash
python3 -mpip install -e .
```


## Uninstall
once you are done, you will probably want to uninstall the `aoc23_utils` package.
```
python3 -mpip uninstall aoc23_utils
```

## Lessons Learned
- `"(?=(%s))"` will allow overlapping matches in regular expressions
- `re.search(...).end()` returns a value one past the index of the last character

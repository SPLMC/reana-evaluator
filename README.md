# ReAna-SPL Evaluator

Evaluator script designed to repeatedly run ReAna-SPL's analysis strategies and gather statistics.
Use `./evaluator.py --help` for options.

The tools needed to run the tests (ReAna-SPL and PARAM) need to be placed under `tools` directory.
Likewise, the behavioral models for the subject SPLs need to be placed under `models`.

Configurations such as executable path and its command-line arguments may be manually
changed in the `configurations.py` module.
The pairs of SPL and strategy to be tested are also defined there.

## Dependencies

This evaluation script depends on the SciPy, NumPy and Matplotlib packages.
They can be installed using _pip_ (as _root_):

```bash
$ pip install matplotlib
$ pip install numpy
$ pip install scipy
```

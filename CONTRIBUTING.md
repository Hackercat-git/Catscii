# Contributing to Catscii

Thanks for taking the time to contribute! 🐾

## Getting started

```bash
git clone https://github.com/Hackercat-git/Catscii.git
cd Catscii
pip install -e ".[fast]"   # installs Pillow + numpy
```

Run the tests before making changes:

```bash
python -m pytest tests/
```

## Reporting bugs

Open an [issue](https://github.com/Hackercat-git/Catscii/issues) and include:

- Your Python version (`python --version`)
- Your Pillow version (`pip show pillow`)
- The command you ran
- What you expected vs. what happened

If you can, attach a small test image that reproduces the problem.

## Suggesting features

Open an issue with the label **enhancement** and describe:

- What you want Catscii to do
- Why it would be useful
- Any examples you have in mind

## Submitting a pull request

1. Fork the repo and create a branch: `git checkout -b my-feature`
2. Make your changes
3. Add or update tests in `tests/test_catscii.py`
4. Run the test suite: `python -m pytest tests/`
5. Open a pull request against `main`

Please keep PRs focused — one feature or fix per PR makes review faster.

## Code style

- Python 3.10+, no external dependencies beyond Pillow (numpy is optional)
- Follow the existing style — keep functions small and well-named
- Add a docstring to any new public function

## Adding a new character style

Edit `styles.py` and add an entry to `STYLES`. Run the tests to make sure
nothing breaks, then update the README table and `docs/index.html`.

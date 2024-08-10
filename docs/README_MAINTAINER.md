# Maintainer documentation

## 1. Clone project and install pip/python

## 2. Create virtual env and install project dependencies

Install `virtualenv` to set up your virtual environment
```bash
pip install --upgrade virtualenv
```

Go to project root and create your virtual environment
```bash
cd <PROJECT_ROOT>
python -m venv venv
```

Activate your virtual environment
```bash
# Windows
.\venv\Scripts\activate

# Linux
source venv/bin/activate
```

Install project dependencies
```bash
pip install -r requirements.txt
```

Install module locally, so you can import it as a module
```bash
pip install -e .
```

## 3. Run the tests

### Prerequisites
Steps 1. and 2. above

### How to run

```bash
# Windows
.\wtests.bat

# Linux
./tests.sh
```

## 4. Build and upload release

Install dependencies

```bash
pip install --upgrade setuptools wheel build twine
```

Build the package (wheel and sdist)
```bash
python -m build 
```

Ensure `.pypirc` in user folder is correct, then upload
```bash
python -m twine upload dist/*
```

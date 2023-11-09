![Workflow Status](https://github.com/software-students-fall2023/3-python-package-exercise-plant-3-0/actions/workflows/build.yml/badge.svg)

# PyPrankError
PyPrankError is a Python package that lets the user create silly (or serious) error messages, stack traces, crash reports, and hacked messages for a pranks purpose.

## Team members
1. [Nathalia Xu](https://github.com/slurp-slurp)
2. [Robert (Bobby) Impastato](https://github.com/bobbyimpastato)
3. [Phoebus Yip](https://github.com/phoebusyip)
4. [Alicia Hwang](https://github.com/a-j-hwang)

## [link to our package's page on the PyPI website](https://pypi.org/project/pyprankerror/)

## How to Install and Use
In your project directory, run `pip install -i https://pypi.org/project/pyprankerror/`.

Now import pyprankerror to use it your own program:

`import pyprankerror`

### Documentation for all functions:  

`generate_hacked_message(is_long, is_silly)`

Description: Returns a message that makes it look like the user is being hacked. Return nothing.
* is_long (bool): False indicates shorter output, True indicates longer output.
* is_silly (bool): True indicates silly less realistic and silly variable and function names.


`generate_stacktrace(length, is_silly)`

Description: Prints a fake stack trace and returns nothing.
* length (int): 0 indicates short (9 lines) output, 1 indicates long (26 lines) output.
* is_silly (bool): True indicates less realistic and silly variable names in the stack trace.


`generate_crash_report(is_long, is_silly)`

Description: Prints a fake crash report
* is_long (bool): False indicates shorter (19 lines) output, True indicates longer output (38 lines).
* is_silly (bool): True indicates a silly and less realistic crash report.


`generate_error(err_type, isSilly)`

Description: Returns a fake error message

* err_type (str): Indicate a “syntax”, “runtime” or “logical” error type.
* is_silly (bool): True indicates silly and less realistic and crash report.

### [Example project](example-program.py)
Run `python example-program.py`

## How to contribute

### To test, build, and distribute with GitHub repo code
- To contribute to our package, please clone [this](https://github.com/software-students-fall2023/3-python-package-exercise-plant-3-0) repository.   
- Move into the project directory and proceed to following steps:  
- Install `pipenv` if you have not already done so: `pip install pipenv`   
- If you have already installed but cannot use `pipenv`, use `python -m pipenv` for all `pipenv` commands instead.  
- Activate the virtual environment and install project dependencies with pipenv:  
`pipenv --python 3.x` # Replace '3.x' with your desired Python version  
- Activate the virtual environment: `pipenv shell`  
(You might need to install `pipenv` in the virtual environment again if you receive error when activating it.)  
- Install project dependencies, including dev packages: `pipenv install --dev`
- Test the source code with Pytest from the main project directory: `pytest` 
- Install build if you haven't: `pip install build`  
- When you are satisfied with the change and wish to build and distribute, make the build: `python -m build`, increment the version number, and then upload to GitHub or PyPI depending on the need of the developers.

### To test, build, and distribute with package from PyPI
- Try [installing and using your package](https://packaging.python.org/en/latest/tutorials/packaging-projects/#installing-your-newly-uploaded-package) in a separate Python project
- Install `pipenv` if you have not already done so: `pip install pipenv`   
- Create a pipenv-managed virtual environment and install the latest version of your package installed:  `pipenv install -i <link to package>` (Note that if you've previously created a pipenv virtual environment in the same directory, you may have to delete the old one first. Find out where it is located with the pipenv --venv command.)  
- Activate the virtual environment: `pipenv shell` 
- Write test code. Note that when testing a PyPI package, the import statement should look like `from PyPrankError import pyprankerror`. If you use any test code from the repository, remove the `src.` in the import statements. 
- Test the source code with Pytest from the root directory: `pytest` 
- Install build if you haven't: `pip install build`  
- Include a pyproject.toml file. You can copy from the repository and increment the version number.
- When you are satisfied with the change and wish to build and distribute, make the build: `python -m build` and then upload to GitHub or PyPI depending on the need of the developers.






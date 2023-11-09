# Infra Simple Service
This readme and template is intended as a guide on how Python code **in this repo** should be written, documented and distributed.

It also includes an [example](#example-on-how-to-use-this-example-simple_service-code-in-other-projects) on how to *use* such a Python library (PIP package) in other project, e.g. in other Python code/projects, in GitHub Action/Azure DevOps Pipelines etc.

The files included in the `code/example-code-template/src` directory may be used as a template in other projects.
```
├─ code/example-code-template/src/
│  ├─ license.txt
│  ├─ pyproject.toml
│  ├─ readme.md
│  ├─ setup.py
│  ├─ simple_service/
│  │  ├─ __init__.py
│  │  ├─ simple_service.py
```

The files included in the `tools` directory may be used to help you set up a isolated Python develop environment (venv) and to distribute your code as a project to your PyPI account.
```
├─ tools/
│  ├─ build.sh
│  ├─ create_requirements.sh
│  ├─ create_venv.sh
```

### What needs to be done before start coding
Create a directory where the project files, code files and directories will reside.
The files and subfolder within this directory should be structured as the `example-code-template` directory tree above.
You may copy all the items from this directory and use them as a template, but make sure to edit the files like described below.

Run `tools/create_venv.sh`
This will create a hidden directory `.venv` within the `src` directory. This will be the virtual environment for the code to use and where  packages will be installed during development.

Notes from `tools/create_venv.sh`:
```
Instead of installing all the needed pip packages on to your system,
the packages should be installed to an isolated environment instead.
Use this script to create a virtual environment before you start coding.

Only the needed packages, and verified version, should be installed
during deploy. This is ensured by generating a requirements.txt file
when ready to distribute and deploy. (Please refer to the create_requirements.sh script.)

Make sure you create a src directory for your code  directory and
files to reside in. The virtual enviroment will be created in a .venv
directory, which is also located in the src directory.

Execute the script by running: ./create_venv.sh

Specify this src/.venv for you IDE project or
activated from shell by running: source .venv (from within the src directory)
```

### When ready to start coding
Make sure your the venv is activated. Please refer to your IDE or activate it from command line using `source .venv/bin/activate`

The code must be placed inn subfolder(s) within the `src` directory - like with the `simple_service` diretory from the template / example.


### How the code should be written and documented?
The code should include comments and proper documentation. **Use Docstrings**
Please refer to the documentation in [simple_service.py](https://github.com/equinor/ops-infra/blob/python_guidelines/python/template_simple_service/src/simple_service/simple_service.py)
and to [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code)

To write proper and understandable code, for you and for others to read, please refer to
[How to Write Beautiful Python Code With PEP 8](https://realpython.com/python-pep8/)

### What needs to be done prior to build and distribution of the code?
`src/requirements.txt`
A `requirements.txt`must be checked in and always follow the code. You may use the `tools/create_requirements.sh`to create one. If new packages are installed or updated during the development, the `requirements.txt` must be regenerated. Use the `tools/create_requirements.sh` frequently/whenever needed.

---
`src/license.txt`
Should be included. We will just use the The MIT License for now. So leave this file as it is.

---

`src/setup.py`
Must be included, but just leave it like it is.

---

`src/pyproject.toml`
Example from the **template_simple_service**:
```
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "infra_simple_service"
description = "Template and testing purposes"
license = {file = "license.txt"}
dynamic = ["version", "readme"]
dependencies = [
    "requests"
]

[tool.setuptools.dynamic]
version = {attr = "simple_service.__version__"}
readme = {file = "readme.md", content-type = "text/markdown"}
```
Edit the following under the `[project]` part:

- **name**
This will be the name of the project on pypi.org. E.g.:
`name = "my-project"`

- **description**
A short description of the project. E.g.:
`description = "A simple service to calculate number of atoms in the universe"`

- **dependencies**
A list of all the pip installed packages during development. These are dependencies which are needed for the code to run. E.g.
`dependencies = ["requests", "Flask", "github-cli"]`

For the **version**, which is located  under the `[tool.setuptools.dynamic]`part, the path to the `__init__.py` file must be correct. E.g.:
`version = {attr = "my_code_dir.__version__"}`

---
`src/my_code_dir/__init__.py`
This file **MUST** include the version of the project.

Example from the **template_simple_service**:
```
__version__ = '0.0.1'
__author__ = "Svein Tore Eikeskog"
__email__ = "st@eikeskog.com"
```

**NOTE:** Next time the project is pushed to pypi the version must be bumped. Edit the `__init__py`file accordingly.

### Build and distribute the project to pypi.org
Execute the `src/build.sh`script to build and push the code pypi.org.


### Example on how to use this example "simple_service" code in other projects:

Create a new directory for your project. Create a new virtual venv and source it:

 ```
 mkdir my_new_project`
 cd my_new_project
 python3 -m venv venv
 source venv/bin/activate
 ```

 Install the simple service from the example:
```
pip install infra-simple-service
```
Create a file (e.g. `main.py`) for the sample code:
```
#!/usr/bin/env python

from simple_service import simple_service

wan_service = simple_service.SimpleService()
wan_service.fetch_wan_ip()
my_ip = wan_service.get_wan_ip()
print(my_ip)
```

### PyPI - account info
TODO: Include this info about PyPI in this wiki.
Equinor account vs. Bouvet account vs. private
Info will follow....
For testing it will probably be ok to use your private account...

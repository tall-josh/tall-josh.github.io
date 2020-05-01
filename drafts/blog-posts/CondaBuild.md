{% raw %}
# Build My First Conda Package Using FUCKING Conda-Build

I have never some across a package with less in the way of concrete examples and work-throughs the assume beginner level.  Not to mention explanations (even at a high level) of what I need to do and why to build a simple conda package. So I'll fucking do it! You're welcome Void.

## What the FUCK do I need to do

### Organize Your Code

If you've already got your code build into a pip package you're off to a good start. If not, [here](https://pythonhosted.org/an_example_pypi_project/setuptools.html#setting-up-setup-py) are some basics.

In a nut shell, if you have a `setup.py` script and you can run `pip install .` you're in a good place.

## What The FUCK does {{ this|mean }}

This is Jinja2 templating syntax. It's pretty simple once you take a look at the docs. To be honest they have a lot of docs, but no realy hands on examples for real world use. Howerver, there are lots of other resources online. [This](http://zetcode.com/python/jinja/) got me started.

In short:
  - `{{ This }}` allows you to insert a variable. You can even cast `TO.lower()` or `TO|lower`.
  - `{% this is a code block %}` For example:

  ```yaml
  # A special function in conda-build that reads in
  # information from your setup.py.
  # In this case we're storing it in a variable
  # named 'data'
  {% set data = load_setup_py_data() %}

  # Here we're pulling out the 'name' value from
  # the data variable and storing it in 'name'
  {% set name = data['name'] %}

  # A key in the yaml file
  entry_points:
    # Loop over all elements of a list
    # Perform an operation on the 'entry' variable
    # and insert it after the '- '
    {% for entry in data['entry_points']['console_scripts'] %}
      - {{ entry.split('=')[0].strip() }} = {{ entry.split('=')[1].strip() }}
    {% endfor %}
  ```

## Install

```bash
conda install conda-build
```

## Run

```bash
# Point conda build to the dir where the recipe
# is located
conda build conda.recipe/
```

# Errors

## Does the setup.py even get loaded correctly

I could not find a way to easily see what (if anythin) Jinja2 had loaded
using `load_setup_py_data()` do I just added some print statements to help.

```python
# terminal
python

# Python shell
import conda_build
conda_build.__file__
> /path/to/site-packages/conda_build/__init__.py

# vim /path/to/site-packages/conda_build/_load_setup_py_data.py
# Add these to the end of load_setup_py_data(...)
# Around line 112, when I did this last
```

## Jinia Rendering Errors 

If you package is not too big then iterating on your template is not too time
consuming. If it is large then waiting for `conda build` to get around to rendering 
your `meta.yaml` can take a bit too long. Using `conda render <path to recipe dir>` 
will speed things up.

## This FUCKING BULLSHIT!

If you get an error that looks something like:

```bash
conda.CondaError: Unable to create prefix directory '/home/jp/anaconda3/conda-bld/beerbot_1588215699220/_h_env_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placeho'.
```

Ok, so what's happening. Well for some reason to do the nested paths on distributed systems this is a hack to make the character length 255 characters. WHATEVER! It doesn't matter. What does matter is they refuse to fix it. So ... if you're getting this error it's probs because you (like a FUCKING normal person) installed conda/miniconda in your home directory. If you're on Linux and you have your home directory encrypted then the encrypted filename length exceeds 255 and you get this error. You can tell conda build to use a non encrypted directory and this will all be a bad dream.

```bash
export CONDA_BLD_PATH=/tmp/condabuild
```

If you dont know if/what directories are encrypted on your system [This](https://askubuntu.com/questions/187323/how-can-i-confirm-that-im-using-ecryptfs) helped me.

## Yaml Parsing Errors:


### mapping values are not allowed in this context

**Error Message**
```bash
  Unable to parse meta.yaml file

  Error Message:
  --> mapping values are not allowed in this context
  -->   in "<unicode string>", line 7, column 8
```

**Cause**

Silly typo. Trailing 'A' at the end of the first line.
```yaml
# Jinja2 Templating syntax. load_setup_py_data is a build in function
# that loads the data from setup.py.
{% set data = load_setup_py_data() %}A

# Set the name variable to the one defined in setup.py
{% set name = data['name'] %}

# Set the version variable to the one defined in setup.py
{% set version = data['version']  %}

package:
  name: "{{ name|lower }}"
  version: "{{ version }}"
  ...
```
### package/name missing

**Error Message**

```bash
Error: package/name missing in: '/home/jp/Documents/repos/beerbot/conda.recipe/meta.yaml'
```

**Cause**

I guessed the vaiable must be empty. I also tried, `name: {{ name.lower()}}` and got a NoneType is not callable error which confirmed my suspicion.

It appears the path to setup.py is realitave to where `meta.yaml` is located. So adjusting adding the arg `setup_file` fixed the isseue. I would point you to some concrete docs on the fucntion but alas I could not find any :-( [here](https://github.com/conda/conda-build/blob/master/conda_build/_load_setup_py_data.py) is the function def on git though.

```Yaml
# Jinja2 Templating syntax. load_setup_py_data is a build in function
# that loads the data from setup.py.

########## THIS CAUSED THE ERROR ############
### {% set data = load_setup_py_data() %} ###
#############################################

# THIS FIXED IT!
# path to setup.py relitave to  recipe_dir.
# I'm running this from the top level dir of the repo with
# conda.recipe dir one level down.
#
# repo_dir/
#   conda.recipe/
#     meta.yaml
#   setup.py
#   ...
#
# from_recipe_dir is set to True to tell the function
# to look for setup.py "from" tje recipe directory.
{% set data = load_setup_py_data(setup_file='../setup.py', from_recipe_dir=True, recipe_dir='./conda.recipe/') %}

# Set the name variable to the one defined in setup.py
{% set name = data['name'] %}

# Set the version variable to the one defined in setup.py
{% set version = data['version']  %}

package:
  name: {{ name|lower }}

```
{% endraw %}

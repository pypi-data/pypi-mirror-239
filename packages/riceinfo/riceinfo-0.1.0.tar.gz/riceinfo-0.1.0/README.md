# RiceInfo Package
![Python package build test](https://github.com/software-students-fall2023/3-python-package-exercise-riceballz/actions/workflows/workflow.yaml/badge.svg)


## What is RiceInfo?

RiceInfo is a fun little package that returns rice trivia, puns, and pictures of riceballs.

## Commands

- **Print a Riceball**: Print out a riceball with a specified emotion, to which it will exclaim its feelings.
- **Tell a Rice Pun**: Input a specified type of joke to return a random pun from our dictionary of puns.
- **Rice History facts**: Specify a specific century you would like to learn a rice history fact. Disclaimer: Only goes through the 1st-21st century.
- **Countries with Rice**: Input from a specific country list to find out their preferred rice type.

## Installation
(Note) when testing this on pypitest we had to install with this: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple riceinfo==0.1.0

RiceInfo can be installed through the pip command: pip install riceinfo

## Functions and usage

Create a new python file and install riceinfo. From there, you can import riceinfo's package with the following lines of code:
```python
from riceinfo.rice import riceinfo
from riceinfo.rice import Pun
```


### Print a riceball: `print_riceball(emotions)`

Print out a riceball with a specific emotion.

The only emotions currently supported is: Happy, Sad, Angry, Nervous.

Valid commands will look like:
```python
riceinfo.print_riceball("happy")
riceinfo.print_riceball("sad")
riceinfo.print_riceball("angry")
riceinfo.print_riceball("nervous")
```

### Tell a Rice Pun: `tellPun(punType: Pun) -> str`

Returns a specified type of pun relating to rice. We have specific types of jokes, short length puns, medium length puns, long length puns, dad puns, and rhyme puns. If you want tio use this function please make sure to also import the pun class Which is provided above at Functions and usage

Valid commands are:
```python
pun = riceinfo.tellPun(Pun.SHORT)
pun = riceinfo.tellPun(Pun.MEDIUM)
pun = riceinfo.tellPun(Pun.LONG)
pun = riceinfo.tellPun(Pun.DAD)
pun = riceinfo.tellPun(Pun.RHYME)
```


This should return the pun to the variable.

### Rice History: `history(century)`

Input a specific century of the common era to have returned a year specific history fact.

Valid command examples are:
```python
history = riceinfo.history(1)
history = riceinfo.history(5)
history = riceinfo.history(21)
history = riceinfo.history(0)
history = riceinfo.history(22)
```



Note that inputting integers that are not within 1 through 21 will return a quip about staying within the range.

### Country's preferred rice: `riceCountry(country_name)`

Input a country from the list of research countries to have returned a small info card about the rice that country commonly uses and its unique properties.

The countries that are valid within this package is: Brazil, Egypt, Mexico, Nigeria, China, Thailand, Indonesia, Japan, and South Korea.

A valid command examples would be:
```python
riceType = riceinfo.riceCountry('brazil')
riceType = riceinfo.riceCountry('Brazil')
riceType = riceinfo.riceCountry('Mexico')
```


### Example File
We have provided an example file with the methods noted above, [click here](https://github.com/software-students-fall2023/3-python-package-exercise-riceballz/blob/main/src/riceinfo/__main__.py).

## Contribute to the package

Should you feel compelled, feel free to contribute to the project. In order to contribute:
1. For the repository by going to our (GitHub Main Page)[https://github.com/software-students-fall2023/3-python-package-exercise-riceballz/tree/main]
2. Using Git Bash or a preferred shell, clone the repository to your local files with the command
'''
git clone ...
'''
3. Set up your development environment by opening up a terminal in python. If you do not have pipenv installed, run the command "pip install pipenv" to install the package. Once installed, install any package dependencies by running "pipenv install --dev".
4. Run "pipenv shell" to activate your virtual environment.
This should allow you to write your code to contribute to the riceinfo package.

### Other Notes

- Make sure to create your own feature branch, then add and commit your changes. From there, create a pull request. Our team will review changes when possible.
- When adding new written functions or building upon old commands, make sure to write and run additional tests in the tests folder.
- Remember to write necessary documentation in the README.md for any additional changes.

## Contributors

- [Andrew Huang](https://github.com/andrew0022)
- [Kei Oshima](https://github.com/KeiOshima)
- [Richard Qu](https://github.com/kingslayerrq)
- [Ryan Horng](https://github.com/Ryan-Horng)

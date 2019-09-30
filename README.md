# BRIW

Academy 2019 MiniProject

This project allows you to have an application that allows you to create rounds of drinks for a group of people, which one of them is going to prepare, and can ask the rest of the people what drinks they want.

## Getting started

### Prerequisites

* [Python 3](https://www.python.org/download/releases/3.0/) - The language used to develop the project.
* [Pytest](https://docs.pytest.org/en/latest/) - Framework used to run the tests.

### Installing dependencies

```
pip3 install -r requirements.txt
```

## Running the tests

Execute at the root of the project: 

```
pytest
```

Get test coverage:

```
pytest --cov=briw tests/
```

## Running the project

Execute at the root of the project: 

```
python3 -m briw
```

## Contributing


Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

#### NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## Releases

### V1.0
In this version you interact with the command console to interact with the user.
In this version you can create rounds in a way not oriented to the collaboration of other users. Only from the person who is using the application in the terminal. 

Link: https://github.com/JulioMarquezIW/BRIW/tree/v1.0

### V1.1

Restructuring of the project, to adapt it more to a Python project, allowing a better use of imports or the creation of the project as a package for export. 
Added unit tests for most general project functions.
Minor fixes.

### V1.2

Minor fixes after a documented section of manual testing. 

Link: https://github.com/JulioMarquezIW/BRIW/tree/v1.2

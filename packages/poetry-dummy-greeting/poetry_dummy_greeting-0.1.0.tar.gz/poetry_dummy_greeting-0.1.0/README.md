# poetry-dummy-greeting
Sample for testing python poetry

- Create a new project:    `poetry new <project-name>`
- Create a new virtual env: `poetry env use <full-path-to-python-executable>`
- Adding dependencies: `poetry add <package-name>`
    - Adding dependencies in a group: `poetry add <package-name1>  <package-name2> --group <group-name>`
- Create requirements from **poetry.lock**: `poetry export --output requirements.txt`
- Run pytest within poetry VM: `poetry run pytest -v`
- Build:   `poetry build`
- Publish: `poetry publish`
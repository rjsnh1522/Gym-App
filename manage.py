import os
import typer
from pathlib import Path

app = typer.Typer()


@app.command()
def startapp(name: str):
    folder_name = f"src/{name}"
    files = ["__init__.py", "views.py", "models.py", "schemas.py", "services.py"]
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    # Create the files inside the folder
    for file_name in files:
        file_path = os.path.join(folder_name, file_name)
        Path(file_path).touch()
    print(f"{name} created")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
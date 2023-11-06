from pathlib import Path

from typer import Option, Typer

from biorepo.repo import Repo

app = Typer(
    name="biorepo",
    help="A tool to manage bioinformatics software",
    add_completion=False,
)


@app.command()
def install(
    biorepo: Path = Option(Path("biorepo.toml")),
    root: Path = Option(Path(".biorepo")),
):
    repo = Repo(root=root, biorepo=biorepo)
    repo.install()


@app.command()
def list(
    biorepo: Path = Option(Path("biorepo.toml")),
    root: Path = Option(Path(".biorepo")),
):
    repo = Repo(root=root, biorepo=biorepo)
    repo.list()


def main():
    app()

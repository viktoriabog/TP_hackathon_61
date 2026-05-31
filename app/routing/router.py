import shutil
from pathlib import Path


class Router:

    def route(
        self,
        filepath,
        sender,
        category
    ):

        if sender and sender != "unknown":

            username = sender.split("@")[0]

        else:

            username = "unknown_user"

        output_dir = (
            Path("output")
            / username
            / category
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            output_dir
            / Path(filepath).name
        )

        shutil.copy(
            filepath,
            destination
        )
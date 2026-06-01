import shutil
from pathlib import Path


class Router:

    def route(self, filepath, sender, category, is_draft=False):
        if is_draft:
            output_dir = Path("output") / "drafts" / category
        else:
            output_dir = Path("output") / category

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            output_dir /
            Path(filepath).name
        )

        shutil.copy(
            filepath,
            destination
        )
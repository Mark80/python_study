from os import listdir
from os.path import isfile, join
from pathlib import Path
from src.repository import pg


class Migration:
    def __init__(self, pg: pg.PG, migration_folder: str):
        self.migration_folder = migration_folder
        self.pg = pg

    async def execute(self):
        folder = self.migration_folder

        migrations_dir = Path(folder)
        if not migrations_dir.is_absolute():
            migrations_dir = Path.cwd() / migrations_dir

        migrations_scripts = [
            f for f in listdir(migrations_dir) if isfile(join(migrations_dir, f))
        ]

        for script in sorted(migrations_scripts):
            with open(migrations_dir / script, "r") as sql_file:
                sql = sql_file.read()
                print(sql)
                try:
                    await self.pg.execute(sql)
                    print(f"Successfully executed {script}")
                except Exception as e:
                    print(f"Error executing {script}: {e}")

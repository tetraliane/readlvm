import click
import yaml
from . import LvmData

@click.command()
@click.option("-e", "--encoding", default="utf_8", help="encoding of the LVM file")
@click.option("-c", "--columns", default="", help="indices of columns to be picked")
@click.argument("src_filename")
def main(encoding: str, columns: str, src_filename: str) -> int:
    cols = None
    if len(columns) > 0:
        cols = list(map(lambda c: int(c) - 1, columns.split(",")))

    try:
        with click.open_file(src_filename, "r", encoding=encoding) as f:
            lvm = LvmData.read(f)
    except Exception as e:
        click.echo(f"{e}\n", err=True)
        return 1

    if cols != None:
        try:
            lvm.pick_cols(cols)
        except IndexError as e:
            click.echo(
                "There are only {} columns but the given index is {}.\n".format(
                    len(lvm.data_labels()), max(cols) + 1
                ),
                err=True
            )
            return 1

    with click.open_file("-", "w") as stdout:
        yaml.dump(lvm.into_yaml(), stdout, allow_unicode=True)

    return 0

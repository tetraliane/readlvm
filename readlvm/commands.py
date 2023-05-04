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
        cols = columns.split(",")

    try:
        lvm = LvmData.read(src_filename)
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

    with click.open_file("-", "r") as stdout:
        yaml.dump(lvm.into_yaml(), stdout, allow_unicode=True)

    return 0

import rich_click as click


@click.group(help="The base command-line interface for the tool.")
@click.pass_context
def cli(context: click.Context) -> None:
    """

    :param context:
    :return:
    """
    pass


if __name__ == "__main__":
    try:
        cli()
    except Exception as exc:
        pass

from puddl.cli.base import root


@root.command()
def transcribe():
    print('See LOG/23/10-29.md')


def main():
    root(auto_envvar_prefix='PUDDL')


if __name__ == '__main__':
    main()

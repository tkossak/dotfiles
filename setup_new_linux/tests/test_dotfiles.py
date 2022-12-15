from setup_new_linux.classes.dotfilesc import Dotfile

def test_dotfile():
    f = Dotfile(
        '/tmp/1/a',
        '/tmp/1/c',
        # f_backup_first=True,
    )
    f.install()
    # verify manually

if __name__ == '__main__':
    test_dotfile()
import os, tempfile


def system(cmd):
    tmp = tempfile.NamedTemporaryFile()
    ppath = os.environ['PYTHONPATH']
    os.unsetenv('PYTHONPATH')
    os.system('%s > %s' % (cmd, tmp.name))
    os.environ['PYTHONPATH'] = ppath
    output = tmp.read()
    tmp.close()
    return output

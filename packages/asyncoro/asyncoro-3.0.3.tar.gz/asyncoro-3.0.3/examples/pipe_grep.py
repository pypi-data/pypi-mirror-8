# Asynchronous pipe example using chained Popen

import sys, logging, subprocess, traceback, platform

if sys.version_info.major > 2:
    import asyncoro3 as asyncoro
    import asyncfile3 as asyncfile
else:
    import asyncoro
    import asyncfile
    
def writer(apipe, inp, coro=None):
    fd = open(inp)
    while True:
        line = fd.readline()
        if not line:
            break
        yield apipe.stdin.write(line)
    apipe.stdin.close()

def line_reader(apipe, coro=None):
    nlines = 0
    while True:
        try:
            line = yield apipe.readline()
        except:
            asyncoro.logger.debug('read failed')
            asyncoro.logger.debug(traceback.format_exc())
            break
        if not line:
            break
        print('%s' % line),
        nlines += 1
    print('lines: %s' % nlines)
    raise StopIteration(nlines)

# asyncoro.logger.setLevel(logging.DEBUG)
if platform.system() == 'Windows':
    # asyncfile.Popen must be used instead of subprocess.Popen
    p1 = asyncfile.Popen([r'\cygwin64\bin\grep.exe', '-i', 'error'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2 = asyncfile.Popen([r'\cygwin64\bin\wc.exe'], stdin=p1.stdout, stdout=subprocess.PIPE)
    async_pipe = asyncfile.AsyncPipe(p1, p2)
    asyncoro.Coro(writer, async_pipe, r'\tmp\grep.inp')
    asyncoro.Coro(line_reader, async_pipe)
    # in Windows child process may not terminate when input is closed -
    # so terminate it explicitly when pipe is done with:
    # p1.terminate()
    # p2.terminate()
else:
    p1 = subprocess.Popen(['grep', '-i', 'error'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['wc'], stdin=p1.stdout, stdout=subprocess.PIPE)
    async_pipe = asyncfile.AsyncPipe(p1, p2)
    asyncoro.Coro(writer, async_pipe, '/var/log/kern.log')
    asyncoro.Coro(line_reader, async_pipe)

    # alternate example:

    # p1 = subprocess.Popen(['tail', '-f', '/var/log/kern.log'], stdin=None, stdout=subprocess.PIPE)
    # p2 = subprocess.Popen(['grep', '--line-buffered', '-i', 'error'],
    #                       stdin=p1.stdout, stdout=subprocess.PIPE)
    # async_pipe = asyncfile.AsyncPipe(p2)
    # asyncoro.Coro(line_reader, async_pipe)

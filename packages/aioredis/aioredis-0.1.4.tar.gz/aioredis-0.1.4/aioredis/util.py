import asyncio

_NOTSET = object()

# NOTE: never put here anything else;
#       just this basic types
_converters = {
    bytes: lambda val: val,
    bytearray: lambda val: val,
    str: lambda val: val.encode('utf-8'),
    int: lambda val: str(val).encode('utf-8'),
    float: lambda val: str(val).encode('utf-8'),
    }


def _bytes_len(sized):
    return str(len(sized)).encode('utf-8')


def encode_command(*args):
    """Encodes arguments into redis bulk-strings array.

    Raises TypeError if any of args not of bytes, str, int or float type.
    """
    buf = bytearray()
    add = lambda data: buf.extend(data + b'\r\n')

    add(b'*' + _bytes_len(args))
    for arg in args:
        if type(arg) in _converters:
            barg = _converters[type(arg)](arg)
            add(b'$' + _bytes_len(barg))
            add(barg)
        else:
            raise TypeError("Argument {!r} expected to be of bytes,"
                            " str, int or float type".format(arg))
    return buf


@asyncio.coroutine
def wait_ok(fut):
    res = yield from fut
    if res == b'QUEUED':
        return res
    return res == b'OK'


@asyncio.coroutine
def wait_convert(fut, type_):
    result = yield from fut
    if result == b'QUEUED':
        return result
    return type_(result)

# -*- coding: utf-8 -*-
"""
Miscellaneous utility functions.

------------------------------------------------------------------------------
This file is part of h3sed - Heroes3 Savegame Editor.
Released under the MIT License.

@created     19.11.2011
@modified    16.11.2020
------------------------------------------------------------------------------
"""
import collections
import ctypes
import datetime
import locale
import math
import os
import re
import subprocess
import sys
import struct
import time
import urllib
import warnings


def m(o, name, case_insensitive=True):
    """Returns the members of the object or dict, filtered by name."""
    members = o.keys() if isinstance(o, dict) else dir(o)
    if case_insensitive:
        return [i for i in members if name.lower() in i.lower()]
    else:
        return [i for i in members if name in i]


def bytoi(bytes):
    """Converts a string of bytes or a bytearray to unsigned integer."""
    fmt = {1: "<B", 2: "<H", 4: "<L", 8: "<Q"}[len(bytes)]
    return struct.unpack(fmt, str(bytes))[0]


def itoby(v, length):
    """
    Converts an unsigned integer to a string of bytes of specified length.
    """
    fmt = {1: "<B", 2: "<H", 4: "<L", 8: "<Q"}[length]
    return struct.pack(fmt, v)


def safe_filename(filename):
    """Returns the filename with characters like \:*?"<>| removed."""
    return re.sub(r"[\/\\\:\*\?\"\<\>\|\x00-\x1f]", "", filename)


def format_bytes(size, precision=2, max_units=True, with_units=True):
    """
    Returns a formatted byte size (e.g. "421.45 MB" or "421,451,273 bytes").

    @param   precision   number of decimals to leave after converting to
                         maximum units
    @param   max_units   whether to convert value to corresponding maximum
                         unit, or leave as bytes and add thousand separators
    @param   with_units  whether to include units in result
    """
    size, formatted, unit = int(size), "0", "bytes"
    if size:
        byteunit = "byte" if 1 == size else "bytes"
        if max_units:
            UNITS = [byteunit, "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
            log = min(len(UNITS) - 1, math.floor(math.log(size, 1024)))
            formatted = "%.*f" % (precision, size / math.pow(1024, log))
            formatted = formatted.rstrip("0").rstrip(".")
            unit = UNITS[int(log)]
        else:
            formatted = "".join([x + ("," if i and not i % 3 else "")
                                 for i, x in enumerate(str(size)[::-1])][::-1])
            unit = byteunit
    return formatted + ((" " + unit) if with_units else "")


def format_exc(e):
    """Formats an exception as Class: message, or Class: (arg1, arg2, ..)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") # DeprecationWarning on e.message
        msg = to_unicode(e.message) if getattr(e, "message", None) \
              else "(%s)" % ", ".join(map(to_unicode, e.args)) if e.args else ""
    result = u"%s%s" % (type(e).__name__, ": " + msg if msg else "")
    return result


def plural(word, items=None, numbers=True, single="1", sep="", pref="", suf=""):
    """
    Returns the word as 'count words', or '1 word' if count is 1,
    or 'words' if count omitted.

    @param   items      item collection or count,
                        or None to get just the plural of the word
             numbers    if False, count is omitted from final result
             single     prefix to use for word if count is 1, e.g. "a"
             sep        thousand-separator to use for count
             pref       prefix to prepend to count, e.g. "~150"
             suf        suffix to append to count, e.g. "150+"
    """
    count   = len(items) if hasattr(items, "__len__") else items or 0
    isupper = word[-1:].isupper()
    suffix = "es" if word and word[-1:].lower() in "xyz" else "s" if word else ""
    if isupper: suffix = suffix.upper()
    if count != 1 and "y" == word[-1:].lower():
        word = word[:-1] + ("I" if isupper else "i")
    result = word + ("" if 1 == count else suffix)
    if numbers and items is not None:
        fmtcount = single if 1 == count else "".join([
            x + ("," if i and not i % 3 else "")
            for i, x in enumerate(str(count)[::-1])][::-1
        ]) if sep else str(count)
        fmtcount = pref + fmtcount + suf
        result = "%s %s" % (single if 1 == count else fmtcount, result)
    return result.strip()


def unique_path(pathname, suffix="%(ext)s_%(counter)s"):
    """
    Returns a unique version of the path. If a file or directory with the
    same name already exists, returns a unique version
    (e.g. "C:\config.sys_2" if ""C:\config.sys" already exists).

    @param   suffix  string to append, formatted with variables counter, ext
    """
    result = pathname
    if "linux2" == sys.platform and isinstance(result, unicode) \
    and "utf-8" != sys.getfilesystemencoding():
        result = result.encode("utf-8") # Linux has trouble if locale not UTF-8
    path, name = os.path.split(result)
    base, ext = os.path.splitext(name)
    if len(name) > 255: # Filesystem limitation
        name = base[:255 - len(ext) - 2] + ".." + ext
        result = os.path.join(path, name)
    counter = 2
    while os.path.exists(result):
        mysuffix = suffix % {"ext": ext, "counter": counter}
        name = base + mysuffix
        if len(name) > 255:
            name = base[:255 - len(mysuffix) - 2] + ".." + mysuffix
        result = os.path.join(path, name)
        counter += 1
    return result


def select_file(filepath):
    """
    Tries to open the file directory and select file.
    Falls back to opening directory only (select is Windows-only).
    """
    if not os.path.exists(filepath):
        return start_file(os.path.split(filepath)[0])
    try: subprocess.Popen('explorer /select, "%s"' % shortpath(filepath))
    except Exception: start_file(os.path.split(filepath)[0])


def add_unique(lst, item, direction=1, maxlen=sys.maxint):
    """
    Adds the item to the list from start or end. If item is already in list,
    removes it first. If list is longer than maxlen, shortens it.

    @param   direction  side from which item is added, -1/1 for start/end
    @param   maxlen     maximum length list is allowed to grow to before
                        shortened from the other direction
    """
    if item in lst:
        lst.remove(item)
    lst.insert(0, item) if direction < 0 else lst.append(item)
    if len(lst) > maxlen:
        lst[:] = lst[:maxlen] if direction < 0 else lst[-maxlen:]
    return lst


def make_unique(value, existing, suffix="_%s", counter=2, case=False):
    """
    Returns a unique string, appending suffix % counter as necessary.

    @param   existing  collection of existing strings to check
    @oaram   case      whether uniqueness should be case-sensitive
    """
    result, is_present = value, (lambda: result in existing)
    if not case:
        existing = [x.lower() for x in existing]
        is_present = lambda: result.lower() in existing
    while is_present(): result, counter = value + suffix % counter, counter + 1
    return result


def get(collection, *path, **kwargs):
    """
    Returns the value at specified collection path. If path not available,
    returns the first keyword argument if any given, or None.
    Collection can be a nested structure of dicts, lists, tuples or strings.
    E.g. util.get({"root": {"first": [{"k": "v"}]}}, "root", "first", 0, "k").
    Also supports named object attributes.
    """
    default = (list(kwargs.values()) + [None])[0]
    result = collection if path else default
    if len(path) == 1 and isinstance(path[0], list): path = path[0]
    for p in path:
        if isinstance(result, collections.Sequence):  # Iterable with index
            if isinstance(p, (int, long)) and p < len(result):
                result = result[p]
            else:
                result = default
        elif isinstance(result, collections.Mapping): # Container with lookup
            result = result.get(p, default)

        else:
            result = getattr(result, p, default)
        if result == default: break  # for p
    return result


def to_unicode(value, encoding=None):
    """
    Returns the value as a Unicode string. Tries decoding as UTF-8 if
    locale encoading fails.
    """
    result = value
    if not isinstance(value, unicode):
        encoding = encoding or locale.getpreferredencoding()
        if isinstance(value, str):
            try:
                result = unicode(value, encoding)
            except Exception:
                result = unicode(value, "utf-8", errors="replace")
        else:
            result = unicode(str(value), errors="replace")
    return result


def longpath(path):
    """Returns the path in long Windows form ("Program Files" not PROGRA~1)."""
    result = path
    try:
        buf = ctypes.create_unicode_buffer(65536)
        GetLongPathNameW = ctypes.windll.kernel32.GetLongPathNameW
        if GetLongPathNameW(unicode(path), buf, 65536):
            result = buf.value
        else:
            head, tail = os.path.split(path)
            if GetLongPathNameW(unicode(head), buf, 65536):
                result = os.path.join(buf.value, tail)
    except Exception: pass
    return result


def shortpath(path):
    """Returns the path in short Windows form (PROGRA~1 not "Program Files")."""
    if isinstance(path, str): return path
    from ctypes import wintypes

    ctypes.windll.kernel32.GetShortPathNameW.argtypes = [
        # lpszLongPath, lpszShortPath, cchBuffer
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD 
    ]
    ctypes.windll.kernel32.GetShortPathNameW.restype = wintypes.DWORD
    buf = ctypes.create_unicode_buffer(4 * len(path))
    ctypes.windll.kernel32.GetShortPathNameW(path, buf, len(buf))
    return buf.value


def win32_unicode_argv():
    """
    Returns Windows command-line arguments converted to Unicode.

    @from    http://stackoverflow.com/a/846931/145400
    """
    result = sys.argv[:]
    try:
        from ctypes import POINTER, byref, cdll, c_int, windll
        from ctypes.wintypes import LPCWSTR, LPWSTR
    except Exception: return result

    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    argc = c_int(0)
    argv = CommandLineToArgvW(GetCommandLineW(), byref(argc))
    if argc.value:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        result = [argv[i].encode("utf-8") for i in range(start, argc.value)]
    return result

# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

import os
import subprocess
import sys
import tempfile

from .environment import enforce_c_locale


def _fix_flags(flags):
    prefix = '--param '
    for flag in flags:
        if flag.startswith(prefix):
            yield '--param'
            yield flag[len(prefix):]
        else:
            yield flag


def run(gcc_command, flags, debug):
    tempdir = tempfile.mkdtemp()
    try:
        input_filename = os.path.join(tempdir, 'empty.c')
        with open(input_filename, 'w') as f:
            pass

        try:
            output_filename = os.path.join(tempdir, 'march_native.s')
            cmd = [
                gcc_command,
                '-S', '-fverbose-asm',
                '-o', output_filename,
                input_filename,
            ] + list(_fix_flags(flags))
            env = os.environ.copy()
            stderr = subprocess.DEVNULL
            enforce_c_locale(env)

            if debug:
                print('# %s' % ' '.join(cmd), file=sys.stderr)
                stderr = None  # i.e. forward to terminal

            try:
                subprocess.check_output(cmd, env=env, stderr=stderr)
            except OSError as e:
                e.strerror += ': "%s"' % gcc_command
                raise

            try:
                with open(output_filename) as f:
                    return f.read()
            finally:
                os.remove(output_filename)
        finally:
            os.remove(input_filename)
    finally:
        os.rmdir(tempdir)

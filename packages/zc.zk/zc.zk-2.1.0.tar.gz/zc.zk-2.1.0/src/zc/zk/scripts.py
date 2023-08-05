##############################################################################
#
# Copyright Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import logging
import optparse
import sys
import zc.zk
import kazoo.security

def world_acl(permission):
    return kazoo.security.ACL(permission, kazoo.security.ANYONE_ID_UNSAFE)

def export(args=None):
    """Usage: %prog [options] connection [path]
    """
    if args is None:
        args = sys.argv[1:]

    parser = optparse.OptionParser(export.__doc__)
    parser.add_option('-e', '--ephemeral', action='store_true')
    parser.add_option('-o', '--output')

    options, args = parser.parse_args(args)
    connection = args.pop(0)
    if args:
        [path] = args
    else:
        path = '/'

    logging.basicConfig(level=logging.WARNING)

    zk = zc.zk.ZooKeeper(connection)
    data = zk.export_tree(path, ephemeral=options.ephemeral)

    if options.output:
        with open(options.output, 'w') as f:
            f.write(data)
    else:
        print data,

    zk.close()

def import_(args=None):
    """Usage: %prog [options] connection [import-file [path]]

    Import a tree definition from a file.

    If no import-file is provided or if the import file is -, then
    data are read from standard input.
    """

    if args is None:
        args = sys.argv[1:]

    parser = optparse.OptionParser(import_.__doc__)
    parser.add_option('-d', '--dry-run', action='store_true')
    parser.add_option('-t', '--trim', action='store_true')
    parser.add_option(
        '-p', '--permission', type='int',
        default=kazoo.security.Permissions.ALL,
        help='ZooKeeper permission bits as integer,'
        ' kazoo.security.Permissions.ALL',
        )

    options, args = parser.parse_args(args)
    if not (1 <= len(args) <= 3):
        parser.parse_args(['-h'])

    connection = args.pop(0)
    if args:
        import_file = args.pop(0)
    else:
        import_file = '-'

    if args:
        [path] = args
    else:
        path = '/'

    logging.basicConfig(level=logging.WARNING)

    zk = zc.zk.ZooKeeper(connection)
    if import_file == '-':
        import_file = sys.stdin
    else:
        import_file = open(import_file)

    zk.import_tree(
        import_file.read(), path,
        trim=options.trim,
        dry_run=options.dry_run,
        acl=[world_acl(options.permission)],
        )

    zk.close()

def validate_(args=None):
    """Usage: %prog connection [file [path]]

    Validate a tree definition from a file.

    If no file is provided or if the import file is -, then
    data are read from standard input.
    """

    if args is None:
        args = sys.argv[1:]

    parser = optparse.OptionParser(import_.__doc__)
    options, args = parser.parse_args(args)
    if len(args) != 1:
        parser.parse_args(['-h'])
    if args:
        import_file = args.pop(0)
    else:
        import_file = '-'

    if import_file == '-':
        import_file = sys.stdin
    else:
        import_file = open(import_file)

    zc.zk.parse_tree(import_file.read())

    import_file.close()

def set_property(args=None):
    if args is None:
        args = sys.argv[1:]

    connection = args.pop(0)
    path = args.pop(0)
    zk = zc.zk.ZooKeeper(connection)

    def _property(arg):
        name, expr = arg.split('=', 1)
        return name, eval(expr, {})

    zk.properties(path).update(dict(map(_property, args)))

    zk.close()

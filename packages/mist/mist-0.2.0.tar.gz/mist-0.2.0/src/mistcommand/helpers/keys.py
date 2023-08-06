import sys

from prettytable import PrettyTable
from mistcommand.helpers.login import authenticate


def show_key(key):
    print "Name: %s" % key.id
    print

    print "Private key:"
    print key.private
    print

    print "Puclic key:"
    print key.public


def list_keys(client):
    keys = client.keys()
    if not keys:
        print "No keys found"
        sys.exit(0)

    x = PrettyTable(["Name", "Is Default"])
    for key in keys:
        x.add_row([key.id, key.is_default])

    print x


def key_action(args):

    client = authenticate()

    if args.action == 'add':
        name = args.name
        key_path = args.key_path
        auto = args.auto_generate

        if auto:
            private = client.generate_key()
        else:
            with open(key_path, "r") as f:
                private = f.read().strip("\n")

        client.add_key(key_name=name, private=private)
        print "Added key %s" % name
    elif args.action == 'list':
        list_keys(client)
    elif args.action == 'delete':
        keys = client.keys(id=args.key)
        key = keys[0] if keys else None
        if key:
            key.delete()
            print "Deleted %s" % key.id
        else:
            print "Cound not find key: %s" % args.key
            sys.exit(0)
    elif args.action == 'rename':
        key_name = args.key
        new_name = args.new_name

        keys = client.keys(id=key_name)
        key = keys[0] if keys else None

        if key:
            key.rename(new_name)
            print "Renamed key to %s" % new_name
        else:
            print "Could not find key: %s" % key_name
    elif args.action == 'display':
        key_name = args.key
        keys = client.keys(id=key_name)
        key = keys[0] if keys else None
        if key:
            show_key(key)
        else:
            print "Could not find key: %s" % key_name


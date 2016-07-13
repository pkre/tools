import sys
import json
import argparse
import binascii
import collections

import decoder


def trim(root, prune):
    """ Prunes the json object to simplify the output """
    if type(root) == bytes:
        try:
            return root.decode('ascii')
        except UnicodeDecodeError:
            return binascii.hexlify(root).decode('utf-8').upper()

    if type(root) == collections.defaultdict:
        for k, v in root.items():
            root[k] = trim(v, prune)
        return root

    if type(root) == list:
        if len(root) == 1 and prune:
            return trim(root[0], prune)
        else:
            return [trim(v, prune) for v in root]
        return root

    return root


def main(infile, outfile, prune):
    root = decoder.process(infile.read())
    root = trim(root, prune)
    json.dump(root, outfile, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', **{
        'type': argparse.FileType('rb'),
        'default': sys.stdin,
        'help': 'The protobuf dump file (default: stdin)',
    })

    parser.add_argument('-o', '--outfile', **{
        'type': argparse.FileType('w'),
        'default': sys.stdout,
        'help': 'The json output file (default: stdout)',
    })

    parser.add_argument('--no-prune', **{
        'action': 'store_false',
        'help': 'prune/cleanup the json output'
    })
    args = parser.parse_args()
    main(args.infile, args.outfile, args.no_prune)
    # main('pm0084.dat')

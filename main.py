#!/usr/bin/env python3

import argparse
import sys

def add_case():
    print('case added')

if __name__ == '__main__':
    # create parser for 'bchoc' and subparsers
    parser = argparse.ArgumentParser(prog='bchoc')
    subparsers = parser.add_subparsers(title='actions')

    add = subparsers.add_parser('add',
                          description='Add a new evidence item to the blockchain and associate it with the given case identifier. For users’ convenience, more than one item_id may be given at a time, which will create a blockchain entry for each item without the need to enter the case_id multiple times. The state of a newly added item is CHECKEDIN. The given evidence ID must be unique (i.e., not already used in the blockchain) to be accepted.')
    add.add_argument('-c',
                     type=str,
                     help='Specifies the case identifier that the evidence is associated with. Must be a valid UUID. When used with log only blocks with the given case_id are returned.')
    add.add_argument('-i',
                     type=str,
                     help='Specifies the evidence item’s identifier. When used with log only blocks with the given item_id are returned. The item ID must be unique within the blockchain. This means you cannot re-add an evidence item once the remove action has been performed on it.',
                     nargs='*')

    checkout = subparsers.add_parser('checkout',
                                     description='Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions may only be performed on evidence items that have already been added to the blockchain.')
    checkout.add_argument()


    args = parser.parse_args()

    if args.filename:

    else:
        sys.exit(-1)
#!/usr/bin/env python3

import argparse


def add(args):
    print('added')


def checkout(args):
    print('checked out')


def checkin(args):
    print('checked in')


def log(args):
    print('logged')


def remove(args):
    print('removed')


def init(args):
    print('initialized')


def verify(args):
    print('verified')


if __name__ == '__main__':
    # create parser for 'bchoc' and subparsers
    parser = argparse.ArgumentParser()
    parser.add_argument('bchoc')
    subparsers = parser.add_subparsers(title='actions')

    # add subparser
    bchoc_add = subparsers.add_parser('add',
                                      description='Add a new evidence item to the blockchain and associate it with the '
                                                  'given case identifier. For users’ convenience, more than one item_'
                                                  'id may be given at a time, which will create a blockchain entry for '
                                                  'each item without the need to enter the case_id multiple times. The '
                                                  'state of a newly added item is CHECKEDIN. The given evidence ID '
                                                  'must be unique (i.e., not already used in the blockchain) to be '
                                                  'accepted.')

    bchoc_add.add_argument('-c', dest='case_id', type=int, required=True,
                           help='Specifies the case identifier that the evidence is associated with. Must be a valid '
                                'UUID. When used with log only blocks with the given case_id are returned.')

    bchoc_add.add_argument('-i', dest='item_id', type=str, nargs='+', required=True,
                           help='Specifies the evidence item’s identifier. When used with log only blocks with the '
                                'given item_id are returned. The item ID must be unique within the blockchain.'
                                ' This means you cannot re-add an evidence item once the remove action has been '
                                'performed on it.')

    bchoc_add.set_defaults(func=add)

    # checkout subparser
    bchoc_checkout = subparsers.add_parser('checkout',
                                           description='Add a new checkout entry to the chain of custody for the given'
                                                       ' evidence item. Checkout actions may only be performed on '
                                                       'evidence items that have already been added to the blockchain.')

    bchoc_checkout.add_argument('-i', dest='item_id', type=str, required=True,
                                help='Specifies the evidence item’s identifier. When used with log only blocks with '
                                     'the given item_id are returned. The item ID must be unique within the blockchain.'
                                     ' This means you cannot re-add an evidence item once the remove action has been '
                                     'performed on it.')

    bchoc_checkout.set_defaults(func=checkout)

    # checkin subparser
    bchoc_checkin = subparsers.add_parser('checkin', description='Add a new checkout entry to the chain of custody '
                                                                 'for the given evidence item. Checkout actions may '
                                                                 'only be performed on evidence items that have already'
                                                                 ' been added to the blockchain.')

    bchoc_checkin.add_argument('-i', dest='item_id', type=str, required=True,
                               help='Specifies the evidence item’s identifier. When used with log only blocks with the '
                                    'given item_id are returned. The item ID must be unique within the blockchain. '
                                    'This means you cannot re-add an evidence item once the remove action has been '
                                    'performed on it.')

    bchoc_checkin.set_defaults(func=checkin)

    # log subparser
    bchoc_log = subparsers.add_parser('log', description='Display the blockchain entries giving the oldest first '
                                                         '(unless -r is given).')

    bchoc_log.add_argument('--reverse', '-r', default=False,
                           help='Reverses the order of the block entries to show the most recent entries first.')

    bchoc_log.add_argument('-n', dest='num_entries', type=int, nargs='*',
                           help='Shows num_entries number of block entries.')

    bchoc_log.add_argument('-c', dest='case_id', type=int, nargs='*',
                           help='Specifies the case identifier that the evidence is associated with. Must be a valid '
                                'UUID. When used with log only blocks with the given case_id are returned.')

    bchoc_log.add_argument('-i', dest='item_id', type=str, nargs='*',
                           help='Specifies the evidence item’s identifier. When used with log only blocks with the '
                                'given item_id are returned. The item ID must be unique within the blockchain. This '
                                'means you cannot re-add an evidence item once the remove action has been performed '
                                'on it.')

    bchoc_log.set_defaults(func=log)

    # remove subparser
    bchoc_remove = subparsers.add_parser('remove',
                                         description='Prevents any further action from being taken on the evidence item'
                                                     ' specified. The specified item must have a state of CHECKEDIN for'
                                                     ' the action to succeed.')

    bchoc_remove.add_argument('-i', dest='item_id', type=str, required=True,
                              help='Specifies the evidence item’s identifier. When used with log only blocks with the '
                                   'given item_id are returned. The item ID must be unique within the blockchain. This'
                                   ' means you cannot re-add an evidence item once the remove action has been performed'
                                   ' on it.')

    bchoc_remove.add_argument('--why', '-y', type=str, required=True,
                              help='Reason for the removal of the item from custody.')

    bchoc_remove.add_argument('-o', dest='owner', type=str,
                              help='Information about the lawful owner to whom the evidence was released. At this time,'
                                   ' text is free-form and does not have any requirements.')

    bchoc_remove.set_defaults(func=remove)

    # init subparser
    bchoc_init = subparsers.add_parser('init',
                                       description='Sanity check. Only starts up and checks for the initial block.')
    bchoc_init.set_defaults(func=init)

    # verify subparser
    bchoc_verify = subparsers.add_parser('verify', description='Parse the blockchain and validate all entries.')
    bchoc_verify.set_defaults(func=verify)

    args = parser.parse_args()
    args.func(args)

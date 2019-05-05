#!/usr/bin/env python3

import argparse
import os
import sys
import struct
import hashlib
import uuid
import maya


# TODO: fix the case related data structures

class Block:
    def __init__(self, previous_hash, case_id, evidence_id, state, data_length, data, timestamp=None):
        self.previous_hash = previous_hash
        if timestamp is None:
            self.timestamp = maya.now()._epoch
        else:
            self.timestamp = timestamp
        self.case_id = case_id
        self.evidence_id = evidence_id
        self.state = state
        self.data_length = data_length
        self.data = data
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha1()
        sha.update((str(self.previous_hash) +
                   str(self.timestamp) +
                   str(self.case_id) +
                   str(self.evidence_id) +
                   str(self.state) +
                   str(self.data_length) +
                   self.data).encode('utf-8'))
        return sha.hexdigest()

    def pack(self):
        return struct.pack('20s d 16s I 11s I',
                           self.previous_hash.encode(),
                           self.timestamp,
                           self.case_id.encode(),
                           self.evidence_id,
                           self.state.encode(),
                           self.data_length)


block_list = []
block_dict = {}
case_dict = {}
item_dict = {}
initialized = False


# TODO: checking if exists
def add(args):
    for i in range(len(args.item_id)):
        try:
            block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
            block = None

            while True:
                packed = block_file.read(68)
                if not packed:
                    break

                unpacked = struct.unpack('20s d 16s I 11s I', packed)

                previous_hash = unpacked[0]
                timestamp = unpacked[1]
                case_id = unpacked[2]
                evidence_id = unpacked[3]
                state = unpacked[4].decode().rstrip('\x00')
                data_length = unpacked[5]

                data = block_file.read(int(data_length)).decode()

                block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
                # block_list.append(block)
                # block_dict[block.previous_hash] = block

            block_file.close()

            block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'ab')
            block = Block(block.hash_block(), args.case_id, args.item_id[i], 'CHECKEDIN', 0, "")
            # block_list.append(initial_block)
            # block_dict[initial_block.previous_hash] = initial_block
            block_file.write(block.pack())
            block_file.write(block.data.encode())
            block_file.close()

        except FileNotFoundError:
            sys.exit(404)


def checkout(args):
    # TODO: check if the items exits, if it does then check if it has been checked out or not, if not create a block
    print(args)
    try:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
        block = None

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0]
            timestamp = unpacked[1]
            case_id = unpacked[2]
            evidence_id = unpacked[3]
            state = unpacked[4].decode().rstrip('\x00')
            data_length = unpacked[5]

            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            # block_list.append(block)
            # block_dict[block.previous_hash] = block

        block_file.close()

        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'ab')
        block = Block(block.hash_block(), "65cc391d-6568-4dcc-a3f1-86a2f04140f3", args.item_id, 'CHECKEDIN', 0, "")
        # block_list.append(initial_block)
        # block_dict[initial_block.previous_hash] = initial_block
        block_file.write(block.pack())
        block_file.write(block.data.encode())
        block_file.close()

    except FileNotFoundError:
        sys.exit(404)


def checkin(args):
    # TODO: check if the items exits, if it does then check if it has been checked out or not, if it has create a block
    print(args)
    try:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
        block = None

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0]
            timestamp = unpacked[1]
            case_id = unpacked[2]
            evidence_id = unpacked[3]
            state = unpacked[4].decode().rstrip('\x00')
            data_length = unpacked[5]

            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            # block_list.append(block)
            # block_dict[block.previous_hash] = block

        block_file.close()

        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'ab')
        block = Block(block.hash_block(), "65cc391d-6568-4dcc-a3f1-86a2f04140f3", args.item_id, 'CHECKEDIN', 0, "")
        # block_list.append(initial_block)
        # block_dict[initial_block.previous_hash] = initial_block
        block_file.write(block.pack())
        block_file.write(block.data.encode())
        block_file.close()

    except FileNotFoundError:
        sys.exit(404)


def log(args):
    # TODO: implement reverse
    print(args)
    try:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
        block = None

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0]
            timestamp = unpacked[1]
            case_id = unpacked[2]
            evidence_id = unpacked[3]
            state = unpacked[4].decode().rstrip('\x00')
            data_length = unpacked[5]

            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            # block_list.append(block)
            # block_dict[block.previous_hash] = block

        block_file.close()

        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'ab')
        data_field = args.reason
        if args.owner:
            data_field = data_field + args.owner
        block = Block(block.hash_block(), "65cc391d-6568-4dcc-a3f1-86a2f04140f3", args.item_id, 'CHECKEDIN', 0,
                      data_field)
        # print(block)
        block_file.write(block.pack())
        block_file.write(block.data.encode())
        block_file.close()

    except FileNotFoundError:
        sys.exit(404)


def remove(args):
    # TODO: check if the items exits, if it does then check if it has been checked out or not, if not create a block
    print(args)
    try:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
        block = None

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0]
            timestamp = unpacked[1]
            case_id = unpacked[2]
            evidence_id = unpacked[3]
            state = unpacked[4].decode().rstrip('\x00')
            data_length = unpacked[5]

            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            # block_list.append(block)
            # block_dict[block.previous_hash] = block

        block_file.close()

        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'ab')
        data_field = args.reason
        if args.owner:
            data_field = data_field + args.owner
        block = Block(block.hash_block(), "65cc391d-6568-4dcc-a3f1-86a2f04140f3", args.item_id, 'CHECKEDIN', 0, data_field)
        # block_list.append(initial_block)
        # block_dict[initial_block.previous_hash] = initial_block
        block_file.write(block.pack())
        block_file.write(block.data.encode())
        block_file.close()

    except FileNotFoundError:
        sys.exit(404)


def init(args):
    global initialized
    global block_list
    initialized = True

    try:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'rb')
        init_bytes = block_file.read(68)
        unpacked = struct.unpack('20s d 16s I 11s I', init_bytes)

        previous_hash = unpacked[0]
        assert previous_hash == bytearray(20)

        timestamp = unpacked[1]
        assert float(timestamp) < maya.now()._epoch

        case_id = unpacked[2]
        assert case_id == bytearray(16)

        evidence_id = unpacked[3]
        assert int(evidence_id) == 0

        state = unpacked[4].decode().rstrip('\x00')
        assert state == 'INITIAL'

        data_length = unpacked[5]
        assert int(data_length) == 14

        data = block_file.read(int(data_length)).decode()
        assert data == 'Initial block'

        initial_block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
        block_list.append(initial_block)
        block_dict[0] = initial_block
        print('Blockchain file found with INITIAL block.')

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0].decode()
            timestamp = unpacked[1]
            case_id = unpacked[2].decode()
            evidence_id = unpacked[3]
            state = unpacked[4].decode().rstrip('\x00')
            data_length = unpacked[5]
            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            block_list.append(block)
            block_dict[block.previous_hash] = block

        block_file.close()

    except FileNotFoundError:
        block_file = open(os.environ.get('ENRON_FILE', 'sample.block'), 'wb')
        initial_block = Block(None, None, 0, 'INITIAL', 14, 'Initial block')
        block_list.append(initial_block)
        block_dict[initial_block.previous_hash] = initial_block
        block_file.write(struct.pack('20s d 16s I 11s I', bytearray(20), initial_block.timestamp,
                                     bytearray(16), initial_block.evidence_id,
                                     initial_block.state.encode(), initial_block.data_length))
        block_file.write(initial_block.data.encode())
        block_file.close()
        print('Blockchain file not found. Created INITIAL block.')


# TODO: finish error checking
def verify(args):
    global block_list

    try:
        block_file = open(os.environ.get('ENRON_FILE', 'test003'), 'rb')

        if initialized:
            block_file.seek(68 + block_list[0].data_length)

        while True:
            packed = block_file.read(68)
            if not packed:
                break

            unpacked = struct.unpack('20s d 16s I 11s I', packed)

            previous_hash = unpacked[0]
            # if previous_hash not in block_dict:
            #     print("")

            timestamp = unpacked[1]

            case_id = unpacked[2]

            evidence_id = unpacked[3]

            state = unpacked[4].decode().rstrip('\x00')

            data_length = unpacked[5]

            data = block_file.read(int(data_length)).decode()

            block = Block(previous_hash, case_id, evidence_id, state, data_length, data, timestamp)
            block_list.append(block)
            block_dict[block.previous_hash] = block

        block_file.close()

    except FileNotFoundError:
        sys.exit(404)


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

    bchoc_add.add_argument('-c', dest='case_id', type=str , required=True,
                           help='Specifies the case identifier that the evidence is associated with. Must be a valid '
                                'UUID. When used with log only blocks with the given case_id are returned.')

    bchoc_add.add_argument('-i', dest='item_id', type=str, required=True, action='append',
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

    bchoc_log.add_argument('-c', dest='case_id', type=str, nargs='*',
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


"""
Test:
52 65 6d 65 6d 62 65 72 20 6d 65 20 61 74 20 65 61 63 68 20 64 61 79 27 73 20 64 61 77 6e 0a 41 73 20 74 68 65 20 73 75 
6e 6c 69 67 68 74 20 70 6c 61 79 73 20 61 6e 64 20 6d 65 6d 6f 72 69 65 73 20 64 72 61 77 6e 0a 49 20 61 6d 20 74 68 65 
20 6c 61 75 67 68 74 65 72 20 61 6e 64 20 74 68 65 20 67 6f 6c 64 65 6e 20 6c 69 67 68 74 0a 54 68 61 74 20 69 73 20 63 
61 72 72 69 65 64 20 6f 6e 20 74 68 65 20 77 69 6e 64 20 69 6e 20 67 65 6e 74 6c 65 20 66 6c 69 67 68 74 0a 46 65 65 6c 
20 6d 65 20 77 69 74 68 20 79 6f 75 20 63 6c 6f 73 65 20 62 79 20 79 6f 75 72 20 73 69 64 65 0a 52 65 6d 65 6d 62 65 72 
20 6d 65 20 61 73 20 6d 79 20 64 75 74 79 20 64 6f 6e 65 20 77 69 74 68 20 70 72 69 64 65 2e
"""
# BlockChain Of Custody
A block chain for "chain of custody"

## Description

The Chain of Custody form is a critical element to a forensic investigation by keeping this record,
examiners can show that the integrity of the evidence has been preserved and not open to compromise.
This project aims to digitize this process and implement blockchain technologies for the purpose of
integrity and non-repudiation. 

A Chain of Custody form keeps track of:

1. **Where** the evidence was stored.
2. **Who** had access to the evidence and **when**.
3. **What** actions were done to the evidence.



## Commands

| Identifiers | Description |
| ----------- | ----------- |
| -c case_id | Specifies the case identifier that the evidence is associated with. Must be a valid UUID. When used with `log` only blocks with the given `case_id` are returned.
| -i item_id | Specifies the evidence item's identifier. When used with `log` only blocks with the given `item_id` are returned. The item ID must be unique within the blockchain. This means you cannot re-add an evidence item once the `remove` action has been performed on it. |
| -r, --reverse | Reverses the order of the block entries to show the most recent entries first. |
| -n num_entries | When used with ``log``, shows ``num_entries`` number of block entries. |
| -y reason, --why reason | Reason for the removal of the evidence item. Must be one of: `DISPOSED`, `DESTROYED`, or `RELEASED`. If the reason given is `RELEASED`, `-o` must also be given. |
| -o owner | Information about the lawful owner to whom the evidence was released. At this time, text is free-form and does not have any requirements. |

### Adding an item

Add a new evidence item to the blockchain and associate it with the given case identifier. For users' convenience, more than one item_id may be given at a time, which will create a blockchain entry for each item without the need to enter the case_id multiple times. The state of a newly added item is `CHECKEDIN`. The given evidence ID must be unique (i.e., not already used in the blockchain) to be accepted.

Usage:
```
bchoc add -c case_id -i item_id [-i item_id ...]
```

Adding two new evidence items to a case:

```
$ bchoc add -c 65cc391d-6568-4dcc-a3f1-86a2f04140f3 -i 987654321 -i 123456789
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Added item: 987654321
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:13:07.820445Z
Added item: 123456789
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:13:07.820445Z
```

Adding the same two evidence items, but one at a time (semantically equivalent to the above example):

```
$ bchoc add -c 65cc391d65684dcca3f186a2f04140f3 -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Added item: 987654321
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:14:09.750755Z
$ bchoc add -c 135312414559765810732748806252319031539 -i 123456789
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Added item: 123456789
  Status: CHECKEDIN
  Time of action: 2019-01-22T03:14:15.248161Z
```


### Checking out an item

Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions may only be performed on evidence items that have already been added to the blockchain.

Usage:
```
bchoc checkout -i item_id
```

Checking out an evidence item:

```
$ bchoc checkout -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Checked out item: 987654321
  Status: CHECKEDOUT
  Time of action: 2019-01-22T03:22:04.220451Z
```


### Checking in an item

Add a new checkin entry to the chain of custody for the given evidence item. Checkin actions may only be performed on evidence items that have already been added to the blockchain.

Usage:
```
bchoc checkin -i item_id
```

Checking in an evidence item:
```
$ bchoc checkin -i 987654321
	Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
	Checked in item: 987654321
  Status: CHECKEDIN
	  Time of action: 2019-01-22T03:24:25.729411Z
```


### Displaying the log

Display the blockchain entries giving the oldest first (unless `-r` is given).

Usage:
```
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
```

Looking at the last 2 entries in the log:
```
$ bchoc log -r -n 2 -i 987654321
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Item: 987654321
Action: CHECKEDIN
Time: 2019-01-22T03:24:25.729411Z

Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Item: 987654321
Action: CHECKEDOUT
Time: 2019-01-22T03:22:04.220451Z
```


### Removing an item

Prevents any further action from being taken on the evidence specified. The specified item must have a state of `CHECKEDIN` for the action to succeed.

Usage:
```
bchoc remove -i item_id -y reason [-o owner]
```

Removing an item:
```
$ bchoc remove -i 987654321 -y RELEASED -o "John Doe, 123 Cherry Ln, Apple, CA 12345, 123-XXX-4567"
Case: 65cc391d-6568-4dcc-a3f1-86a2f04140f3
Removed item: 987654321
  Status: RELEASED
  Owner info: John Doe, 123 Cherry Ln, Apple, CA 12345, 123-XXX-4567
  Time of action: 2019-01-22T03:24:25.729411Z
```


### Initializing a new log

Starts up and checks for the initial block.

Usage:
```
bchoc init
```

Verifying the blockchain:
```
$ bchoc verify
Transactions in blockchain: 6
State of blockchain: CLEAN
```


### Verifying

Parses the blockchain and validates all entries.

Usage:
```
bchoc verify
```

Verifying the blockchain when it has errors:
```
$ bchoc verify
Transactions in blockchain: 6
State of blockchain: ERROR
Bad block: ca53b1f604b633a6bc3cf75325932596efc4717f
Parent block: NOT FOUND
```

## Structure

Every block in the blockchain will have the same structure:

| Length (bits) | Field Name - Description |
| ------------- | ------------------------ |
| 128           | Index - Must be a valid UUID |
| 160           | Previous Hash - SHA-1 hash of this block's parent |
| 64            | Timestamp - Regular Unix timestamp. Must be printed in ISO |8601 format anytime displayed to user. |
| 128           | Case ID - UUID stored as an integer. |
| 32            | Evidence Item ID - 4-byte integer. |
| 88            | State - Must be one of: `CHECKEDIN`, `CHECKEDOUT`, `DISPOSED`, `DESTROYED`, or `RELEASED`. |
| 32            | Data Length (byte count) - 4-byte integer. |
| 0 to (2^32)*8 | Data - Free form text with byte length specified in `Data Length`. |

All timestamps must be stored in UTC and account for the difference between local time and UTC.

## Credits

Assignment created by [Mike Mabey](https://mikemabey.com/)
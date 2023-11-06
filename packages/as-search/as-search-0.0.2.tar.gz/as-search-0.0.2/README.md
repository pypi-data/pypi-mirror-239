# as-search

Search info in Autonomous System database

## Example

```
$ as-search ip 8.8.8.8
8.8.8.8 8.8.8.0 8.8.8.255 US GOOGLE
```

```
 as-search ip 8.8.8.8 -j
{"target": "8.8.8.8", "asn": 15169, "organization": "GOOGLE", "country": "US", "start_ip": "8.8.8.0", "end_ip": "8.8.8.255"}
```

## Installation

```
pip install as-search
```

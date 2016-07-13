# Misc Tools
Some simple quality of life tools

## Protocol Buffer Dumper
The dumper.py file takes a raw binary dump file and converts it to JSON.

Due to the ambiguous raw format of protocol buffers, the json output will not match the original format 100%, but should be pretty accurate.

```bash
# convert dump file to json
python3 dumper.py -i packet.bin --o packet.json
```

> INFO: There are several decoding defaults do to the ambiguities in the wire protocol:
> 1. varints are decoded to int32/int64
> 1. 64bits are decoded to doubles
> 1. 32bits are decoded to floats
> 1. bytes are decoded to ascii if possible, otherwise dumped as hex
>
> SEE: https://developers.google.com/protocol-buffers/docs/encoding

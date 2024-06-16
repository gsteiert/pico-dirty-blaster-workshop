#!/usr/bin/env python3
import sys
import struct
import subprocess
import re
import os
import os.path
import argparse
import json
from time import sleep


UF2_MAGIC_START0 = 0x0A324655 # "UF2\n"
UF2_MAGIC_START1 = 0x9E5D5157 # Randomly selected
UF2_MAGIC_END    = 0x0AB16F30 # Ditto

jbchdraddr = 0x20000
jbcspeed = 1000000
familyid = 0x0
jbcaction = b""
jbcfilename = b""
jbcdescription = b""


def convert_to_uf2(uf2_content, jbc_content):
    global jbchdraddr, familyid, jbcaction, jbcdescription, jbcfilename, jbcspeed

    datapadding = b""
    while len(datapadding) < 512 - 256 - 32 - 4:
        datapadding += b"\x00\x00\x00\x00"

    uf2_blocks_in = len(uf2_content) // 512
    if (uf2_blocks_in % 16) == 0:
        uf2_blocks_out = uf2_blocks_in
    else:
        uf2_blocks_out = uf2_blocks_in + 16 - (uf2_blocks_in % 16)
    jbc_blocks = ((len(jbc_content) + 255) // 256)
    numblocks = uf2_blocks_out + jbc_blocks + 1
    outp = []

    currfamilyid = None
    all_families_same = True
    prev_flag = None
    all_flags_same = True
    uf2_high_addr = 0

    for blockno in range(uf2_blocks_in):
        ptr = blockno * 512
        block = uf2_content[ptr:ptr + 512]
        hdi = struct.unpack(b"<IIIIIIII", block[0:32])
        if hdi[0] != UF2_MAGIC_START0 or hdi[1] != UF2_MAGIC_START1:
            print("Skipping block at " + ptr + "; bad magic")
            continue
        if hdi[2] & 1:
            # NO-flash flag set; skip block
            continue
        datalen = hdi[4]
        if datalen > 476:
            assert False, "Invalid UF2 data size at " + ptr
        if datalen < 256:
            print("Short block at block #%d\n", hdi[5])

        hdo = struct.pack(b"<IIIIIIII", hdi[0], hdi[1], hdi[2], hdi[3], hdi[4], hdi[5], numblocks, hdi[7])
        outp.append(hdo)
        outp.append(block[32:512])

        if prev_flag == None:
            prev_flag = hdi[2]
        if prev_flag != hdi[2]:
            all_flags_same = False
        if currfamilyid == None:
            currfamilyid = hdi[7]
        if currfamilyid != hdi[7]:
            all_families_same = False
        if (hdi[3]+hdi[4]-1) > uf2_high_addr:
            uf2_high_addr = hdi[3]+hdi[4]-1

    print("--- UF2 File Header Info ---")
    print("Highest address written:  0x{:08x}".format(uf2_high_addr))
    if all_families_same:
        print("All family values consistent, 0x{:04x}".format(hdi[7]))
        familyid = hdi[7]
    else:
        error("Families were not all the same")
    if all_flags_same:
        print("All block flag values consistent, 0x{:04x}".format(hdi[2]))
        flags = hdi[2]
    else:
        error("Flags were not all the same")
    print("----------------------------")


# Flash sector erase size for pico board is 4096.  Need to pad or writing will stop
# TBD enter dummy data, don't reuse last buffer
    blockno = uf2_blocks_in
    lastaddr = hdi[3]
    print("Last Address (pre padding):  0x{:04x}".format(lastaddr))
# Init dummy chunks for padding
    chunk = b"\x00"
    while len(chunk) < 256:
        chunk += b"\x00"
# Add padding blocks
    while (blockno < uf2_blocks_out):
        lastaddr += 256
        hdo = struct.pack(b"<IIIIIIII", hdi[0], hdi[1], hdi[2], lastaddr, 256, blockno, numblocks, hdi[7])
        block = hdo + chunk + datapadding + struct.pack(b"<I", UF2_MAGIC_END)
        assert len(block) == 512
        outp.append(block)
        blockno += 1
    print("Last Address (post padding): 0x{:04x}".format(lastaddr))

# Create JUF2 Header Block
    chunk = struct.pack(b"<IIIIII16s32s128s", 0x3246554A, 0, 
          len(jbc_content), (jbchdraddr + 256), jbcspeed, 0, jbcaction.encode('utf-8'), 
          jbcfilename.encode('utf-8'), jbcdescription.encode('utf-8')) 

    hdo = struct.pack(b"<IIIIIIII",
        UF2_MAGIC_START0, UF2_MAGIC_START1,
        flags, jbchdraddr, 256, blockno, numblocks, familyid)
    while len(chunk) < 256:
        chunk += b"\x00"
    block = hdo + chunk + datapadding + struct.pack(b"<I", UF2_MAGIC_END)
    assert len(block) == 512
    outp.append(block)

# Add JBC Blocks
    for jbcblock in range(0, jbc_blocks):
        blockno += 1
        ptr = 256 * jbcblock
        chunk = jbc_content[ptr:ptr + 256]
        hdo = struct.pack(b"<IIIIIIII",
            UF2_MAGIC_START0, UF2_MAGIC_START1,
            flags, (ptr + jbchdraddr + 256), 256, blockno, numblocks, familyid)
        while len(chunk) < 256:
            chunk += b"\x00"
        block = hdo + chunk + datapadding + struct.pack(b"<I", UF2_MAGIC_END)
        assert len(block) == 512
        outp.append(block)

    return b"".join(outp)

def write_file(name, buf):
    with open(name, "wb") as f:
        f.write(buf)
    print("Wrote %d bytes to %s" % (len(buf), name))


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def main():
    global jbchdraddr, familyid, jbcaction, jbcdescription, jbcfilename, jbcspeed
    parser = argparse.ArgumentParser(description='Convert to UF2 or flash directly.')
    parser.add_argument('-a', '--action', dest='action', type=str,
                        default="PROGRAM",
                        help='set action to perform (default: PROGRAM')
    parser.add_argument('-b', '--base', dest='base', type=str,
                        default="0x20000",
                        help='set address of JUF2 header (default: 0x20000)')
    parser.add_argument('-d', '--description', dest='desc', type=str,
                        default="",
                        help='optional description of the JUF2')
    parser.add_argument('-f', '--family', dest='family', type=str,
                        default="0x0",
                        help='specify familyID - number or name (default: 0x0)')
    parser.add_argument('-u', '--uf2', metavar="FILE", dest='uf2', type=str,
                        help='uf2 input file')
    parser.add_argument('-j', '--jbc', metavar="FILE", dest='jbc', type=str,
                        help='jbc input file')
    parser.add_argument('-o', '--output', metavar="FILE", dest='output', type=str,
                        help='write output to named file; defaults to "flash.uf2" or "flash.bin" where sensible')
    parser.add_argument('-s', '--speed', dest='speed', type=str,
                        help='set JTAG speed in Hz')
    parser.add_argument('-i', '--info', action='store_true',
                        help='display header information from UF2, do not convert')
    args = parser.parse_args()

    jbchdraddr = int(args.base, 0)

#    families = load_families()

    if not args.uf2:
        error("Need input uf2 file")
    with open(args.uf2, mode='rb') as fu:
        uf2buf = fu.read()

    if not args.jbc:
        error("Need input jbc file")
    with open(args.jbc, mode='rb') as fj:
        jbcbuf = fj.read()
    jf = args.jbc.rpartition("/")
    jbcfilename = jf[-1]

    if not args.output:
        error("Need output file")

    if args.speed:
        jbcspeed = int(args.speed, 0)

    if args.action:
        jbcaction = args.action

    if args.desc:
        jbcdescription = args.desc

    outbuf = convert_to_uf2(uf2buf, jbcbuf)
    write_file(args.output, outbuf)


if __name__ == "__main__":
    main()

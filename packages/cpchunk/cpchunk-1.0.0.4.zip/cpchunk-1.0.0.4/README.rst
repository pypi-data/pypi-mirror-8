=========
 cpchunk
=========

What it is
==========
cpchunk ("copy chunk") copies binary data from one file and inserts it into (or replaces) another file. Specifically, it copies *len* bytes from *offset1* in file A into *offset2* in file B. It can also append to file B or replace file B instead. Thus, cpchunk can be thought of as a copy tool for parts of files rather than whole files.

**WARNING:** cpchunk generally assumes you know what you're doing. It can be quite easy to overwrite more data than you intended, or to truncate a file that you wanted to update. We cannot take any responsibility for anything that happens while using the program, whether it is working correctly or not. As with any tool, back up your data if you don't want to lose it!


What it's good for
==================
cpchunk was written as a ROM hacking tool, but it has no behavior specific to dealing with ROMs. Any time you want to copy (part of) a file into (part of) another file, cpchunk is your tool.

Here is a real-world example. The arcade game Donkey Kong stores its main program code from 0x0000 to 0x3fff in memory space. However, this code must be split across four different ROM files:

* 0x0000-0fff is stored in c_5et_g.bin
* 0x1000-1fff is stored in c_5ct_g.bin
* 0x2000-2fff is stored in c_5bt_g.bin
* 0x3000-3fff is stored in c_5at_g.bin

Since these blocks are contiguous, a programmer making a ROM for this hardware would probably prefer to create a single 16 KB ROM named, say, dkong.bin, then split the ROM into four afterward. To perform this split, the programmer would run the following commands::

    cpchunk -s 0x0000 -l 0x1000 dkong.bin c_5et_g.bin
    cpchunk -s 0x1000 -l 0x1000 dkong.bin c_5ct_g.bin
    cpchunk -s 0x2000 -l 0x1000 dkong.bin c_5bt_g.bin
    cpchunk -s 0x3000 -l 0x1000 dkong.bin c_5at_g.bin

The ``-s`` option defines the source offset to copy from, and the ``-l`` option defines the length of the chunk to copy. So the lines can be read as "Extract 0x1000 bytes from dkong.bin starting at 0x0000 and put them into c_5et_g.bin", and so forth.

Suppose instead the programmer were making a ROM for Donkey Kong Junior hardware. The ROM map for this hardware is rather stranger:

* djr1-c_5b_f-2.5b contains 0x0000-0fff, then 0x3000-3fff
* djr1-c_5c_f-2.5c contains 0x2000-27ff, then 0x4800-0x4fff, then 0x1000-0x17ff, then 0x5800-0x5fff
* djr1-c_5e_f-2.5e contains 0x4000-47ff, then 0x2800-0x2fff, then 0x5000-0x57ff, then 0x1800-0x1fff

Bizarre, isn't it? But it's no trouble for cpchunk. Here are the commands::

    cpchunk -s 0x0000 -l 0x1000 dkongjr.bin djr1-c_5b_f-2.5b
    cpchunk -s 0x3000 -l 0x1000 dkongjr.bin -a djr1-c_5b_f-2.5b
    cpchunk -s 0x2000 -l 0x800 dkongjr.bin djr1-c_5c_f-2.5c
    cpchunk -s 0x4800 -l 0x800 dkongjr.bin -a djr1-c_5c_f-2.5c
    cpchunk -s 0x1000 -l 0x800 dkongjr.bin -a djr1-c_5c_f-2.5c
    cpchunk -s 0x5800 -l 0x800 dkongjr.bin -a djr1-c_5c_f-2.5c
    cpchunk -s 0x4000 -l 0x800 dkongjr.bin djr1-c_5e_f-2.5e
    cpchunk -s 0x2800 -l 0x800 dkongjr.bin -a djr1-c_5e_f-2.5e
    cpchunk -s 0x5000 -l 0x800 dkongjr.bin -a djr1-c_5e_f-2.5e
    cpchunk -s 0x1800 -l 0x800 dkongjr.bin -a djr1-c_5e_f-2.5e

Here the ``-a`` option is used to append to the destination file. Note that the ``-a`` option does not have to be placed before the destination filename, but its role seems clearest there.


How to install
==============
The preferred method if you have a Python 3.4 or later is to type ``pip install cpchunk`` at the command line.


How to use
==========
Typing ``cpchunk -h`` should be sufficient to grasp the parameters. Here are some examples.

Ripping a file from 0x1000 to 0x1fff inclusive::

    cpchunk -s 0x1000 -l 0x1000 src.bin ripped.bin

In this case, since no destination offset is specified, cpchunk will replace rather than modify ripped.bin.

Ripping a file from 0x1000 to 0x1fff inclusive and inserting it into another file at 0x800::

    cpchunk -s 0x1000 -l 0x1000 src.bin -d 0x800 dest.bin

In this case, if dest.bin does not already exist, the program will raise an error. ``touch`` the file (or create it by some other means) if you really want to insert into an empty file.

Ripping a file from 0x1000 to 0x1fff inclusive and appending it to the end of another file::

    cpchunk -s 0x1000 -l 0x1000 src.bin -a dest.bin

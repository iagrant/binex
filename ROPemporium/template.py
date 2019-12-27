#!/usr/bin/env python3

from pwn import *

#ALWAYS DEBUG!
context.log_level='DEBUG'
context(terminal=['tmux','new-window'],os='linux',arch='amd64')
#context(terminal=['tmux','new-window'],os='linux',arch='i386')
p = gdb.debug('./binary','b main')
#p = process('./binary')

junk = ("A"* 40).encode()

p.recvuntil('>')
p.sendline(junk)
p.interactive()
#flag = p.recvline()
#log.success("Flag: "+flag.decode('ascii'))

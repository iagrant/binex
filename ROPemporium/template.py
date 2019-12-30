#!/usr/bin/env python3

from pwn import *

#ALWAYS DEBUG!
context.log_level='DEBUG'
context(terminal=['tmux','new-window'],os='linux',arch='amd64')
#context(terminal=['tmux','new-window'],os='linux',arch='i386')
p = gdb.debug('./binary','b main')
#p = process('./binary')

junk = ("A"* 40).encode()
payload = junk
log.info('Payload length: %i'%len(payload))
p.recvuntil('>')
log.info('Sending payload')
p.sendline(payload)
log.info('Payload Sent')
p.interactive()
#flag = p.recvline()
#log.success("Flag: "+flag.decode('ascii'))

# SPLIT


## 32 bit

Once again fire up gef-gdb and locate the offset needed to file the buffer. `44 bytes` once again!

If we fire up ghidra and look at the disasm and the decompiled sections we see that sadly there is no magical function for us to call and win.
We actually have to try and do something.

### Useful Function & String

But there's still hope!
There's this cool useful function waiting to be used but sadly its got a gross parameter of `/bin/ls`
![usefulFunction](imgs/32bit/usefulFunction.png)

Luckily there's also a useful string for us to use. Go into ghidra and search for `bin` in program text then data values and you'll get:
```
0804a030	usefulString	Global	ds "/bin/cat flag.txt"
```

You can also see it by just navigating to the `.data` section of the code
![usefulString](imgs/32bit/usefulString.png)

### Puting it all together

Alright s now that we have both a usefulFunction and a usefulString we can make some magic.

Payload:

```python
junk = ("A"* 44).encode()
system = p32(0x8048657)
#system = p32(0x8048430)
cat = p32(0x804a030)
payload = system+arg
```

We need the 44 bytes of junk to overflow the buffer so then the adress of where system gets called can overflow into $eip and change the flow of the program

Then after system address is pushed on the stack we push the address of the useful string aka `/bin/cat flag.txt` onto it so when we go to the `system` function call it'll pull `/bin/cat flag.txt` as the argument off the stack

![syscall](imgs/32bit/syscall)

## 64 bit
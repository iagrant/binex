# RET2WIN


## 32 bit

### Buffer Overflow

Using gef/gdb to find how larget the bufer is by making a de Bruijn cyclic pattern.
Which is a pattern that doesn't repeat so the program can easily find the exact spot that breaks the binary.

I created a pattern of length 50 to see where the buffer breaks

![pattern](32bit/imgs/pattern.png)

Looking at the registers we can see that the input spilled out of the intended buffer and into $eip (the index pointer which is the register that holds the current instructon ie the current step in the code)

![registers](32bit/imgs/registers.png)


Using the following command gef can nicely give us the offset needed to break the buffer.

![offset](32bit/imgs/offset.png)

Now that we are able to bump $eip and take control of where the program goes we need to find where we want it to go

Looking at all the functions in the file we find one that isn't called by main and isn't just a normal C function `ret2win`

![functions](32bit/imgs/functions.png)

If we open it up in ghidra we get a pretty cool decompiled view of the function, showing exactly what it does.

![decompiled](32bit/imgs/ret2winDecompiled.png)

From the gdb output we can see the address of the function `0x08048659`

If we append that address to the end of the 44 bytes of garbage then the address of ret2win will overwrite $eip.

Allowing us to changing the flow of the program to do what we want instead of what was intended.

This is the basic principle of Return Oriented Programming (ROP), overflow the buffer and take controle of the instruction pointer, after that it gets a lot more complicated but that is the extreme basics.

We can combine the junk 44 bytes and our 'payload' contain the address of the function we want to into a nice python [script](exploit32.py)

![flag](32bit/imgs/flag.png)

## 64 bit

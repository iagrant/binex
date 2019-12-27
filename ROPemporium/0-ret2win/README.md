# RET2WIN - The First Step of ROP

## 32 bit

### Finding the Buffer Size

Use gef/gdb to find how larget the bufer is by making a de Bruijn cyclic pattern.

A de Bruijn cyclic pattern is a pattern that doesn't repeat so the program can easily find the exact spot that breaks the binary.

I used a pattern of length 50 to see where the buffer breaks

![pattern](imgs/32bit/pattern.png)

Looking at the registers we can see that the input spilled out of the intended buffer and into $eip
- $eip is the index pointer which is the register that holds the current instructon ie the current step in the code

![registers](imgs/32bit/registers.png)


Using the following command gef can nicely give us the offset needed to break the buffer.

![offset](imgs/32bit/offset.png)

### Modifing the Instruction Pointer

Now that we are able to bump $eip and take control of where the program goes we need to find where we want it to go

Looking at all the functions in the file we find one that isn't called by main and isn't just a normal C function `ret2win`

![functions](imgs/32bit/functions.png)

If we open it up in ghidra we get a pretty cool decompiled view of the function, showing exactly what it does.

And perfect! We want to cat the flag.txt file.

![decompiled](imgs/32bit/ret2winDecompiled.png)

From the gdb output we can see the address of the function `0x08048659`

If we append that address to the end of the 44 bytes of garbage then the address of ret2win will overwrite $eip.

Allowing us to changing the flow of the program to do what we want instead of what was intended.

This is the basic principle of Return Oriented Programming (ROP), overflow the buffer and take controle of the instruction pointer, after that it gets a lot more complicated but that is the extreme basics.

We can combine the junk 44 bytes and our 'payload' contain the address of the function we want to into a nice python [script](exploit32.py)

![flag](imgs/32bit/flag.png)

## 64 bit

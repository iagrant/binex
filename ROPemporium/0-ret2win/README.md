# RET2WIN


## 32 bit

### Buffer Overflow

Using gef/gdb to find how larget the bufer is by making a de Bruijn cyclic pattern.
Which is a pattern that doesn't repeat so the program can easily find the exact spot that breaks the binary.

I created a pattern of length 50 to see where the buffer breaks

![pattern](pattern.png)

Looking at the registers we can see that the input spilled out of the intended buffer($eax) and into $eip

[registers][registers.png]


Using the following command gef can nicely give us the offset needed to break the buffer.
[offset][offset.png]


## 64 bit

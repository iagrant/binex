# badchars


## 32bit


## 64bit

Like always check the buffer we know it is 40bytes but its always good to be safe.

Running it we see some pretty bad news
```
badchars are: b i c / <space> f n s
```
Which eliminates `/bin` from our ropchain and any opcodes that happen to have the same bytes as the above chars

Converting them to hex so later we can give the bad bytes to ropper so it avoids them
```
0x62, 0x69, 0x63, 0x2f, 0x20, 0x66, 0x6e, 0x73
```

### Avoiding Bad Chars


Luckily ROPEmporium was nice and left a hint in the symbol table of the ELF

![hint](imgs/64bit/usefulGadget.png)

If they weren't that nice we could have also found that gadget and other useful gadgets by using ropper which is covered in **Finding Gadgets** section below

So now that we know we have a nice XOR gadget to be used we need to XOR the badchars in `/bin/cat flag.txt` with a key in this instance a single letter since its
```
xor byte ptr [r15], r14b; ret;
```
This XORs a single byte in r15 with the low/first byte of r14

So our XOR key will just be a single letter

Using [xor.py](xor.py) a quick and dirty script made to help find a key that didn't produce any badchars

The key doesn't have to be the same for all of them. I just did for convience.

```
"/bin/cat flag.txt" XOR "D" = "k&-*k'atd"lag.txt"
```

Now that we can disguise our favorite string we can move on to creating the payload

### Creating the Payload

The payload is gonna have 3 parts
1) loading the string to memory
2) modifying the string in memory
3) loading the string into system call

#### Finding Gadgets

ropper is a super handy gadget finder that gef uses to locate ROP gadgets. It's general usage is as follows
- A 'gadget' in ROP terms is a string of asm operations followed by a ret call so it can be chained or returned into the next part of the ropchain
- `--search` uses a regex to find your query in the asm's opcodes ex: `--search "pop rdi"` will return gadgets that contain `pop rdi`
- `-b` is used to specify bad bytes, which is critical for this challenge

```
ropper --search $QUERY -b 6269632f20666e73 #-b is bad bytes and the number is all the bad bytes above just lumped together
```

#### Loading the String

Searching by `mov qword` we get

```
0x0000000000400b34: mov qword ptr [r13], r12; ret;
```

Searching for `pop r12` we get:

```
0x0000000000400b3b: pop r12; pop r13; ret;
```

Using these two gadgets we are able to take our string off the stack and into memory. But we can't use a lot of chars so whats the point!?

Even if we can write to memory it'll be missing chars so it'll just be garbage. But luckily we disguised our favorite string in the previous section
- The important thing is that it doesn't have any of the previously stated bad chars

We also need to find somewhere to place the string into memory. We can find this by looking at the ELF's sections. Using `rabin2` from radare2
```
rabin2 -S badchars
```
![data section](imgs/64bit/data.png)

```
data_start = 0x601080 # pop_r12_r13 = p64(0x400b3b)
mov_r13_r12 = p64(0x400b34)
load_str_1 = pop_r12_r13 + bin_cat + p64(data_start) + mov_r13_r12
load_str_2 = pop_r12_r13 + flag_txt + p64(data_start+0x8) + mov_r13_r12
load_str_3 = pop_r12_r13 + last_bit + p64(data_start+0x10) + mov_r13_r12
load_str = load_str_1 + load_str_2 + load_str_3
```
I'm using .bss(0x601080) instead of .data(0x601070) because the third char for the string would have landed at 0x601073 which ends in a bad char 0x73 aka 's'

You could off set it by one and have the start be 0x601071 so then the third char is 0x601074 instead of 0x601073 it really doesn't matter.

But throught this whole challenge be aware of the bad chars and if something isn't working but it definately should then it's probably bad chars.

Test and get this part working before moving on.

![loaded string](imgs/64bit/loadedString.png)

#### Modifing the String

Now that the string is load


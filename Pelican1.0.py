ver = '0.1' ##Version Number
#  _____           _   _                        
# |  __ \         | | (_)                       
# | |__) |   ___  | |  _    ___    __ _   _ __  
# |  ___/   / _ \ | | | |  / __|  / _` | | '_ \ 
# | |      |  __/ | | | | | (__  | (_| | | | | |
# |_|       \___| |_| |_|  \___|  \__,_| |_| |_|
# Steven Rakhmanchik (C) 2019
# -------------------------------------------------------------------
#This work is licensed under a
#Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
#International License.
# -------------------------------------------------------------------
from PIL import Image, ImageDraw
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import textwrap
import sys

##INCLUDED FOR FUTURE VERSIONS INCLUDING AES ENCRYPTION SUPPORT
##import hashlib
##import pyaes

scan_factor = 5

def Encrypt(save_name):
    w = int(2200 / scan_factor)
    h = int(1700 / scan_factor)
    binary = []
    length = []
    rich_txt = ''

    Tk().withdraw()
    filename = askopenfilename()

    file = open(filename,"r")
    raw_txt = str(file.read())
    raw_txt = ' '.join(format(ord(i), 'b') for i in raw_txt)
    for word in raw_txt.split():
        if len(word) < 10:
            binary.append(''.join(format(ord(str(len(word))), 'b')))
            binary.append(word)
    rich_txt = ''
    for i in binary:
        rich_txt = rich_txt + i
    rich_txt = rich_txt.replace(" ", "")
    len_bin = str(len(rich_txt))
    len_len_bin = str(len(len_bin))
    rich_txt = ''.join(format(ord(i), 'b') for i in len_bin) + rich_txt
    rich_txt = ''.join(format(ord(len_len_bin), 'b')) + rich_txt
    
    im = Image.new('1', (h, w), 0xffffff)
    loc = 0
    pixels = im.load()
    for x in range(0,w):
        for y in range(0,h):
            if loc >= len(rich_txt) or y >= h or x >= w:
                im.save(save_name + '.png')
                break
            if (rich_txt[loc] == "1"):
                pixels[y,x] = 0
            if (rich_txt[loc] == "0"):
                pixels[y,x] = 1
            loc = loc + 1
        if loc >= len(rich_txt) or y >= h or x >= w:
            im.save(save_name + '.png')
            break
    im.save(save_name + '.png')

def Decrypt(save_name):
    w = int(2200 / scan_factor)
    h = int(1700 / scan_factor)
    data = ''
    Tk().withdraw()
    filename = askopenfilename()
    im = Image.open(filename)
    pixels = im.load()
    for x in range(0,6):
        if pixels[x,0] == 0:
            data = data + '1'
        else:
            data = data + '0'
    len_len_binary = int(chr(int(data,2)))
    counter = 0
    data = ''
    bin_len = []
    for x in range(6,6 + 6 * len_len_binary):
        if pixels[x,0] == 0:
            data = data + '1'
        else:
            data = data + '0'
        if counter == 6 * len_len_binary:
            break
    bin_len = [(data[i:i+6]) for i in range(0, len(data), 6)] 
    for x in range(0,len(bin_len)):
        bin_len[x] = int(chr(int(bin_len[x], 2)))
    for x in range(0,len(bin_len)):
        length = sum(d * 10**i for i, d in enumerate(bin_len[::-1]))
    loc = 0
    data = ''
    length = length + ((1 + len_len_binary) * 6)
    for x in range(0,w):
        for y in range(0,h):
            if loc >= length:
                break
            if pixels[y,x] == 0:
                add = '1'
            else:
                add ='0'
            data = data + add
            loc = loc + 1
        if loc >= length:
                break
    data = data[(len_len_binary + 1) * 6::]
    data = data
    loc = 0
    bin_data = ''
    rich_txt = ''
    len_follow = ''
    for z in range(0,999999999999):
        if loc >= len(data):
            break
        bin_data = ''
        len_follow = ''
        for y in range(0,6):
            len_follow = len_follow + data[loc]
            loc = loc + 1
        len_follow = int(chr(int(len_follow, 2)))
        for y in range(0,len_follow):
            bin_data = bin_data + data[loc]
            loc = loc + 1
        rich_txt = rich_txt + chr(int(bin_data, 2))
##        print(str(loc) + '/' + str(len(data)))
    print(rich_txt)
    file = open(save_name + '.txt',"w+")
    file.write(rich_txt)
    file.close()

if len(sys.argv) == 1:
    op = input("Enter Operation: ")
    if op.lower() == 'e' or op.lower() == 'encrypt':
        save_name = input("Enter Name Of Resulting .PNG File: ")
        Encrypt(save_name)
    if op.lower() == 'd' or op.lower() == 'decrypt':
        save_name = input("Enter Name Of Resulting Text File: ")
        Decrypt(save_name)
    
if len(sys.argv) == 3:
    save_name = sys.argv[2]
    if sys.argv[1].lower() == 'e' or sys.argv[1].lower() == 'encrypt':
        Encrypt(save_name)
    if sys.argv[1].lower() == 'd' or sys.argv[1].lower() == 'decrypt':
        Decrypt(save_name)


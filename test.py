import hashlib
import os
import datetime
import qrcode
import cv2
import numpy
from PIL import Image
from pyzbar import pyzbar

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def DecodeQR(filename):
    if not os.path.exists(filename):
        raise FileExistsError(filename)

    return pyzbar.decode(Image.open(filename), symbols=[pyzbar.ZBarSymbol.QRCODE])

qr = qrcode.QRCode(version=1, 
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=4,
)

#Compute MD5
filename_i = 'data/test_long.c'
filename_o = 'data/output'

#Read a file
f = open(filename_i, mode='rb')
patch_id = 0

while True:
    b = f.read(2048)
    if not b:
        break
    proto_head = ('#%6d#')%patch_id
    qr.clear()
    qr.add_data(proto_head+str(b))
    qr.make(fit = True)
    img = qr.make_image()
    #print(img.get_image())
    mat = cv2.cvtColor(numpy.asarray(img.get_image().convert('RGB')),cv2.COLOR_RGB2BGR)
    cv2.imshow("", mat)
    cv2.waitKey(10)
    #img.get_image().show()
    #img.save(('data/qrcode/%d.png')%(patch_id))
    patch_id+=1

f.close()

#Splite to string

#Encode to Image

#Decode from Image
info = {}
for it in range(0, patch_id):
    imagefile = ('data/qrcode/%d.png')%(it)
    qrinfo = DecodeQR(imagefile)[0].data.decode('utf-8')
    file_id = int(qrinfo[1:7])
    #print(file_id)
    info[file_id] = qrinfo[8:]

sorted(info.items(),key=lambda item:item[0])

#Recover File
content = ''
prev_id = -1
for key, value in info.items():
    prev_id+=1
    while(prev_id < key):
        content += ((">>>>>>>> File Patch %d Lost <<<<<<<<<")%prev_id)
        prev_id+=1
    content += value

command = ("byte_info=%s"%info)
by = eval(content)
f = open(filename_o, mode='wb+')
f.write(by)
f.close()

#Check MD5
input_md5 = GetFileMd5(filename_i)
output_md5 = GetFileMd5(filename_o)
print("input:  ",input_md5)
print("output: ",output_md5)
exit()

import os


datatype = r"C:\Users\zhangwei\Desktop\class1\images\2014.tif"

if not os.path.exists(datatype):
   os.makedirs(datatype)
   print("目录创建成功！")
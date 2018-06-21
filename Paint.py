from PIL import Image
import pandas as pd
from collections import Counter
import glob,os
import numpy as np

#Change the name of the file here
thing=[]
for file in glob.glob("*.csv"):
	thing.append(file)

data=pd.read_csv(thing[0])

x=data['X'].astype(float)
y=data['Y'].astype(float)
z=data['Z'].astype(float)

#Makes a guess as to the resolution of the topographic data
dx=round(abs((min(x)-max(x))/(x[0]-x[1])))
dy=len(x)/dx
check=dy-int(dy)

#Refine guess
i=0
while dy-int(dy)!=0.0:
	dx=dx+i
	dy=len(x)/dx
	if check>=.5:
		i=i-1
	else:
		i=i+1

print([dx,dy])

#Create blank image
im=Image.new('RGB',(int(dx),int(dy)),(0,0,255))
pix=im.load()
width,height=im.size

#Assume that the mode of the elevations is the reservoir level
data=Counter(z)
highest=data.most_common(1)[0][0] 

zz=np.array(z)
zzz=5*zz
z=zzz.tolist()

def paint():
	count=-1
	for i in range(height):
		for j in range(width):
			count=count+1
			if int(z[count])>5*highest:
				pix[j,i]=(int(z[count])-5*int(highest),100,125)
			if count%800000==0:
				a=round(count/(width*height),3)*100
				print(a,"%")
	im.save("Elevationmap.jpg")

paint()
import os
import cv2
import random


user_id = input("enter your id")
user_id_str = str(user_id)
rn = random.randrange(1,3)
rn_str = str(rn)
in_loc = ("INPUT/"+user_id_str+"_"+rn_str+".bmp")
db_loc = ("FP_DB/"+user_id_str+".bmp")


global load_img 
load_img = cv2.imread(in_loc)

bstscr = 0
filen = None
img = None
kp1, kp2, mp = None, None, None

fpimg = cv2.imread(db_loc)
sift = cv2.SIFT_create()

keyp1, desp1 = sift.detectAndCompute(load_img, None   )
keyp2, desp2 = sift.detectAndCompute(fpimg, None   )

matchs = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(desp1, desp2, k=2)

matchp = []

for p, q in matchs:
    if p.distance < 0.1* q.distance:
        matchp.append(p)

keyp = 0
if len(keyp1)<len(keyp2):
    keyp = len(keyp1)
else:
    keyp = len(keyp2)

if len(matchp) / keyp *100 > bstscr:
    bstscr = len(matchp) / keyp *100
    filen = db_loc
    img = fpimg
    kp1,kp2,mp = keyp1, keyp2 , matchp
    print("Best Match: " + filen)
    print("Score: " + str(bstscr))
        
def res_show():
    global load_img
    if filen == None: 
        load_img = cv2.resize(load_img,None, fx=4, fy=4)
        cv2.imshow("NOTFOUND", load_img)
        print(in_loc)
        print(db_loc)
        cv2.waitKey(0)
        cv2.destroyAllWindows  
        exit()
    
    else:
        res = cv2.drawMatches(load_img, kp1, img, kp2, mp, None)
        res = cv2.resize(res,None, fx=4, fy=4)
        cv2.imshow("result", res)
        print(in_loc)
        print(db_loc)
        cv2.waitKey(0)
        cv2.destroyAllWindows

res_show()
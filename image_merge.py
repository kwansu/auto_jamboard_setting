import cv2
import os
import glob


src_path = "trg.png"
trg_path = r"C:\Users\kwansu\Downloads\Lecture 3 - MDPs and Dynamic Programming\*"
save_path = "save/"


src = cv2.imread(src_path)
for path in glob.glob(trg_path):
    trg = cv2.imread(path)
    src[src.shape[0] - trg.shape[0]:, :trg.shape[1]] = trg
    cv2.imwrite(save_path + os.path.basename(path), src)
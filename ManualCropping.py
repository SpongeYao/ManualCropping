# encoding: utf-8
'''
Command line: 
python ManualCropping.py <input folder> <output folder>

s: save the last rectangle and go to next image
x: skip and go to next image
z: clear window
q: quit the all process
'''
import csv
import cv2
import os
import sys

# mouse callback function
def draw_callback(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global img_display, img_canvas
    global rectangle_info
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing == False:
            drawing = True
            ix,iy = x,y
        elif drawing == True:
            drawing = False
            cv2.rectangle(img_display,(ix,iy),(x,y),(0,255,0),1)
            img_canvas= img_display.copy()
            rectangle_info.append([ix, iy, x-ix, y-iy])
            print 'Cropped: ',rectangle_info[-1]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img_display= img_canvas.copy()
            cv2.rectangle(img_display,(ix,iy),(x,y),(0,255,0),1)

def check_path(arg_path):
    # make sure output dir exists
    if(not os.path.isdir(arg_path)):
        os.makedirs(arg_path)
        return False
    else:
        return True

readPath= sys.argv[1]+'/'
OutputPath= sys.argv[2]+'/'
rectangle_info= []
cropdatafile= 'info_crop.csv'


check_path(OutputPath)
Filenames = [f for f in os.listdir(readPath) if os.path.isfile(os.path.join(readPath,f))]
exit_loop= False
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

for f in Filenames:
    if exit_loop:
        print 'The cropping process is terminated...'
        break
    print '>> ', f
    img = cv2.imread(readPath+f)
    # Crop and Normalization 
    img= img[25:img.shape[0]-25, 10:img.shape[1]-10] 
    img= cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)

    img_display= img.copy()
    img_canvas= img.copy()
    cv2.namedWindow(readPath+f)
    
    cv2.moveWindow(readPath+f, 10,50)
    cv2.setMouseCallback(readPath+f,draw_callback)
    index_drawing= True
    while(index_drawing):
        cv2.imshow(readPath+f,img_display)
        k = cv2.waitKey(10) & 0xFF
        if k == ord('s'): # saving the rectangle data and exit
            
            SaveFile = open(OutputPath+cropdatafile, "a")
            SaveFile.write(f+ ','+ str(len(rectangle_info))+',')
            for row in rectangle_info:
                for element in row:
                    SaveFile.write(str(element)+ ',')

            SaveFile.write("\n")
            SaveFile.close()
            
            crop_img= img[rectangle_info[-1][1]:rectangle_info[-1][1]+rectangle_info[-1][3],rectangle_info[-1][0]:rectangle_info[-1][0]+rectangle_info[-1][2]]
            cv2.imwrite(OutputPath+'cropped_'+f.split('.')[0]+'.JPEG',crop_img)
            #cv2.imwrite(DIR_CROPPED+f, cropped)
            #== Destroy Window Command ==
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            #============================
            index_drawing= False
        elif k == ord('x'): # Exit w/o any saving
            #== Destroy Window Command ==
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            #============================
            index_drawing= False
        elif k == ord('z'): # Clear Window
            img_display= img.copy()
            img_canvas= img.copy()
            rectangle_info=[]
        elif k == ord('q'):
            exit_loop= True
            #== Destroy Window Command ==
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            #============================
            index_drawing= False
    del rectangle_info[:]

    
# 顯示視窗，直到任何鍵盤輸入後才離開
cv2.waitKey(1)
cv2.destroyAllWindows()
for i in range (1,5):
    cv2.waitKey(1)


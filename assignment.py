import cv2   #importing cv2
import numpy as np #importing numpy
import math #importing math



imgloc = input("Enter your imageLocation: ")
print(imgloc)

img= cv2.imread(imgloc,0)   #Getting the image by giving the absolute / relative path


#######
#  Function rotateImage
# it takes an image and an angle as an argument and return
# an image with the rotation applied
#
#
#
#
# ############
def rotateImage(image, angle):
    row,col = image.shape  ## Getting the image height and width and save them into row , col
    center=tuple(np.array([row,col])/2) ## the center is half the row and col
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0) ##Calculates an affine matrix of 2D rotation
    new_image = cv2.warpAffine(image, rot_mat, (col,row)) ## Applies an affine transformation to an image by getting the original <src> image and
    ## the rotatio matrix and the size
    return new_image                  #the function return the rotated image


#######
#  Function getrotateImage
# it takes an image as an argument and apply
# -Canny edge detection and then Houghlines deetction
#the function take the atan of every line ((y2-y1),(x2-x1) )
#and return the averge of estimated angles
#
#
# ############
def getrotateImage(img):
    img_edges = cv2.Canny(img, 100, 100, apertureSize=3)  ## Applying canny edges to the image
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=10) ## Appling hough lines detection and save the detected
    # lines in lines variable
    angles = []  ## intialziation of empty list of angles

    for x1, y1, x2, y2 in lines[0]:  ## for loop for every line detected in hough line
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))   ## atan function returns the theta of two passed points
        # with the postive x-axis
        angles.append(angle) # append every new angle to the list of angles

    median_angle = np.median(angles) ## Taking averge of all angles detecd
    img_rotated = rotateImage(img, median_angle)  ## calling the function rotateimage to get the new rotated image
    return img_rotated ## return the rotated image


#######
#  Function arrangeCircle
# it rearrange the circles nparray that we extracted by hough circles
# Firstly by arranging the y axis then by arranging the x axis
#So that the circles are arranged so that every following
# circle is the circle next to its previos in the paper
#
# ############
def arrangeCircle():
    ####
    # Arrange  y in ascending order
    #
    # #######

    for i in range(len(circles[0])):
        for j in range(0, len(circles[0]) - i - 1):
            if circles[0][j][1] > circles[0][j + 1][1]:
                temp = circles[0][j].copy()
                circles[0][j] = circles[0][j + 1]
                circles[0][(j + 1)] = temp

    ####
    #
    # Then Arranging  the Xs in ascending order
    #
    #####

    for i in range(len(circles[0])):
        for j in range(0, len(circles[0]) - i - 1):
            if circles[0][j][1] <= circles[0][j + 1][1] <= (circles[0][j][1] + 5):
                if circles[0][j][0] > circles[0][j + 1][0]:
                    temp = circles[0][j].copy()
                    circles[0][j] = circles[0][j + 1]
                    circles[0][(j + 1)] = temp

#######
#  Function getAnswers
# it uses  the circles nparray that we extracted by hough circles
# and the filledCircles nparray that we created
# To figure the corresponding answer of student to every Question in the Paper
#
# ############
def getAnswers():
    for i in range(len(filledCircles[0])): ## For every Circle in the Filled Circles
        choice = 0 ## intialize choice intially to equal zero
        for j in range(len(circles[0])): ## for every circle in the Circles nparray

            if (filledCircles[0][i] == circles[0][j]).all():        ## if the circle in circles array match the one in filled array <matches both x and y >
                if i < 3:
                    if i == 0:
                        if choice == 0:
                            Questions_and_answers[i][1] = "Male "
                        elif choice == 1:
                            Questions_and_answers[i][1] = "Female "
                    elif i == 1:
                        if choice == 0:
                            Questions_and_answers[i][1] = "Fall "
                        elif choice == 1:
                            Questions_and_answers[i][1] = "Spring "

                        elif choice == 2:
                            Questions_and_answers[i][1] = "Summer "

                    elif i == 2:
                        if choice == 0:
                            Questions_and_answers[i][1] = "MCTA "
                        elif choice == 1:
                            Questions_and_answers[i][1] = "ENVER "

                        elif choice == 2:
                            Questions_and_answers[i][1] = "BLDG"

                        elif choice == 3:
                            Questions_and_answers[i][1] = "CESS "

                        elif choice == 4:
                            Questions_and_answers[i][1] = "ERGY"



                        elif choice == 5:
                            Questions_and_answers[i][1] = "COMM "

                        elif choice == 6:
                            Questions_and_answers[i][1] = "MANF"

                        elif choice == 7:
                            Questions_and_answers[i][1] = "LAAR "

                        elif choice == 8:
                            Questions_and_answers[i][1] = "MATL"



                        elif choice == 9:
                            Questions_and_answers[i][1] = "CISE"

                        elif choice == 10:
                            Questions_and_answers[i][1] = "HAUD "
                else:
                    if choice == 0:
                        Questions_and_answers[i][1] = "Strongly Agree "
                    elif choice == 1:
                        Questions_and_answers[i][1] = "Agree "

                    elif choice == 2:
                        Questions_and_answers[i][1] = "Neutral"

                    elif choice == 3:
                        Questions_and_answers[i][1] = "Disagree "

                    elif choice == 4:
                        Questions_and_answers[i][1] = "Strongly Disagree"
            elif ((filledCircles[0][i][1] - 50) <= circles[0][j][1] <= (filledCircles[0][i][1] + 50)and (i == 2)):    ## if we are in the program area we will
                # compare the y's of both circles and filled circles with tolerance up and down 50 px if the y's are equal we will increment
                # the choice by one
                choice = choice + 1
            elif ((filledCircles[0][i][1] - 10) <= circles[0][j][1] <= (filledCircles[0][i][1] + 10)and (not(i == 2))):
                choice = choice + 1## if we are in any other area than  the program area we will
                # compare the y's of both circles and filled circles with tolerance up and down 10 px if the y's are equal we will increment
                # the choice by one







x=cv2.resize(img,(800,800)) ## resize the image to be viewable
cv2.imshow('detected circles', x)  ## show the image
cv2.waitKey(500) ## wait without closing the preview window

img = getrotateImage(img)  ## Calling th rotation function to get the rotated circle
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)  ## chane to Grayscale
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=10,maxRadius=15)       ## Performing Hough circle detection with minR=10 and max R =15
# to detect all circles within these constraints in our image
circles = np.uint16(np.around(circles)) ## using approx
arrangeCircle() ## calling the arrange circles function to arrange the circles with respect to both  x and y

    


filledCircles = np.empty((1,22,3),int) # create an empty String where we will store the circles shaded(have back color )
k=0

#########
# In the Following loop we will copy the filled circles to the filled circles array and also make visualiztion of all
# circles detected by hough
# ##########
for i in circles[0,:]:
    # Draw all circles detected
    cv2.circle(cimg, (i[0], i[1]), i[2], (255, 0, 0), 2)
    x = cv2.resize(cimg, (800, 800)) ## resize the image to be viewable
    cv2.imshow('detected circles', x) ## view detected circles
    cv2.waitKey(100) ## wait for preveiw
    if img[i[1]][i[0]] == 0: ## if  the circle center is black then we will assume its black and added it to filled circles
        k=k+1
        filledCircles[0][k-1]=i





for i in filledCircles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
        x=cv2.resize(cimg,(800,800)) ## resize the image to be viewable
        cv2.imshow('detected circles', x)  ## view detected filled  circles
        cv2.waitKey(100) ## wait for preveiw









Questions_and_answers = [["Gender",""],["semester",""],["Program",""],["1.1",""] ,["1.2",""],["1.3",""] ,
                         ["1.4",""],["1.5",""] ,["2.1",""] ,["2.2",""],["2.3",""] ,
                         ["2.4",""],["2.5",""],["2.6",""],["3.1",""] ,["3.2",""],["3.3",""] ,
                         ["4.1",""],["4.2",""],["4.3",""] ,["5.1",""],["5.2",""] ]

 ## we will intialize a list that has only the questions and empty answers







getAnswers () ## we will call the getAnswers function to get the responding answers to our questions


f= open("The answers.txt","w+")      ## we will open the answers file <if not there it will be created> and
# give the ability to read and write from it
first_line = "Question"+"                 " + "Respond"         ## A String that classify questions and answers at the begining of our file
f.write(first_line ) ## write the string on the File
f.write("\n") ## write empty line to the file
f.write("----------------------------------------------------------------------------")## write separators  to the file
f.write("\n") ## write empty line to the file




#############
#
# The Following String is used in Writing the questions and thier anwsers to the file we created
#
# ###########





for i in range(len(Questions_and_answers)) : ## for every element in the list
    StrinG = Questions_and_answers[i][0]  + "                 " + Questions_and_answers[i][1] ## get the Question and the answer
    f.write(StrinG) ## write to the file  the Question and the answer
    f.write("\n")  ## write empty line to the file
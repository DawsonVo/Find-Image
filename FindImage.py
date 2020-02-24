#Dawson Vo 500879711 - fixed


#for my ease of testing
#-----------------------------------------------------------------------------------------------------------
#for timer
import time
setMediaFolder(getMediaPath())
#This is the scene that will be searched
scene = makePicture("scene.jpg")
#This is the template that is being found
template = makePicture("waldo.jpg")
#------------------------------------------------------------------------------------------------------------
#matrixtype controls where the grayscale() function saves its luminance values to
#matrixtype  0 - matrixtemplate, 1 - matrixsearch
matrixtype = 0
#comparetype controls if controlOne() runs with a limiter or not - ie if controlOne() stops when lumsum reaches a certain number or computes the whole value
#comparetype  0 - normal computation, 1 - optimized computation with limiter
comparetype = 0
#comparelimit will be the minimum value of that the first 10 pixels cant surpass (if the first 10 pixels are off then the rest of the pixels will be off)
comparelimit = 100
matrixscores = 0
matrixtemplate = 0
matrixsearch = 0


  
  
#DONE________________________________________________________________________________________________________   
def findImage(targetJPG, searchJPG): #findImage(template, scene) Target - Image being found, Search - Image containing template
  global matrixtype
  #start timer
  timeStart = time.clock()
  #grayscale both images
  grayscale(targetJPG)
  #sets up grayscale() to put luminance values into the matrixsearch matrix instead of the matrix template one
  matrixtype = 1
  grayscale(searchJPG)
  #lumMatrix is the matrix that contains all absolute luminance differences - this is given by compareAll() which returns a matrix
  lumMatrix = compareAll(targetJPG,searchJPG)
  #
  coor = find2Dmin(lumMatrix)
  #ending statement
  print "The coordinates of the top left corner of template on searchImage is " +String( coor)
  
  displayMatch(searchJPG,coor[0],coor[1],getWidth(targetJPG),getHeight(targetJPG),red)
  
  #timer 
  timeEnd = time.clock() - timeStart
  m, s = divmod(timeEnd, 60)
  h, m = divmod(m, 60)
  return "Processing Time: %d:%02d:%02d" % (h, m, s)
  
  
  
#DONE________________________________________________________________________________________________________ 
#Grayscales the given picture
def grayscale(picture):
  global matrixtype
  global matrixtemplate
  global matrixsearch
  h = getHeight(picture)
  w = getWidth(picture)
  #if we are in matrixtype = 0 we are running grayscale on the template image, 1 is for searchImage
  if matrixtype == 0:
    matrixtemplate = [[9999999999999 for i in range(w)] for j in range(h)]
  if matrixtype == 1:
    matrixsearch = [[9999999999999 for i in range(w)] for j in range(h)]
#going through all pixels of the image then getting the luminance with the function (r+g+b)/3
#putting values into the matrix after getting the values of luminance instead of doing it in the compareOne() function to reduce the amount of times getPixel() and getRed() are used
  for y in range(h):
    for x in range(w):
      #i will be the pixel
      i = getPixel(picture,x,y)
      #getting the red,green,and blue values of the pixel
      r = getRed(i)
      g  = getGreen(i)
      b = getBlue(i)
      #calculating the luminance of the pixel
      lum = (r+g+b)/3
      c = Color(lum,lum,lum)
      #setting the color of the pixel to the luminance
      i.setColor(c)
      
      #adds luminance value to the corresponding array based on matrix type
      if matrixtype == 0:
        matrixtemplate[y][x] = lum
      elif matrixtype == 1:
        matrixsearch [y][x] = lum
    
    
#Done_______________________________________________________________________________________________________
def compareOne(template,searchImage,x1,y1):
  #calling the matrixes declared at the beggining of the code - lumsum is the value from summing the absolute difference between pixels on template and searchImage
  global matrixtemplate
  global matrixsearch
  global matrixtype
  global comparetype
  global comparelimit
  lumsum = 0
  
  #was moved to grayscale() to reduce the amount of times getPixel().getRed() is used-------------------------------------------------------------------------------------------------------------------------------------------------------
  #if the matrix for template (matrixtemplate) containing its luminance values for each pixel has not been set up, then create one
  #This optimizes the code by preventing repetition of calculating the luminance of the same pixel using the function getPixel()
  #if matrixtemplate == 0:
  #  w = getWidth(template)
  #  h = getHeight(template)
  #  matrixtemplate = [[9999999999999 for i in range(w)] for j in range(h)]
  #  for y in range(h):
  #    for x in range(w):
  #      matrixtemplate [y][x] = getPixel(template,x,y).getRed()
        
  #if the matrix for searchImage (matrixsearch) containing its luminance values for each pixel has not been set up, then create one
  #This optimizes the code by preventing repetition of calculating the luminance of the same pixel using the function getPixel()
  #if matrixsearch == 0:
  #  w = getWidth(searchImage)
  #  h = getHeight(searchImage)
  #  matrixsearch = [[9999999999999 for i in range(w)] for j in range(h)]
  #  for y in range(h):
  #    for x in range(w):
  #      matrixsearch [y][x] = getPixel(searchImage,x,y).getRed()
  #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  
  
  #for each pixel in searchImage within the size of template (ie for pixel x and y, x1<x<x1+template.getWidth() and y1<y<y1+template.getHeight())
  #This is done by pulling the luminance value for template and its corresponding pixel on searchImage from their respective matrixes
  #after obtaining the luminance value get the absolute difference then add it to the running sum (lumsum)            
  for y in range(template.getHeight()):
    for x in range(template.getWidth()):
      #get lumT from matrixtemplate and lumSI from matrixsearch\
      
      lumT = matrixtemplate[y][x]
      #the corresponding pixel would be the pixel from template if it was overlayed ontop of searchImage with the top-left corner on x1,y1
      lumSI=matrixsearch[y+y1][x+x1]
      
      #add the absolute difference to the running sum (lumsum)
      lumsum+= abs(lumT-lumSI)
      
      if x<10 and y ==0 and comparetype == 1 and comparelimit<lumsum  :
        lumsum = 999999999999999
        return lumsum
  
  #return the running sum of absolute differences for each pixel's luminance
  #print lumsum
  return lumsum
  
  
#DONE________________________________________________________________________________________________________
#runs compareOne() for each pixel in search image then, returns a matrix of all values returned by compareOne() for each pixel
def compareAll(template,searchImage):
  #calles the matrix from
  global matrixscores
  global comparetype
  global comparelimit
  
  
  #sizes of both images
  h = getHeight(template)
  w = getWidth(template)
  h1 = getHeight(searchImage)
  w1 = getWidth(searchImage)
  #sets up compareOne() to run optimized with limiter
  comparetype = 1
  #creates matrix with size enough for just the pixels being calculated - ie Pixels in the bottom and right where the template would exit the searchImage are not included in the matrix
  matrixscores = [[9999999999999 for i in range(w1-w+1)] for j in range(h1-h+1)]
  #runs compareOne() for each index in matrixscores
  for y in range(len(matrixscores)):
    for x in range(len(matrixscores[0])):
      matrixscores [y][x] = compareOne(template,searchImage,x,y)
  return matrixscores
  
  
  
#DONE________________________________________________________________________________________________________ '
#Findes the smallest value in a given matrix - in this case it will be used to find the smallest value in matrixscores, which will be the coordinates of the top-left
#corner where the image in template, best matches searchImage
def find2Dmin(matrix):
  #setting variables with min being a large number
  mincol = 0
  minrow = 0
  min = 9999999999999999999999
  #this goes through all values of matrix, if the value in matrix is lower than min, set min to the matrix value and set mincol to the x value and minrow to the y value
  for y in range(len(matrix)):
    for x in range(len(matrix[0])):
      
      if min>matrix[y][x]:
        
        min = matrix [y][x]
        mincol = x
        minrow = y
        
  #return the coordinates of the min value (x,y)
  return(mincol,minrow)


#DONE________________________________________________________________________________________________________ 
#Creates lines of 3 thickness around the matched coordinates
def displayMatch(searchImage,x1,y1,w1,h1,color):
  #runs through all pixels
  for y in range(getHeight(searchImage)):
    for x in range(getWidth(searchImage)):
      #creates left line
      if x>=x1-1 and x<=x1+1 and y>=y1 and y<=y1+h1:
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)
      #creates right line
      elif x>=x1+w1-1 and x<=x1+w1+1 and y>=y1 and y<=y1+h1:
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)
      #creates top line
      elif y>=y1-1 and y<=y1+1 and x>=x1 and x<=x1+w1:
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)
      #creates bottom line
      elif y>=y1-1+h1 and y<=y1+1+h1 and x>=x1 and x<=x1+w1:
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)
  explore(searchImage)
#!/usr/bin/env python


# Minimum version: scratch 2.


import os, sys
import time
import zipfile
import json
import datetime
#To make it compatible with python 3
from __future__ import print_function

def createHeader(codeInInit=''):
  head = '#!/usr/bin/env python\n'
  head += '# -*- coding: utf-8 -*-\n\n\n'
  head += 'import numpy as np\n'
  head += 'import cv2\n'
  head += 'import ast\n'
  head += 'import sys, time\n'
  head += 'import LearnBotClient\n\n\n'
  head += '# Ctrl+c handling\n'
  head += 'import signal\n'
  head += 'signal.signal(signal.SIGINT, signal.SIG_DFL)\n\n\n'
  head += 'class MiClase(LearnBotClient.Client):\n'
  head += '  def __init__(self):\n'
  if codeInInit == '':
    head += '    pass'
  else:
    head += codeInInit
  head += '\n\n'
  head += '  def code(self):'
  return head


def createTail():
  tail = '# When everything done, release the capture\n'
  tail += 'cv2.destroyAllWindows()\n\n'
  tail += 'miclase = MiClase()\n'
  tail += 'miclase.main(sys.argv)\n'
  return tail


def putIdentation(numberSpaces):
  identation=''
  for i in range(0,numberSpaces):
    identation += ' '
  return identation



def hasChildList(itemList):
  if len(itemList) == 1:
    return False
  else:
    for item in itemList:      
      if (type(itemList) == list):
        return True
  return False



def getcodelist(code):
  codeReturn = ''
  for itemList in code:
#      if (type(itemList) == list):
    if hasChildList(itemList) is True:
      codeReturn += (itemList[0] + '\n' + str(getcodelist(itemList)))
    else:
      codeReturn = str(itemList[0]) + '\n'
#      for item in itemList:
#         # print item
#          codeReturn += item

  return codeReturn
            

    
def codeWorker (codeJSON,identation):
  loops = {'doForever','while'}
  learnbotBlocks = {'getImage','getDistance','moveRobot','delay'}
  questions = {'doIfElse'}
  functionsScratch = {'wait:elapsed:from:','turnLeft','turnRight','forward'}
  codePython = ''
  locate = False
  #for i in range(0,len(codeJSON)) and locate is False:
  i=0
  while i < len(codeJSON) and locate is False:
    if type(codeJSON[i]) == int: # si es un numero es que indica posicion
      pass
    else:
      if str(codeJSON[i]) in loops:
        #################################################################
        ###                      LOOP SECTION                         ###
        #################################################################        
        if codeJSON[i] == 'doForever':
          codePython += putIdentation(identation) + 'while True:\n'
          identation += 2
          i += 1
          for codJSON in codeJSON[i]:
            output,codeTemp = codeWorker(codJSON, identation)          
            codePython += codeTemp
          identation -= 2
          locate = True
          break
        elif codeJSON[i] == 'doRepeat':
          i += 1
          codePython += putIdentation(identation) + 'for i in range(0,'+str(codeJSON[i])+'):\n'
          identation += 2
          i += 1                 
          output,codeTemp = codeWorker(codeJSON[i][0], identation)
          codePython += codeTemp
          identation -= 2
        else:
          print ('aaa')
      
      elif str(str(codeJSON).split(' ')[0]).translate(None,"u,'[]") in questions:        
        #################################################################
        ###                    QUESTION SECTION                       ###
        #################################################################
        i += 1
        locate = True        
        question = str(str(codeJSON).split(' ')[0]).translate(None,"u,'[]")
        if question == 'doIfElse':
          codePython += putIdentation(identation) +'if ' + (str(codeJSON[1][1]).split(' ')[1]).translate(None,"u,'[]") +' '+ str(codeJSON[1][0]) +' '+ str(codeJSON[1][2])+':\n'
          identation += 2
          output,codeTemp = codeWorker(codeJSON[2], identation)         
          codePython += codeTemp
          identation -= 2          
          codePython += putIdentation(identation) +'else:\n'
          identation += 2
          output,codeTemp = codeWorker(codeJSON[3], identation)          
          codePython += codeTemp
          identation -= 2
          break

      elif (str(str(codeJSON).split(' ')[1])).translate(None,"u,'[]") in learnbotBlocks:
        #################################################################
        ###                     ZONE OWN BLOCKS                       ###
        #################################################################          
        i += 1
        locate = True
        # asi de complejo porque me quedo con la primera palabra de la primera celda
        action = (str(str(codeJSON).split(' ')[1])).translate(None,"u,'[]")
        if action == 'getImage':
          codePython += putIdentation(identation) + 'image = self.getImage()\n'
        elif action == 'getDistance':
          codePython += putIdentation(identation) + 'distance = ast.literal_eval(self.getSonars())["sensor1"]["dist"]\n'
        elif action == 'moveRobot':
          vAdv = (str(str(codeJSON).split(' ')[4])).translate(None,"u,'[]")
          vRot = (str(str(codeJSON).split(' ')[5])).translate(None,"u,'[]")
          codePython += putIdentation(identation) + 'self.setRobotSpeed('+vAdv+','+vRot+')\n'
        elif action == 'delay':
          codePython += putIdentation(identation) + 'time.sleep('+(str(str(codeJSON).split(' ')[3])).translate(None,"u,'[]")+')\n'          
        break
      
      elif str(str(codeJSON).split(' ')[0]).translate(None,"u,'[]") in functionsScratch:
        codePython += putIdentation(identation) + 'time.sleep('+str(str(codeJSON).split(' ')[1]).translate(None,"u,'[]")+')\n'
        i += 1
        locate = True
        break

      else:
        i += 1
        locate = True
        break



      # elif codeJSON[i] == 'forward:':
      #   codePython += putIdentation(identation) + 'self.setRobotSpeed('+str(codeJSON[i+1])+',0)\n'
      # elif codeJSON[i] == 'turnRight:':
      #   codePython += putIdentation(identation) + 'self.setRobotSpeed('+str(codeJSON[i+1])+',0)\n'
      # elif codeJSON[i] == 'turnLeft:':
      #   codePython += putIdentation(identation) + 'self.setRobotSpeed('+str(codeJSON[i+1])+',0)\n'



      #   pass
      # if type(code) == list:
      #   codePython = getcodelist(code)

  # print codePython
  return True,codePython



def main():
  sourceFile = sys.argv[1]
  try:
      os.system('cp '+sourceFile+' temp.zip')
  except IOError:
      print ('cannot open', sourceFile)
  else:    
      fh = open('temp.zip', 'rb')
      z = zipfile.ZipFile(fh)
      locate = False
      for name in z.namelist():
        if name == 'project.json':
          data = json.loads(z.read(name))
          codeScratchJSON = data['children'][0]['scripts'] # contiene las posiciones de donde empieza
          for code in codeScratchJSON:
            if code[2][0][0] == 'procDef':
              #################################################################
              ###               OWN BLOCKS DEFINITION ZONE                  ###
              #################################################################
              pass
            else:
              if code[2][0][0] == 'whenGreenFlag':
                identation=4
                print (code[2][1])
                print ('-----------------')
                print ('-----------------')
                print ('-----------------')
                # code[2][1] porque es donde esta el codigo
                locate,codePython = codeWorker(code[2][1],identation)
              else:
                print ('Not init block program')
          
      if locate is False:
        print ('The content of file is not correct :-(')
      else:
        print (createHeader() + '\n' + codePython + '\n'+ '\n'+ '\n' + createTail())
        #print codePython
        print ("Opening the file...")
        try:
	  filename = sourceFile.split('.')[0]
	  with open(filename+'.py', "w") as outfile:
	    outfile.write(createHeader() + '\n' + codePython + '\n'+ '\n'+ '\n' + createTail())
	  outfile.close()
	  os.system('python '+filename+'.py --Ice.Config=LearnBotClient.conf')
	except IOError:
	  print ("oops! I don't write de file")
      os.system('rm temp.zip')


if __name__ == "__main__":
    main()

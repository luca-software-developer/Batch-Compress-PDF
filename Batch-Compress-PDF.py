
#######################################################
##                                                   ##
##  BatchCompressPDF ver. 1.0.0.0                    ##
##                                                   ##
##  Programma per la compressione dei PDF in batch.  ##
##                                                   ##
#######################################################

from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

import os
import glob
import pathlib
import subprocess

APP_NAME = 'BatchCompressPDF'
APP_VERSION = '1.0.0.0'

def clearScreen():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

def printHeader():
    print()
    print( '       *****************************************************')
    print( '       *                                                   *')
    print(f'       *  {APP_NAME} ver. {APP_VERSION}                    *')
    print( '       *                                                   *')
    print( '       *  Programma per la compressione dei PDF in batch.  *')
    print( '       *                                                   *')
    print( '       *****************************************************')
    print()
    print()

def setTitle(title):
    subprocess.call(f'title {title}', shell=True)

def setColor(colorString):
    subprocess.call(f'color {colorString}', shell=True)

def init():
    clearScreen()
    printHeader()
    setTitle(APP_NAME)
    setColor('1f')

def waitForEnter():
    input('\n       Premere [Invio] per continuare ... ')

def requestFolder(whichDir):
    result = ''
    print(f'  [?]  Trascina qui la cartella {whichDir} e poi premi [Invio]\n')
    while not result or not os.path.exists(result):
        result = input(f'       >>>  ').strip()
    print()
    return result

def compressPDF(inPath, outPath):
    reader = PdfReader(inPath)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    with open(outPath, 'wb') as outFile:
        writer.write(outFile)

def main():
    init()
    
    inDir = requestFolder('con i PDF da comprimere')

    count = 0
    inPaths = list(glob.iglob(f'{inDir}/**/*.pdf', recursive=True))
    for inPath in inPaths:
        stem = pathlib.Path(inPath).stem
        path = pathlib.Path(inPath).parent.resolve()
        outPath = f'{path}/{stem} (compresso).pdf'
        
        compressPDF(inPath, outPath)

        count += 1
        progress = round(100 * count / len(inPaths))
        preSize = pathlib.Path(inPath).stat().st_size
        postSize = pathlib.Path(outPath).stat().st_size
        compressionRatio = round(100 - 100 * postSize / preSize)
        
        print(f'  [!]  Compresso {pathlib.Path(inPath).name} ({preSize} byte => {postSize} byte / {compressionRatio}%) ... {progress}%')

    print(f'\n  [!]  Operazione completata!')
    
    waitForEnter()

if __name__ == '__main__':
    while True:
        main()

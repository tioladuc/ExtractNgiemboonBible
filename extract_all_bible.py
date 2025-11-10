from pathlib import Path
import requests
import time
import os
from bs4 import BeautifulSoup


def getUrlContent(url, fileName):
    if os.path.exists(fileName) and os.path.isfile(fileName):
        return True

    response = requests.get(url)
    time.sleep(2) # to avoid been band
    # print(url + " === " + fileName)
    # print(response.text)
    if "Nous sommes désolés, la page que tu cherches est introuvable." in response.text:
        print("first")
        return False

    # print(response.text)
    # Save the response content into a text file
    with open(fileName, "w", encoding="utf-8") as file:
        file.write(response.text)
        
    return True

def getCompleteBible(livreOfBible, biblesList, core_bible):
    for bible in biblesList:
        folder = core_bible + bible['folder']
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        bible_compteur = 1
        arrayOfLinks = []

        for livre in livreOfBible:
            livre_temp = livre.replace(".[Page].[Code]", "")[-3:]
            
            livre_re = folder + "/" + livre_temp
            print(livre_re)
            folder_path_temp = Path(livre_re)
            if not folder_path_temp.exists():
                folder_path_temp.mkdir(parents=True)

            for i in range(1, 2):
                url = livre.replace("[Page]", str(i))
                url = url.replace("[Code]", bible['folder'])
                url = url.replace("[CodeNumber]", bible['code'])
                fileName = livre_re + "/" + str(bible_compteur) + "_chap_" + str(i) + ".html"

                if getUrlContent(url, fileName) == False:
                    break
                            
                arrayOfLinks.append( str(bible_compteur) + ") " + url)
                bible_compteur = bible_compteur + 1
                print(url + " //// " + fileName)
            
        compilationFile = folder + "/list_of_urls.txt"
        with open(compilationFile, "w", encoding="utf-8") as file:
            for line in arrayOfLinks:
                file.write(f"{line}\n")
            

        print(bible)

def getTestOfExtractionVerses():    
    getUrlContent("https://www.bible.com/fr/bible/37/1CH.1.CEB", "fileNameA.html")
    getUrlContent("https://www.bible.com/fr/bible/4488/1CH.1.NNH", "fileNameB.html")

    html_contentA = ""
    with open("fileNameA.html", "r", encoding="utf-8") as file:
            html_contentA = file.read()
    html_contentB = ""
    with open("fileNameB.html", "r", encoding="utf-8") as file:
            html_contentB = file.read()

    dataA = extract_data_test(html_contentA, "1CH", "1")
    dataB = extract_data_test(html_contentB, "1CH", "1")
    print("******************************************************************************")
    print("**************ContentA="+ str(len(dataA)) +"** ContentB="+ str(len(dataB)) +"********************")
    print("******************************************************************************")
    for i in range(0, len(dataA)):
        print(str(i+1) + ") " + dataA[i])
    print("******************************************************************************")
    for i in range(0, len(dataB)):
        print(str(i+1) + ") " + dataB[i])


def extract_data_test(html_content, book, chapter):
    soup = BeautifulSoup(html_content, "html.parser")
    result = []
    
    for i in range(1,1000):
        verseCode = book + "." + chapter + "." + str(i)
        #print(verseCode)
        verse = soup.find("span", {"data-usfm": verseCode})
        if verse is None:
            return result
        label = verse.find("span", class_="ChapterContent_label__R2PLt")
        other = verse.find("span", class_="ChapterContent_note__YlDW0")        
        if label:
            label.decompose()  # removes the tag completely
        if other:
            other.decompose()  # removes the tag completely
        result.append(verse.get_text())#(separator="", strip=True))
    return result


livreOfBible = [
"https://www.bible.com/fr/bible/[CodeNumber]/GEN.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/EXO.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/LEV.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/NUM.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/DEU.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JOS.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JDG.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/RUT.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/1SA.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2SA.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/1KI.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2KI.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/1CH.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2CH.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/EZR.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/NEH.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/EST.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JOB.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/PSA.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/PRO.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/ECC.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/SNG.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/ISA.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JER.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/LAM.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/EZK.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/DAN.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/HOS.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/JOL.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/AMO.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/OBA.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/JON.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/MIC.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/NAM.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/HAB.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/ZEP.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/HAG.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/ZEC.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/MAL.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/MAT.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/MRK.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/LUK.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JHN.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/ACT.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/ROM.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/1CO.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2CO.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/GAL.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/EPH.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/PHP.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/COL.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/1TH.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2TH.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/1TI.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2TI.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/TIT.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/PHM.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/HEB.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JAS.[Page].[Code]",

"https://www.bible.com/fr/bible/[CodeNumber]/1PE.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2PE.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/1JN.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/2JN.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/3JN.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/JUD.[Page].[Code]",
"https://www.bible.com/fr/bible/[CodeNumber]/REV.[Page].[Code]"
]

biblesList = [
    {"folder": "NNH", "code": "4488"}, 
    #{"folder": "NGBM", "code": "299"}, 
    {"folder": "CSB", "code": "1713"}
    #{"folder": "KJV", "code": "1"}
]

core_bible = "core_bible/"

#getTestOfExtractionVerses()
getCompleteBible(livreOfBible, biblesList, core_bible)
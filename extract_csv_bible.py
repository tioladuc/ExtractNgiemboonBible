import os
from collections import Counter
from pathlib import Path
import csv
from bs4 import BeautifulSoup

def extract_verses_from_chapter(file):
    result = []

    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    

    verses = soup.find_all("span", class_="ChapterContent_verse__57FIw")
    if len(verses) == 0:
        return [] #raise ValueError("No div with data-testid='chapter-content' found.")

    # Find all span elements with a data-usfm attribute
    for verse_span in verses:
        label = verse_span.find("span", class_="ChapterContent_label__R2PLt")
        if label:
            label.decompose()  # removes the tag completely
        
        text = verse_span.get_text(separator="", strip=True)
        if text.strip() != "":
            result.append(text)
        #verse_detail = verse_span.find_all("span")
        #if len(verse_detail)==2:
            #result.append(verse_detail[1].get_text(strip=True))

    return result


def verification(dialect, english, coreFolder):
    dialect = coreFolder + dialect['folder']
    english = coreFolder + english['folder']
    
    subfolders_dialect = [f for f in os.listdir(dialect) if os.path.isdir(os.path.join(dialect, f))]
    subfolders_english = [f for f in os.listdir(english) if os.path.isdir(os.path.join(english, f))]
    
    if Counter(subfolders_dialect) != Counter(subfolders_english):
        return False

    for subfolder in subfolders_dialect:
        dialectA = dialect + "/" + subfolder
        englishA = english + "/" + subfolder

        subfolders_dialectA = [f for f in os.listdir(dialectA) if os.path.isdir(os.path.join(dialectA, f))]
        subfolders_englishA = [f for f in os.listdir(englishA) if os.path.isdir(os.path.join(englishA, f))]

        if Counter(subfolders_dialectA) != Counter(subfolders_englishA):
            return False

    return True


def save_csv_data(data, fileName):
    with open(fileName, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def extract_book_chapter_to_csv(dialectFolder, englishFolder, dataTextFile, subfolderBook):
    dialectAFile = dialectFolder + "/" + subfolderBook + "/" + dataTextFile
    englishAFile = englishFolder + "/" + subfolderBook + "/" + dataTextFile
    csv_destinationFile = csv_bible + subfolderBook + "/" + dataTextFile.replace(".txt", ".csv")
    
    arrayDialect = extract_verses_from_chapter(dialectAFile)
    arrayEnglish = extract_verses_from_chapter(englishAFile)
    arrayDestination = []
    print("=============================="+dataTextFile+"====================================")
    #print(arrayDialect)
    #print("******************************************************************")
    #print(arrayEnglish)
    #print("--------------------------------------------------------------------")
    
    if len(arrayDialect) == len(arrayEnglish):
        for i in range(0, len(arrayDialect)):
            arrayDestination.append({'ngiemboon':arrayDialect[i], 'en': arrayEnglish[i]})
        save_csv_data(arrayDestination, csv_destinationFile)
    else:
        print("exit exit ** "+str(len(arrayDialect))+" ** ==========  ** "+str(len(arrayEnglish))+" ** ")


def constructing_csv(dialect, english, coreFolder, csv_bible):
    dialect = coreFolder + dialect['folder']
    english = coreFolder + english['folder']
    
    subfolders_dialect = [f for f in os.listdir(dialect) if os.path.isdir(os.path.join(dialect, f))]
    subfolders_english = [f for f in os.listdir(english) if os.path.isdir(os.path.join(english, f))]
    
    if Counter(subfolders_dialect) != Counter(subfolders_english):
        return False

    for subfolderBook in subfolders_dialect:
        dialectA = dialect + "/" + subfolderBook
        englishA = english + "/" + subfolderBook
        
        subfolders_dialectLivre = [f for f in os.listdir(dialectA) if not os.path.isdir(os.path.join(dialectA, f))]
        subfolders_englishLivre = [f for f in os.listdir(englishA) if not os.path.isdir(os.path.join(englishA, f))]

        if Counter(subfolders_dialectLivre) != Counter(subfolders_englishLivre):
            return False

        bookFolder = csv_bible + subfolderBook
        bookFolder_path = Path(bookFolder)

        if not bookFolder_path.exists():
            bookFolder_path.mkdir(parents=True)

        for file in subfolders_englishLivre:
            extract_book_chapter_to_csv(dialect, english, file, subfolderBook)
    return True



biblesList = [
    {"folder": "NNH", "code": "4488"}, 
    {"folder": "NGBM", "code": "299"}, 
    {"folder": "CSB", "code": "1713"}
]

core_bible = "core_bible/"
csv_bible = "csv_bible/"
sourceDialete = biblesList[0]
destinationEnglish = biblesList[2]

if verification(sourceDialete, destinationEnglish, core_bible):
    constructing_csv(sourceDialete, destinationEnglish, core_bible, csv_bible)
else:
    print("verification NOT OK")

###fileA = "core_bible/KJV/3JN/64_chap_1.txt"
###fileB = "core_bible/NNH/3JN/64_chap_1.txt"
###dataA = extract_verses_from_chapter(fileA)
###dataB = extract_verses_from_chapter(fileB)
###print(str(len(dataA)) + " ====== " +str(len(dataB)))
###print("********************************************************")
#print(dataA)
###it = 1
###for item in dataA:
###    print (str(it) +") " + item +"\n\n")
###    it = it + 1
###print("-------------------------------------------------------")
###it = 1
###for item in dataB:
###    print (str(it) +") " + item +"\n\n")
###    it = it + 1
#print(dataB)
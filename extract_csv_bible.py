import os
from collections import Counter
from pathlib import Path
import csv
from bs4 import BeautifulSoup


incoherences_verses = []
coherences_verses = []

def extract_verses_from_chapter(file, book, chapter):
    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()

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
        result.append(verse.get_text())
    return result


def extract_verses_from_chapter_notworking(file):
    result = []

    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    

    verses = soup.find_all("span", class_="ChapterContent_verse__57FIw")
    if len(verses) == 0:
        return [] 

    # Find all span elements with a data-usfm attribute
    for verse_span in verses:
        label = verse_span.find("span", class_="ChapterContent_label__R2PLt")
        if label:
            label.decompose()  # removes the tag completely
        
        text = verse_span.get_text(separator="", strip=True)
        if text.strip() != "":
            result.append(text)
        
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


def extract_book_chapter_to_csv(dialectFolder, englishFolder, dataTextFileDialect, dataTextFileEnglish, subfolderBook, bookCode, chapter):
    dialectAFile = dialectFolder + "/" + subfolderBook + "/" + dataTextFileDialect
    englishAFile = englishFolder + "/" + subfolderBook + "/" + dataTextFileEnglish
    csv_destinationFile = csv_bible + subfolderBook + "/" + subfolderBook + "_chap_" + chapter + ".csv"
    csv_destinationFileAll = csv_bible_all + "/" + subfolderBook + "_chap_" + chapter + ".csv" 
    
    print(dialectAFile+"++++"+bookCode+"++++"+chapter)
    arrayDialect = extract_verses_from_chapter(dialectAFile, bookCode, chapter)
    arrayEnglish = extract_verses_from_chapter(englishAFile, bookCode, chapter)
    arrayDestination = []
    
    status = " OK "
    if len(arrayDialect)!=len(arrayEnglish):
        status = " BAD "
    log = "Book : " + bookCode + " // Chapter: " + chapter + " Dialect/English: "+ str(len(arrayDialect)) +"/"+ str(len(arrayEnglish)) +" verses" + status + " ("+ dialectAFile +" ="+ englishAFile +")"
    print(log)
    
    if len(arrayDialect) == len(arrayEnglish):
        for i in range(0, len(arrayDialect)):
            arrayDestination.append({'ngiemboon':arrayDialect[i], 'en': arrayEnglish[i]})
        save_csv_data(arrayDestination, csv_destinationFile)
        save_csv_data(arrayDestination, csv_destinationFileAll)
        coherences_verses.append(log)
    else:
        incoherences_verses.append(log)
        


def constructing_csv(dialect, english, coreFolder, csv_bible):
    dialect = coreFolder + dialect['folder']
    english = coreFolder + english['folder']

    if not os.path.isdir(csv_bible_all):
        os.mkdir(csv_bible_all)
        
    subfolders_dialect = [f for f in os.listdir(dialect) if os.path.isdir(os.path.join(dialect, f))]
    subfolders_english = [f for f in os.listdir(english) if os.path.isdir(os.path.join(english, f))]
    
    if len(subfolders_dialect) != len(subfolders_english):
        return False

    for subfolderBook in subfolders_dialect:
        dialectA = dialect + "/" + subfolderBook
        englishA = english + "/" + subfolderBook
        
        subfolders_dialectBook = [f for f in os.listdir(dialectA) if not os.path.isdir(os.path.join(dialectA, f))]
        subfolders_englishBook = [f for f in os.listdir(englishA) if not os.path.isdir(os.path.join(englishA, f))]

        if len(subfolders_dialectBook) != len(subfolders_englishBook):
            continue

        bookFolder = csv_bible + subfolderBook
        bookFolder_path = Path(bookFolder)

        if not bookFolder_path.exists():
            bookFolder_path.mkdir(parents=True)
        
        for indx in range(1, 500):
            pattern = "_chap_" + str(indx) + ".html"
            resultDialect = [f for f in subfolders_dialectBook if f.endswith(pattern)]
            resultEnglish = [f for f in subfolders_englishBook if f.endswith(pattern)]
            if not (len(resultDialect) == 1 and len(resultEnglish) ==1):
                break
            print(subfolderBook + " ==> " + resultDialect[0] + " ==> " + resultEnglish[0])
            extract_book_chapter_to_csv(dialect, english, resultDialect[0], resultEnglish[0], subfolderBook, subfolderBook, str(indx))
        
    return True


biblesList = [
    {"folder": "NNH", "code": "4488"}, 
    #{"folder": "NGBM", "code": "299"}, 
    {"folder": "CSB", "code": "1713"}
    #{"folder": "KJV", "code": "1"}
]

core_bible = "core_bible/"
csv_bible = "csv_bible/"
csv_bible_all = "csv_bible/0_ALL/"
sourceDialete = biblesList[0]
destinationEnglish = biblesList[1]

if verification(sourceDialete, destinationEnglish, core_bible):
    constructing_csv(sourceDialete, destinationEnglish, core_bible, csv_bible)
    print("verification NOT OK")
else:
    print("verification NOT OK")

with open(csv_bible + "incoherences_verses.txt", "w", encoding="utf-8") as file:
    file.write("Dialete: " + sourceDialete['folder'] + "("+ sourceDialete['code'] +") /// English: " + destinationEnglish['folder'] + "("+ destinationEnglish['code'] +") " + "\n")
    for line in incoherences_verses:
        file.write(line + "\n")
with open(csv_bible + "coherences_verses.txt", "w", encoding="utf-8") as file:
    file.write("Dialete: " + sourceDialete['folder'] + "("+ sourceDialete['code'] +") /// English: " + destinationEnglish['folder'] + "("+ destinationEnglish['code'] +") " + "\n")
    for line in coherences_verses:
        file.write(line + "\n")

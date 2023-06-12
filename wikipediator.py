from libzim.reader import Archive
from libzim.search import Query, Searcher
from libzim.suggestion import SuggestionSearcher
from bs4 import BeautifulSoup
import re
import sqlite3
import os
from tqdm import tqdm

def process_zim(zim_path):
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("CREATE TABLE words(\
                word TEXT UNIQUE COLLATE NOCASE,\
                count INTEGER DEFAULT 1\
                );"
                )

    zim = Archive(zim_path)
    print(f"Articles to by scanned from {zim_path}: {zim.all_entry_count}")

    for index in tqdm(range(zim.all_entry_count)):
        entry = zim._get_entry_by_id(index)
        if (entry.path.startswith('A/')):
            #print(f"Processing entry {index}/{zim.all_entry_count}: {entry.title}")
            entry = (bytes(entry.get_item().content).decode("UTF-8"))
            soup = BeautifulSoup(entry, features="html.parser")
            text = soup.get_text()
            text = re.sub(r"[0-9]", "", text)
            text = re.findall(r"\w+", text)
            for word in text:
                sql=("INSERT INTO words(word) VALUES(?)\
                    ON CONFLICT(word) DO UPDATE SET count=count+1;")
                cur.execute(sql,(word,))
    db.commit()

    cur.execute("SELECT * FROM words ORDER BY count DESC")
    with open(f"{zim_path}.txt", "w", newline='\n') as f:
            for row in cur:
                print(row[0], file=f)
    with open(f'{zim_path}.sql', 'w') as p:    
        for line in db.iterdump():
            p.write('%s\n' % line)

    db.close()

for file in os.listdir("."):
    if file.endswith(".zim"):
        process_zim(file)
    else:
        continue

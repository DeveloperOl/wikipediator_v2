# Wikipediator_v2

This is a small python script I wrote to generate wordlists from `.zim`-files. It can be used to process topic- or language specific wikipedia dumps stored as `zim`-archives. Pre-crawled `zim`s can be found using google or here: [Index of /kiwix/zim/wikipedia](https://ftp.fau.de/kiwix/zim/wikipedia/)

# Usage

- place `zim`-files in same folder as the python script

```
pip3 install -r requirements.txt
python3 ./wikipediator.py
```

Result will be two files - an ordered wordlist by word occurence and an sql-file for manual investigation.

# Contributions

This is just a hacky script I wrote in a day - there is probably a lot improvement possible. Feel free to open PRs. If you want my opionion first, raise an issue.
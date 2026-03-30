import codecs
import os

try:
    with codecs.open('requirements.txt', 'r', 'utf-16le') as f:
        lines = f.readlines()
except UnicodeError:
    with codecs.open('requirements.txt', 'r', 'utf-8') as f:
        lines = f.readlines()

new_lines = []
for line in lines:
    line = line.strip()
    if not line: continue
    if line.startswith('easyocr') or line.startswith('torch'):
        continue
    new_lines.append(line)

new_lines.append('pytesseract')

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines) + '\n')

print("Updated requirements.txt successfully!")

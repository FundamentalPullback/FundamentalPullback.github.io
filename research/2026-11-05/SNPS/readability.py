import re

def spaced(text):
    # Preserve link targets, URLs, paths, code spans, and identifiers with hyphens.
    text=re.sub(r'\bQ([1-4])(20[0-9]{2})\b',r'Q\1 FY\2',text)
    text=re.sub(r'\bQ([1-4])FY',r'Q\1 FY',text)
    parts=re.split(r'(https?://[^\s)]+|\]\([^)]*\)|`[^`]*`|\bS3-SNPS-[\w-]+\b|\bA104\b|\bOpportunity100\b|\b(?:FY\d+|Q[1-4]|TTM\d+|9M\d+|S\d+)\b)',text)
    for i in range(0,len(parts),2):
        s=parts[i]
        s=re.sub(r'(?<=[A-Za-zÁÉÍÓÚáéíóúñÑ])(?=[0-9])',' ',s)
        s=re.sub(r'(?<=[0-9])(?=[A-Za-zÁÉÍÓÚáéíóúñÑ])',' ',s)
        s=re.sub(r'(?<=[%])(?=[A-Za-zÁÉÍÓÚáéíóúñÑ])',' ',s)
        parts[i]=s
    return ''.join(parts)

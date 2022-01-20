str = "https://gunet2.cs.unipi.gr/modules/document/document.php?course=TMA117&download=/50f69fea4uro.pdf"

substr = str[-10:len(str)]
if '.' not in substr:
    print(substr)
else:
    extension = substr[substr.index('.'): len(substr)]
    print(extension)
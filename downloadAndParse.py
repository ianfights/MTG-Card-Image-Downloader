import requests


def downloadSetImages(setCode, maxSetNum):
    print(f'Downloading Card Images for {setCode}')
    for i in range(1,maxSetNum+1):

        # Because the website has the card number exactly we need to add the leading zeros if necessary

        cardNumber = f"{i:03d}"
        # print(cardNumber)

        page = requests.get(f"https://www.mtgpics.com/card?ref={setCode}{cardNumber}")
        img_data = requests.get(f"https://www.mtgpics.com/pics/big/{setCode}/{cardNumber}.jpg").content
        page = str(page.content)

        # We need the card name, which can be found in the title 
        # So we find the index for the title tag, add its offset, and do the same thing for the closing tag.
        # Once that's done we clean up the string

        titleStart = page.find("<title>")
        title = page[titleStart + len("<title>"):]
        titleEnd = title.find("</title>")
        
        # Because wotc are a bunch of stupid fucks who have decided newer sets should have non-sequential numbering, I now have to check if the 
        # Card even fucking exists
        
        if title.find('-') == -1:
            # Card doesn't exist because fucking hasboro 
            continue
            
        
            
        
        # Also have to strip out /'s because the dual faced cars have / in thir name on this site
        # Also have to strip out 's because ¯\_(ツ)_/¯ unicode or something
        title = title[:titleEnd].split('-')[0].strip().split("/")[0].replace("&#039;","'")

        
        
        print(f'{setCode}-{cardNumber} - {title} - {i}/{maxSetNum}')



        with open(f"set-images/{setCode}/{title}.jpg", 'wb') as handler:
            handler.write(img_data)
# get only the verses from the kjv.json file and remove ambiguous unicode characters

import json

def main():
    # Load the JSON file
    with open('kjv.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # get rid of metadata
    bible_dict = data['verses']
    
    # get rid of ambiguous unicode characters
    for verse in bible_dict:
        verse['text'] = verse['text'].encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    
    # save as another JSON file
    with open('kjv_bible.json', 'w', encoding='utf-8') as f:
        json.dump(bible_dict, f, ensure_ascii=False, indent=4)
    
    
if __name__ == "__main__":
    main()
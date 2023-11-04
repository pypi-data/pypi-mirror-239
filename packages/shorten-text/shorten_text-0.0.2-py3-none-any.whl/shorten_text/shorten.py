def shorten_text(text):
    try:
        if text.isdigit():
            raise ValueError("Text should be alphabatic or alphanumeric")
    except AttributeError:
        return "should be a String"
    
    shorten_text = []
    
    WORD = text.upper()
    vowels=['A', 'E', 'I', 'O', 'U']
    for i in range(len(text)):
        if (WORD[i]  not in vowels):
            shorten_text.append(text[i])
            
    return ''.join(letter for letter in shorten_text)

def main():
    text = input("text: ")
    short_text = shorten_text(text)
    print(short_text)
    

if __name__ == '__main__':
    main()
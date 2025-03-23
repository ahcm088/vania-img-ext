from spellchecker import SpellChecker

# Initialize the spell checker
spell = SpellChecker(language='pt')

def correct_spelling(text):
    words = text.split()  # Split the text into words
    corrected_words = []

    for word in words:
        # Check if the word is misspelled
        corrected = spell.correction(word)
        
        # If the correction is None, use the original word
        if corrected is None:
            corrected = word
        
        corrected_words.append(corrected)

    # Join the corrected words back into a string
    corrected_text = " ".join(corrected_words)
    return corrected_text

# Sample texts
texts = [
    "Isso custa 1,A4 reais",
    "Eletrodomesticos como o Refrigador e fogão estão em promoção.",
    "Eu comprei um Sanduiche do Burger King por 10 dolares.",
    "Eu comprei um Sanduixe do Burger King por 10 dolares."
]

# Correct the spelling for each text
corrected_texts_spellchecker = [correct_spelling(text) for text in texts]

# Print the corrected texts
for original, corrected in zip(texts, corrected_texts_spellchecker):
    print(f"Original: {original}")
    print(f"Corrected: {corrected}\n")

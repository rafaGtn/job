import pymorphy2

# Initialize the pymorphy2 morphological analyzer
morph = pymorphy2.MorphAnalyzer()

# List of Russian electrical terminology items (to be filled with the actual terms)
terms = [
    # Add the 184 electrical terminology items here
]

# Open the output file
with open('sklonenie_result.txt', 'w', encoding='utf-8') as result_file:
    for term in terms:
        # Get the word's grammatical information
        parsed_word = morph.parse(term)[0]
        
        # Decline the word in all cases and both numbers
        results = {
            'nominative': [parsed_word.inflect({'nomn', 'sing'}).word, parsed_word.inflect({'nomn', 'plur'}).word],
            'genitive': [parsed_word.inflect({'gent', 'sing'}).word, parsed_word.inflect({'gent', 'plur'}).word],
            'dative': [parsed_word.inflect({'datv', 'sing'}).word, parsed_word.inflect({'datv', 'plur'}).word],
            'accusative': [parsed_word.inflect({'accs', 'sing'}).word, parsed_word.inflect({'accs', 'plur'}).word],
            'instrumental': [parsed_word.inflect({'ablt', 'sing'}).word, parsed_word.inflect({'ablt', 'plur'}).word],
            'prepositional': [parsed_word.inflect({'loct', 'sing'}).word, parsed_word.inflect({'loct', 'plur'}).word],
        }

        # Write the results to the output file
        result_file.write(f'{term}:\n')
        for case, forms in results.items():
            result_file.write(f'  {case}: {forms[0]} (singular), {forms[1]} (plural)\n')
        result_file.write('\n')

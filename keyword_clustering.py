import pandas as pd
import re

# Функция для чтения ключевых слов из файла
# Function to read keywords from the file

def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        keywords = file.readlines()
    return [keyword.strip() for keyword in keywords]

# Функция для классификации ключевых слов
# Function to classify keywords

def categorize_keywords(keywords):
    categories = {
        'valid': [],
        'invalid': []
    }
    subcategories = {
        'Cities': [],
        'Malls': [],
        'Restaurants': [],
        'Parks': [],
        'Monuments': [],
        'Hotels': []
    }
    trash_keywords = []

    # Регулярные выражения для фильтрации
    # Regex patterns for filtering
    trash_patterns = re.compile(r'просп\.|ул\.|адрес|локация|маршрут|координаты|как добраться', re.IGNORECASE)
    valid_patterns = re.compile(r'^(?!.*просп\.|ул\.|адрес|локация|маршрут).*$', re.IGNORECASE)

    for keyword in keywords:
        if trash_patterns.search(keyword):
            trash_keywords.append(keyword)
        elif valid_patterns.match(keyword):
            categories['valid'].append(keyword)
            # Определение подкатегорий
            # Determine subcategories
            if 'молл' in keyword.lower():
                subcategories['Malls'].append(keyword)
            elif 'ресторан' in keyword.lower():
                subcategories['Restaurants'].append(keyword)
            elif 'город' in keyword.lower():
                subcategories['Cities'].append(keyword)
            elif 'парк' in keyword.lower():
                subcategories['Parks'].append(keyword)
            elif 'монумент' in keyword.lower():
                subcategories['Monuments'].append(keyword)
            elif 'отель' in keyword.lower():
                subcategories['Hotels'].append(keyword)
    return categories, subcategories, trash_keywords

# Функция для экспорта результатов в CSV
# Function to export results to CSV

def export_to_csv(categories, subcategories, trash_keywords, output_file):
    records = []
    for category, kw_list in categories.items():
        for keyword in kw_list:
            records.append({'keyword': keyword, 'category': category, 'subcategory': '', 'is_trash': False})

    for subcategory, kw_list in subcategories.items():
        for keyword in kw_list:
            for record in records:
                if record['keyword'] == keyword:
                    record['subcategory'] = subcategory
                    break

    for keyword in trash_keywords:
        records.append({'keyword': keyword, 'category': 'invalid', 'subcategory': '', 'is_trash': True})

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False, encoding='utf-8')

# Функция для генерации статистического отчета
# Function to generate statistics report

def generate_statistics_report(categories, subcategories):
    print('Statistics Report:')
    print(f"Valid Queries: {len(categories['valid'])}")
    print(f"Invalid Queries: {len(categories['invalid'])}")
    for subcategory, kw_list in subcategories.items():
        print(f"{subcategory}: {len(kw_list)}")

# Главная функция
# Main function

def main():
    keywords = read_keywords('zapros.md')
    categories, subcategories, trash_keywords = categorize_keywords(keywords)
    export_to_csv(categories, subcategories, trash_keywords, 'keywords_classification.csv')
    generate_statistics_report(categories, subcategories)

if __name__ == '__main__':
    main()
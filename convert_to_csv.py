import csv


# Функция для обработки строк и извлечения логинов
def extract_logins_from_file(file_path):
    logins = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("Логины из комментариев:"):
                # Удаляем начальную часть строки "Логины из комментариев:" и разделяем оставшуюся строку по запятым
                extracted_logins = line.replace("Логины из комментариев:", "").strip().split(',')
                # Добавляем логины в набор, удаляя пробелы
                for login in extracted_logins:
                    stripped_login = login.strip()
                    if stripped_login:
                        logins.add(stripped_login)

    return logins


# Функция для записи логинов в CSV файл
def write_logins_to_csv(logins, output_file_path):
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Login'])  # Заголовок столбца
        for login in sorted(logins)[1:]:  # Сортировка логинов для удобства
            writer.writerow([login])


# Основной блок программы
input_file_path = 'output.txt'
output_file_path = 'logins.csv'

# Извлечение логинов из файла
logins = extract_logins_from_file(input_file_path)

# Запись логинов в CSV файл
write_logins_to_csv(logins, output_file_path)

print("CSV файл 'logins.csv' успешно создан.")

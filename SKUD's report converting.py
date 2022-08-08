# Преобразование выгрузки СКУД в удобно читаемый формат.

# Преобразование даты в формат гггг.мм.дд.
def converting_date(s):
    temp = s.split('.')[: : -1]
    return '.'.join(temp)

# Приведение времени к формату чч:мм:сс.
def normalizing_time(s):
    if s.index(':') == 1:
        return '0' + s
    else:
        return s

# Определение содержания строки: проход, название точки прохода или иное.
def identifing_string(s):
    temp = [i.strip('"') for i in s.split(';')]
    first_element = temp[0]
    if all((first_element[0 : 2].isdigit(), first_element[3 : 5].isdigit())):
        date = converting_date(first_element.split()[0])
        time = normalizing_time(first_element.split()[1])
        name = temp[4]
        return 'passage', name, date, time
    elif temp[1] == temp[2] == temp[3] == '':
        return first_element  # checkpoint
    else:
        pass

# Преобразование содержимого исходного файла в словарь вида:
# {ФИО: {дата: {время: точка прохода}}}.
def converting_input_file_to_dict():
    res_dict = {}
    checkpoint = ''
    file_name = input('Пожалуйста, введите имя и путь к файлу: ')
    with open(file_name, 'r', encoding='windows-1251') as file:
        for line in file:
            essence = identifing_string(line)
            if essence is None:
                continue
            elif essence[0] == 'passage':
                fio = essence[1]
                date = essence[2]
                time = essence[3]
                if fio in res_dict:
                    if date in res_dict[fio]:
                        res_dict[fio][date][time] = checkpoint
                    else:
                        res_dict[fio][date] = {time: checkpoint}
                else:
                    res_dict[fio] = {date: {time: checkpoint}}
            else:
                checkpoint = essence
    return writing_result_to_file(file_name, res_dict)

# Сохранение всех событий в файл.
def writing_result_to_file(f_name, result_dict):
    with open(f'{f_name}_converted.csv', 'w', encoding='windows-1251') as file:
        file.write('ФИО;Дата;Время;Точка прохода\n')
        for fio in result_dict:
            for date in result_dict[fio]:
                for time, checkpoint in result_dict[fio][date].items():
                    file.write(f'{fio};{date};{time};{checkpoint}\n')
        print('Исполнено.')


# Краткое описание требований к исходному файлу.
print('''Файл выгрузки СКУД необходимо сохранять в формате ".csv", а в качестве разделителя выбирать ";".
По умолчанию СКУД сохраняет файл в кодировке windows-1251 (ansi). В таком формате выгрузка из СКУД может быть здесь обработана.
Получаемый после обработки файл сохраняется в формате ".csv", кодировка windows-1251. Его можно открывать в MS Excel.
''')

# Основной цикл.    
again = '1'
while again == '1':
    converting_input_file_to_dict()
    again = input('Желаете повторить? (1 = да, любой иной символ = нет): ')
print('Всего доброго.')

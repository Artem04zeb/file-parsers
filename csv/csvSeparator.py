import pandas as pd
import os
import chardet
import json


def split_csv():
    print('Утилита дробления файла начала свою работу ...')
    with open('config.json', encoding='utf-8') as json_file:
        data = json.load(json_file)['Configuration']
        SourceInputFile = data['SourceInputFile']
        InputSeparator = data['InputSeparator']
        CountOfParts = int(data['CountOfParts'])
        OutputSeparator = data['OutputSeparator']
        OutputEncoding = data['OutputEncoding']

    # Определяем кодировку исходного файла
    with open(SourceInputFile, 'rb') as f:
        Inputencoding = chardet.detect(f.read())['encoding']

    # Читаем CSV файл
    df = pd.read_csv(SourceInputFile, encoding=Inputencoding, on_bad_lines='skip', sep=InputSeparator)
    
    # Определяем количество строк в файле
    total_rows = len(df)
    
    # Вычисляем количество строк в каждой части
    rows_per_file = total_rows // CountOfParts
    remainder = total_rows % CountOfParts

    # Создаем директорию для сохранения частей
    base_name = os.path.splitext(SourceInputFile)[0]
    os.makedirs(base_name, exist_ok=True)

    start_row = 0
    for i in range(CountOfParts):
        # Определяем количество строк для текущей части
        if i < remainder:
            end_row = start_row + rows_per_file + 1  # Добавляем одну строку для первых "remainder" файлов
        else:
            end_row = start_row + rows_per_file
        
        # Срезаем данные и сохраняем в новый CSV файл
        df.iloc[start_row:end_row].to_csv(os.path.join(base_name, f'part_{i+1}.csv'), index=False, encoding=OutputEncoding, sep=OutputSeparator)
        print('Создан файл №', i+1)
        
        # Обновляем начальную строку для следующей части
        start_row = end_row 
    
    print()
    print(f'CSV файл успешно разбит на {CountOfParts} частей и сохранен в директории "{base_name}".')
    input('Нажмите любую кнопку, чтобы закрыть окно консоли')

# Вызов главной функции
split_csv()

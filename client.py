import socket


HELP = '''    Приложение поддерживает команды для сохранения полученных данных
    save0, save1, ... save5 у каждого пользователя есть 6 ячеек для сохранения,
    для проверки состояния ячеек используйте команду: save,
    для загрузки из нужной ячейки используйте команду: load[номер ячейки 0-6],
    команды exit, close для выхода'''

HOST = ('localhost', 10000)  # адрес хоста

SAVED_DATA = {
    'save0' : None,
    'save1' : None,
    'save2' : None,
    'save3' : None,
    'save4' : None,
    'save5' : None,
}  # написсал сохранение как 6 свободных ячеек


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect(HOST)
# UDP соединение

def add_saved_data(data, position):  # функция для сохранения последнего ответа
    try:
        SAVED_DATA[position] = data
        print(f'{data} сохранена в {position}')
    except NameError:
        print("Не удалось сохранить")


def send_to_server(data):  # отправка данных на сервер по соединению
    client.sendto(input_data.encode('utf-8'), HOST)
    data = client.recvfrom(4098)[0].decode()  # получение ответа от сервера
    print(data)
    return data


def load_data(data):  # функция для загузки сохранённых данных  поддерживает множестенную загрузку "load0+load0**load0"
    try:
        if 'load' in data:
            for i in range(len(SAVED_DATA)):
                if f'load{i}' in data : splited_data = data.replace(f'load{i}', SAVED_DATA[f'save{i}'])
            load_data(splited_data)
        else:  # load(ов) больше не осталось, готовое выражение отправляем на сервер и получаем ответ
            client.sendto(data.encode('utf-8'), HOST)
            data = client.recvfrom(4098)[0].decode()
            print(data)

    except (UnboundLocalError, TypeError):
        print('Не удалось вычеслить, возможно была совершена ошибка')


while True:
    input_data = input("Введите help или математическое выражение: ").lstrip().rstrip()
    if input_data:
        if input_data in ('exit', 'close'):  # функционал команд exit, close 
            break
        elif input_data in ('help'):# функционал команды help
            print(HELP)

        elif 'load' in input_data:  # функционал команды laod
            load_data(input_data)

        elif 'save' in input_data:  # функционал команды save
            try:
                if input_data in ({'save' + str(i) for i in range(6)}):  # если команда save[0-5]
                    add_saved_data(data, input_data)  # передаём последные полученные данные и команду save[0-5]
                elif input_data == 'save':# если команда save
                    print(SAVED_DATA.items())
                else:
                    print('Команда save может быть без аргументов "save" или поддерживает значения от 0 до 5 "save1"')
            except NameError:  # отлавливает исключение если при использовании save[0-5] переменная data отсутствует
                print('Не удалось сохранить')

        else :  # данные прошли все стадии обработки и отправляются на сервер
            data = send_to_server(input_data)


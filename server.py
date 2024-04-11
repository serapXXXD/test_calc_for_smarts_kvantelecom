import socket
from numexpr import evaluate

HOST = ('localhost', 10000)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(HOST)
print('Сервер запущен...')
# UDP соединение

def math_expression(expression: str):  # функция для обработки полученной информации
    try:
        res = evaluate(expression)  # выполнение вычисления выражения
        server.sendto(str(res).encode(), addr)  # отправка ответа клиенту
    except:
        res = 'Не удаллось произвести вычесление'
        server.sendto(res.encode(), addr)


while True:  # поддержка соединения 
    data, addr = server.recvfrom(4096)  # получение запроса
    print(f'Новое соединение с {addr}: {data.decode()}')
    math_expression(data.decode('utf-8'))  # передача запроса в функцию для вычисления выражения

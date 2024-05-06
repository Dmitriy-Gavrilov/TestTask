from operations import *


def operation_input(wallet: Wallet) -> Operation:
    """Функция создания объекта операции и обработки пользовательского ввода"""
    status: str = input("Введите тип операции (Доход/Расход): ")
    while status != "Доход" and status != "Расход":
        print("Неверный тип операции")
        status = input("Введите тип операции (Доход/Расход): ")

    while True:
        try:
            date: dt.date = dt.datetime(*list(map(int, input("Введите дату в формате YYYY-MM-DD: ").split("-")))).date()
            if date < wallet.current_date:
                raise ValueError
            break
        except ValueError:
            print("Некорректная дата")

    value_input: str = input("Введите сумму: ")
    while not all(x.isdigit() for x in value_input):
        print("При вводе суммы должны использоваться только цифры")
        value_input: str = input("Введите сумму: ")
    value: int = int(value_input)

    description: str = input("Введите описание операции: ")

    return Operation(status, date, value, description)


def main():
    wallet = Wallet()
    wallet.read_args()
    if wallet.load_data():
        print("Данные успешно загружены из файла")
    else:
        print("Файл не найден. Данные не загружены")

    while True:
        choice = input("1 - Добавить запись\n"
                       "2 - Изменить запись\n"
                       "3 - Удалить запись\n"
                       "4 - Очистить данные о записях\n"
                       "5 - Просмотр баланса\n"
                       "6 - Просмотр записей\n"
                       "7 - Сохранить операции в файл\n"
                       "8 - Очистить данные в файле\n"
                       "9 - Выход\n")

        match choice:
            case "1":
                if wallet.add(operation_input(wallet)):
                    print("Операция успешно добавлена")
                else:
                    print("Невозможно добавить операцию")
            case "2":
                index: int = int(input("Введите порядковый номер операции (начиная с 0): "))
                print("Введите новую операцию")
                if wallet.update(index, operation_input(wallet)):
                    print("Операция успешно изменена")
                else:
                    print("Невозможно изменить операцию")
            case "3":
                index: int = int(input("Введите порядковый номер операции (начиная с 0): "))
                if wallet.delete(index):
                    print("Операция успешно удалена")
                else:
                    print("Невозможно удалить операцию")
            case "4":
                wallet.clear_wallet()
                print("Записи успешно очищены")
            case "5":
                wallet.print_balance()
            case "6":
                print(wallet)
            case "7":
                if wallet.save_data():
                    print("Данные успешно сохранены")
                else:
                    print("Ошибка при сохранении данных")
            case "8":
                if wallet.clear_file():
                    print("Данные в файле успешно очищены")
                else:
                    print("Ошибка. Файл не найден")
            case "9":
                break
            case _:
                print("Неизвестная команда")


if __name__ == "__main__":
    main()
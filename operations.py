import sys
import datetime as dt
import csv


class Operation:
    """Класс для представления операции"""

    def __init__(self, status: str, date: dt.date, value: int, description: str) -> None:
        self.__status = status
        self.__date = date
        self.__value = value
        self.__description = description

    def __str__(self) -> str:
        return (f"Дата: {self.__date}\n"
                f"Тип операции: {self.status}\n"
                f"Сумма: {self.__value}\n"
                f"Описание: {self.__description}\n")

    # Геттеры и сеттеры для полей класса
    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str) -> None:
        self.__status = status

    @property
    def date(self) -> dt.date:
        return self.__date

    @date.setter
    def date(self, date: dt.date) -> None:
        self.__date = date

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int) -> None:
        self.__value = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description


class Wallet:
    """
    Класс-коллекция для хранения и обработки операций

    Операции:
            add:            добавление элемента
            delete:         удаление элемента
            update:         изменение элемента
            clear_wallet:   очистка коллекции
            print_balance:  вывод баланса
            read_args:      считывание имени файла как аргумента командной строки
            load_data:      Загрузка данных из файла в коллекцию
            save_data:      Сохранение данных из коллекции в файл
            clear_file:     Очистка данных в файле
    """

    def __init__(self, balance: int = 0) -> None:
        self.__wallet: list[Operation] = []
        self.__balance = balance
        self.__current_date: dt.date = dt.date.min

        self.__filename: str = ""

    def __str__(self) -> str:
        result: str = ""
        for i in range(len(self.__wallet)):
            result += f"{i})\n{str(self.__wallet[i])}"

        return result if result else "Нет операций"

    # Геттер и сеттер для поля даты
    @property
    def current_date(self) -> dt.date:
        return self.__current_date

    @current_date.setter
    def current_date(self, new_date: dt.date) -> None:
        self.__current_date = new_date

    def read_args(self) -> None:
        if len(sys.argv) > 1:
            self.__filename = sys.argv[1]

    def print_balance(self) -> None:
        print(f"Текущий баланс: {self.__balance}")

    @staticmethod
    def __update_balance(status: str, value: int, balance: int) -> int:
        match status:
            case "Доход":
                return balance + value
            case "Расход":
                return balance - value

    def add(self, operation: Operation) -> bool:
        new_balance: int = self.__update_balance(operation.status, operation.value, self.__balance)
        if new_balance >= 0:
            self.__balance = new_balance
            self.__current_date = operation.date
            self.__wallet.append(operation)
            return True
        else:
            return False

    def delete(self, index: int) -> bool:
        if index >= len(self.__wallet):
            return False

        wallet_copy: list[Operation] = []
        balance_copy: int = 0
        is_del: bool = False

        for i in range(len(self.__wallet)):
            if i == index:
                is_del = True
            else:
                if not is_del:
                    balance_copy = self.__update_balance(self.__wallet[i].status, self.__wallet[i].value, balance_copy)
                    wallet_copy.append(self.__wallet[i])
                else:
                    new_balance: int = self.__update_balance(self.__wallet[i].status, self.__wallet[i].value,
                                                             balance_copy)
                    if new_balance >= 0:
                        balance_copy = new_balance
                        wallet_copy.append(self.__wallet[i])
                    else:
                        return False

        self.__balance = balance_copy
        del self.__wallet[index]
        return True

    def update(self, index: int, operation: Operation) -> bool:
        if index >= len(self.__wallet):
            return False

        wallet_copy: list[Operation] = []
        balance_copy: int = 0
        is_change = False

        for i in range(len(self.__wallet)):
            if i == index:
                is_change = True
                new_balance: int = self.__update_balance(operation.status, operation.value, balance_copy)
                if new_balance >= 0:
                    balance_copy = new_balance
                    wallet_copy.append(self.__wallet[i])
                else:
                    return False
            else:
                if not is_change:
                    balance_copy = self.__update_balance(self.__wallet[i].status, self.__wallet[i].value, balance_copy)
                    wallet_copy.append(self.__wallet[i])
                else:
                    new_balance: int = self.__update_balance(self.__wallet[i].status, self.__wallet[i].value,
                                                             balance_copy)
                    if new_balance >= 0:
                        balance_copy = new_balance
                        wallet_copy.append(self.__wallet[i])
                    else:
                        return False

        self.__balance = balance_copy
        self.__wallet[index] = operation
        return True

    def clear_wallet(self) -> None:
        self.__wallet.clear()
        self.__balance = 0

    def load_data(self) -> bool:
        try:
            with open(self.__filename, encoding="utf-8") as f:
                reader = csv.reader(f)
                self.__wallet.clear()
                self.__balance = 0
                for row in reader:
                    if row:
                        self.add(Operation(row[0], dt.datetime.strptime(row[1], "%Y-%m-%d").date(),
                                           int(row[2]), row[3]))
            return True
        except FileNotFoundError:
            return False

    def save_data(self) -> bool:
        try:
            with open(self.__filename, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                for operation in self.__wallet:
                    data = [operation.status, str(operation.date), str(operation.value), operation.description]
                    writer.writerow(data)
            return True
        except FileNotFoundError:
            return False

    def clear_file(self) -> bool:
        try:
            with open(self.__filename, "w") as f:
                csv.writer(f).writerow("")
            return True
        except FileNotFoundError:
            return False


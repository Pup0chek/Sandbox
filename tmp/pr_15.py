class Mixin:
    def __add__(self, other):
        if isinstance(self, str) and isinstance(other, str):
            return self.__class__(super().__add__(other))

        elif isinstance(self, str) and isinstance(other, list):
            return self.__class__(self + ''.join(map(str, other)))

        elif isinstance(self, list) and isinstance(other, list):
            return self.__class__(super().__add__(other))

        elif isinstance(self, list) and isinstance(other, str):
            new_list = self.copy()
            new_list.append(other)
            return self.__class__(new_list)
        else:
            raise TypeError(f"Unsupported operand types for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __isub__(self, other):
        if isinstance(self, str) and isinstance(other, str):
            return self.__class__(self.replace(other, ''))

        elif isinstance(self, list) and isinstance(other, list):
            self[:] = [item for item in self if item not in other]
            return self

        elif isinstance(self, list) and isinstance(other, str):
            self[:] = [item for item in self if item != other]
            return self

        elif isinstance(self, str) and isinstance(other, list):
            result = self
            for elem in other:
                if isinstance(elem, str):
                    result = result.replace(elem, '')
            return self.__class__(result)
        else:
            raise TypeError(f"Unsupported operand types for -=: '{type(self).__name__}' and '{type(other).__name__}'")


class A(Mixin, str):
    def __new__(cls, value):
        # Применяем фильтр: удаляем пробелы по краям
        filtered_value = value.strip()
        return super().__new__(cls, filtered_value)


class B(Mixin, list):
    def __init__(self, iterable):
        # Применяем фильтр: удаляем дубликаты, сохраняя порядок
        filtered_list = []
        seen = set()
        for item in iterable:
            if item not in seen:
                seen.add(item)
                filtered_list.append(item)
        super().__init__(filtered_list)


# Примеры использования:

if __name__ == "__main__":
    # Создаем экземпляры классов A и B
    a1 = A("  Привет ")
    a2 = A("Мир")
    b1 = B([1, 2, 3, 2])
    b2 = B([3, 4])

    print("a1:", a1)
    print("a2:", a2)
    print("b1:", b1)
    print("b2:", b2)

    # Операции сложения
    a3 = a1 + a2
    print("a1 + a2:", a3)

    a4 = a1 + b1
    print("a1 + b1:", a4)

    b3 = b1 + a2
    print("b1 + a2:", b3)

    b4 = b1 + b2
    print("b1 + b2:", b4)

    # Операции вычитания
    a5 = A("ПриветМир")
    print("a5:", a5)
    a5 -= "Мир"
    print("a5 после -= 'Мир':", a5)

    b5 = B([1, 2, 3, 4, 5])
    print("b5:", b5)
    b5 -= [2, 4]
    print("b5 после -= [2, 4]:", b5)

    a6 = A("Привет123")
    print("a6:", a6)
    a6 -= b1
    print("a6 после -= b1:", a6)

    b6 = B([1, "Мир", 3, "Привет"])
    print("b6:", b6)
    b6 -= "Мир"
    print("b6 после -= 'Мир':", b6)

    b7 = B([1, 2, 3, 2])
    a7 = A("Мир")
    b7-= a7
    print("b7:", b7)


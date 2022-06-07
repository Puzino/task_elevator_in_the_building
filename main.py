import sys
from random import randint, choice
from time import sleep

"""Класс для создания размера здания и людей на этаже"""


class People:
    """
    Инициализирует размер здания, создает пустой список с людьми на этаже
    наполняет в функции (_people_floors).
    """

    def __init__(self):
        self.floors = randint(5, 21)
        self.people_on_floors = []

    def _people_floors(self):
        """Создает список со случайными людьми которым нужно на определенный этаж."""
        people = []
        for i in range(1, self.floors + 1):
            for _ in range(randint(0, 10)):
                x = randint(1, self.floors)
                if x != i:
                    people.append(x)
            self.people_on_floors.append(people)
            people = []


"""Класс наполнения словаря с людьми."""


class Elevator(People):
    """Инициализирует список"""

    def __init__(self):
        super(Elevator, self).__init__()
        self.elevator = {}

    def _button_for_elevator(self, floor):
        """Генерирует кнопки (Вверх/Вниз)"""
        x = ''
        people = self.people_on_floors[floor]
        if floor == 0:
            x = 'Up'
        elif self.floors == floor + 1:
            x = 'Down'
        elif len(people) == 0:
            x = ''
        elif len(people) >= 1:
            if people[0] > floor:
                x = 'Up'
            else:
                x = 'Down'
        return x

    def _create(self):
        """Наполнение списка"""
        self._people_floors()
        for floor in range(self.floors):
            x = self._button_for_elevator(floor)

            self.elevator[floor + 1] = {
                'people': self.people_on_floors[floor],
                'button': x,
                'people_exit': 0,
            }


"""Класс запуска логики лифта"""


class Run(Elevator):
    """Инициализируем пустой лифт (Наполняется по мере прохождения по этажам). Кнопка направления лифта. """

    def __init__(self):
        super(Run, self).__init__()
        self.button_lift = ''
        self.lift = []

    def _distributor(self, idx, btn):
        """Добавляет людей в лифт с этажа"""
        peoples = self.elevator[idx]['people']
        self._output(idx=idx)
        for _ in range(len(peoples)):
            self._btn(idx=idx)
            if len(self.lift) < 5 and btn == self.button_lift and btn == self.elevator[idx]['button']:
                try:
                    self.lift.append(peoples[0])
                    del peoples[0]

                except IndexError:
                    continue

    def _output(self, idx):
        """Убирает со списка людей которым нужно выйти на конкретном этаже. Добавляет человека со случайным этажом."""
        for _ in range(len(self.lift)):
            if idx in self.lift:
                self.lift.remove(idx)
                self.elevator[idx]['people_exit'] += 1
                self._input(idx=idx)

    def _input(self, idx):
        """Добавляет на вышедшем этаже нового человека со случайным этажом."""
        x = choice([x for x in range(1, self.floors + 1) if x != idx])
        self.elevator[idx]['people'].append(x)

    def _btn(self, idx):
        """Переоределяет кнопи лифта на этаже"""
        btn = self.elevator[idx]['people']
        if btn[0] > idx:
            self.elevator[idx]['button'] = 'Up'
        elif btn[0] < idx:
            self.elevator[idx]['button'] = 'Down'


class Print(Run):
    """
    Инициализирует количество этажей для прохождения по списку.
    Максимальный этаж, минимальный этаж.
    Счётчик определяющий завершение программы если на этажах больше нет людей.
    Активирует функцию создания словаря.
    """

    def __init__(self):
        super(Print, self).__init__()
        self.count = 1
        self.max_lift = self.floors
        self.min_lift = 1

        self._create()

    def _conclusion(self, count):
        """Вывод в консоль результата."""
        sys.stdout.write(
            f"\rЭтаж: {count}. Exit: {self.elevator[count]['people_exit']} |  {self.lift}  |{self.elevator[count]['button']}| {self.elevator[count]['people']}")
        sleep(1)

    def _up(self):
        """Логика движения лифта вверх."""
        while self.count <= self.max_lift:
            # Кнопка лифта
            self.button_lift = 'Up'
            # Принт в консоль
            self._conclusion(count=self.count)
            # Добавление людей в лифт
            self._distributor(idx=self.count, btn=self.elevator[self.count]['button'])

            if self.count == self.max_lift:  # Условие, если этаж человека был достигнут,
                # (макс. этаж человека в лифте),
                # запустить обатный порядок.
                self._down()
            elif len(self.lift) == 0:  # Иначе-если, лифт пустой, ехать к максимальному этажу.
                self.max_lift = self.floors
            else:  # Высчитывает макс. этаж.
                self.max_lift = max(self.lift)

            self.count += 1

    def _down(self):
        """Логика движения лифта вниз."""
        while self.count >= self.min_lift:
            # Кнопка лифта
            self.button_lift = 'Down'
            # Принт в консоль
            self._conclusion(count=self.count)
            # Добавление людей в лифт
            self._distributor(idx=self.count, btn=self.elevator[self.count]['button'])

            if len(self.lift) == 0:  # Иначе-если, лифт пустой, ехать к минимальному этажу.
                self.min_lift = 1

            else:  # Высчитывает мин. этаж.
                self.min_lift = min(self.lift)

            self.count -= 1


Print()._up()

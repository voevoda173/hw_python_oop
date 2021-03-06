from dataclasses import asdict, dataclass
from typing import ClassVar, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    Содержит следующие параметры:
    training_type - тип тренировки,
    duration - время тренировки в часах,
    distance - преодоленная дистанция в километрах,
    speed - средняя скорость движения в километрах в час
    calories - количество потряченных калорий в ккал.
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TEXT_INFO: str = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.'
                      )

    def get_message(self) -> str:
        return self.TEXT_INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки.
    Содержит следующие параметры:
    action: int - количество базовых движений в тренировке в единицах,
    duration: float - время тренировки в часах,
    weight: float - вес спортсмена в килограммах.
    """

    action: int = 0
    duration: float = 0
    weight: float = 0

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Не определен метод расчета количества'
                                  f'потраченных каллорий для тренировки типа'
                                  f' {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )
        return info_message


@dataclass
class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTI_RUN: ClassVar[int] = 18
    SPEED_CORRECTOR: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.SPEED_MULTI_RUN * self.get_mean_speed()
             - self.SPEED_CORRECTOR) * self.weight / self.M_IN_KM
            * self.duration * self.M_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height - рост спортсмена в сантиметрах.
    """

    height: float = 0

    WEIGHT_MULTI: ClassVar[float] = 0.035
    SPEED_MULTI_WLK: ClassVar[float] = 0.029
    SPEED_ERECT: ClassVar[float] = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        weight_adj = self.WEIGHT_MULTI * self.weight
        speed_adj = (
            (self.get_mean_speed() ** self.SPEED_ERECT // self.height)
            * self.SPEED_MULTI_WLK
        )
        duration_min = self.duration * self.M_IN_H
        return((weight_adj + speed_adj * self.weight) * duration_min)


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
        LEN_STEP - длина гребка спортсмена в метрах,
        length_pool - длина бассейна в метрах,
        count_pool - количество бассейнов, преодоленных спортсменом.
    """

    length_pool: int = 25
    count_pool: int = 0

    LEN_STEP: ClassVar[float] = 1.38
    SPEED_ADD: ClassVar[float] = 1.1
    SPEED_MULTI_SWM: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_ADD)
            * self.SPEED_MULTI_SWM * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_dict: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return training_type_dict[workout_type](*data)
    except KeyError:
        raise KeyError(f'Тип тренировки {workout_type}  не определен')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        print(training.show_training_info().get_message())
    except AttributeError:
        print('Не хватает данных.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

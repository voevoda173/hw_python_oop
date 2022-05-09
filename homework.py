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
    TEXT_INFO: str = ('Тип тренировки: {}; '
                      'Длительность: {:.3f} ч.; '
                      'Дистанция: {:.3f} км; '
                      'Ср. скорость: {:.3f} км/ч; '
                      'Потрачено ккал: {:.3f}.'
                      )

    def get_message(self) -> str:
        return self.TEXT_INFO.format(*asdict(self).values())


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
    H_IN_M: ClassVar[int] = 60

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

    COEFF_CAL_RUN_1: ClassVar[int] = 18
    COEFF_CAL_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        """
        return (
            (self.COEFF_CAL_RUN_1 * self.get_mean_speed()
             - self.COEFF_CAL_RUN_2) * self.weight / self.M_IN_KM
            * self.duration * super().H_IN_M
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    height - рост спортсмена в сантиметрах.
    """

    height: float = 0
    COEFF_CAL_WLK_1: ClassVar[float] = 0.035
    COEFF_CAL_WLK_2: ClassVar[float] = 0.029
    COEFF_CAL_WLK_3: ClassVar[float] = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        """
        return(
            (self.COEFF_CAL_WLK_1 * self.weight + (self.get_mean_speed()
             ** self.COEFF_CAL_WLK_3 // self.height) * self.COEFF_CAL_WLK_2
             * self.weight) * self.duration * super().H_IN_M
        )


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
    COEFF_CAL_SWM_1: ClassVar[float] = 1.1
    COEFF_CAL_SWM_2: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        """
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий.
        """
        return (
            (self.get_mean_speed() + self.COEFF_CAL_SWM_1)
            * self.COEFF_CAL_SWM_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_type_dict: Dict[str, str] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}
        return training_type_dict[workout_type](*data)
    except TypeError:
        print('Указанный тип тренировки не поддерживается.')


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
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

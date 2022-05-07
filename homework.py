class InfoMessage:
    """Информационное сообщение о тренировке.
    Содержит следующие параметры:
    training_type - тип тренировки,
    duration - время тренировки в часах,
    distance - преодоленная дистанция в километрах,
    speed - средняя скорость движения в километрах в час
    calories - количество потряченных калорий в ккал.
    """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.'
               )


class Training:
    """Базовый класс тренировки.
    Содержит следующие параметры:
    action - количество базовых движений в тренировке в единицах,
    duration - время тренировки в часах,
    weight - вес спортсмена в килограммах.
    Содержит следующие переменные класса:
    M_IN_KM - коэффициент расстояния, необходимый для перевода
    километров в метры,
    LEN_STEP - длина шага спортсмена в метрах.
    """

    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )
        return info_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий
        cf_run_1, cf_run_2 - коэффициенты, используемые для расчета
        количества потраченных калорий в тренировке Running.
        cal_run_1 - расчет предварительного значения, которое
        используется для расчета количества потраченных калорий
        в тренировке Running.
        """
        cf_run_1 = 18
        cf_run_2 = 20
        cal_run_1 = (cf_run_1 * self.get_mean_speed() - cf_run_2) * self.weight
        calories = cal_run_1 / self.M_IN_KM * (self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий
        cf_wlk_1, cf_wlk_2 - коэффициенты, используемые для расчета
        количества потраченных калорий в тренировке SportsWalking.
        cal_wlk_1, cal_wlk_2, cal_wlk_2 - расчет предварительного значения,
        которое используется для расчета количества потраченных калорий
        в тренировке Running.
        """
        cf_wlk_1 = 0.035
        cf_wlk_2 = 0.029
        cal_wlk_1 = cf_wlk_1 * self.weight
        cal_wlk_2 = self.get_mean_speed()**2 // self.height
        cal_wlk_3 = cal_wlk_2 * cf_wlk_2 * self.weight
        calories = (cal_wlk_1 + cal_wlk_3) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание.
        LEN_STEP - длина гребка спортсмена в метрах,
        length_pool - длина бассейна в метрах,
        count_pool - количество бассейнов, преодоленных спортсменом.
    """

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения
        cal_swm_1 - расчет предварительного значения,
        которое используется для расчета средней скорости движения.
        """
        cal_swm_1 = self.length_pool * self.count_pool
        mean_speed = cal_swm_1 / super().M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> int:
        """Получить количество затраченных калорий.
        cf_swm_1, cf_swm_2 - коэффициенты, используемые для расчета
        количества потраченных калорий в тренировке Swimming.
        """
        cf_swm_1 = 1.1
        cf_swm_2 = 2
        calories = (self.get_mean_speed() + cf_swm_1) * cf_swm_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    return training_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

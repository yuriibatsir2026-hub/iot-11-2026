from functools import singledispatchmethod


class TimeConverter:
    def __init__(self, seconds=0):
        self.set_seconds(seconds)

    def __del__(self):
        print("Об’єкт TimeConverter видалено.")

    def get_seconds(self):
        return self.__seconds

    def set_seconds(self, seconds):
        if type(seconds) is not int:
            raise TypeError("Кількість секунд має бути цілим числом.")
        if seconds < 0:
            raise ValueError("Кількість секунд має бути невід’ємною.")
        self.__seconds = seconds

    @singledispatchmethod
    def outputConvertedTime(self, value):
        raise TypeError("Передайте рядок hh:mm:ss або ціле число секунд.")

    @outputConvertedTime.register(str)
    def _output_from_text(self, value):
        hours, minutes, seconds = value.split(":")
        if len(hours) < 2 or len(minutes) != 2 or len(seconds) != 2:
            raise ValueError("Введіть час у форматі hh:mm:ss.")
        if not value.replace(":", "").isdecimal():
            raise ValueError("Введіть час у форматі hh:mm:ss.")

        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        if minutes > 59 or seconds > 59:
            raise ValueError("Хвилини й секунди мають бути від 00 до 59.")

        self.set_seconds(hours * 3600 + minutes * 60 + seconds)
        print(f"{value} = {self.get_seconds()} с")

    @outputConvertedTime.register(int)
    def _output_from_seconds(self, value):
        self.set_seconds(value)
        hours = value // 3600
        minutes = (value % 3600) // 60
        seconds = value % 60
        print(f"{value} с = {hours:02d}:{minutes:02d}:{seconds:02d}")


def main():
    converter = TimeConverter()

    converter.outputConvertedTime("01:02:03")
    converter.outputConvertedTime(converter.get_seconds())

    try:
        user_input = input("\nВведіть час hh:mm:ss або кількість секунд: ").strip()
        if ":" in user_input:
            converter.outputConvertedTime(user_input)
        else:
            converter.outputConvertedTime(int(user_input))
    except ValueError as error:
        print(f"Помилка: {error}")

    del converter


if __name__ == "__main__":
    main()

import csv
import datetime
import re
from prettytable import PrettyTable

def is_correct_input(filter: str, sort_param: str, is_reverse_sort: str) -> bool:
    if (filter != ""):
        if (':' not in filter):
            print("Формат ввода некорректен")
            return False
        else:
            field = filter[:filter.index(":")]
            if (field not in fields_dict.values()):
                print("Параметр поиска некорректен")
                return False
    if (sort_param != "" and sort_param not in dic_naming.values()):
        print("Параметр сортировки некорректен")
        return False
    if (is_reverse_sort != "Да" and is_reverse_sort != "Нет" and is_reverse_sort != ""):
        print("Порядок сортировки задан некорректно")
        return False
    return True

def bool_parse(item: str) -> bool:
    if (item == "Да"):
        return True
    return False

class Vacancy:
    def __init__(self, item: dict):
        self.__name = item["name"]
        self.__description = item["description"]
        self.__key_skills = item["key_skills"].split("; ")
        self.__experience_id = item["experience_id"]
        self.__premium = item["premium"]
        self.__employer_name = item["employer_name"]
        self.salary = Salary(item)
        self.__area_name = item["area_name"]
        self.__published_at = item["published_at"]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def key_skills(self):
        return self.__key_skills

    @key_skills.setter
    def key_skills(self, key_skills):
        self.__key_skills = key_skills

    @property
    def experience_id(self):
        return self.__experience_id

    @experience_id.setter
    def experience_id(self, experience_id):
        self.__experience_id = experience_id

    @property
    def premium(self):
        return self.__premium

    @premium.setter
    def premium(self, premium):
        self.__premium = premium

    @property
    def employer_name(self):
        return self.__employer_name

    @employer_name.setter
    def employer_name(self, employer_name):
        self.__employer_name = employer_name

    @property
    def area_name(self):
        return self.__area_name

    @area_name.setter
    def area_name(self, area_name):
        self.__area_name = area_name

    @property
    def published_at(self):
        return self.__published_at

    @published_at.setter
    def published_at(self, published_at):
        self.__published_at = published_at

class Salary:
    def __init__(self, item: dict):
        self.__salary_from = item["salary_from"]
        self.__salary_to = item["salary_to"]
        self.__salary_currency = item["salary_currency"]
        self.__salary_gross = item["salary_gross"]

    @property
    def salary_from(self):
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, salary_from):
        self.__salary_from = salary_from

    @property
    def salary_to(self):
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, salary_to):
        self.__salary_to = salary_to

    @property
    def salary_currency(self):
        return self.__salary_currency

    @salary_currency.setter
    def salary_currency(self, salary_currency):
        self.__salary_currency = salary_currency

    @property
    def salary_gross(self):
        return self.__salary_gross

    @salary_gross.setter
    def salary_gross(self, salary_gross):
        self.__salary_gross = salary_gross

    def get_salary(self):
        return '{0:,}'.format(int(float(self.salary_from) // 1)).replace(',', ' ') + " - " + \
                        '{0:,}'.format(int(float(self.salary_to) // 1)).replace(',', ' ') + \
                        f" ({currency_dict[self.salary_currency]}) " \
                        f"({'Без вычета налогов' if (self.salary_gross == 'True' or self.salary_gross == 'TRUE') else 'С вычетом налогов'})"

class DataSet:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__data = self.universal_csv_parser()
        self.__vacancies_objects = [Vacancy(item) for item in self.data]

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name):
        self.__file_name = file_name

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def vacancies_objects(self):
        return self.__vacancies_objects

    @vacancies_objects.setter
    def vacancies_objects(self, vacancies_objects):
        self.__vacancies_objects = vacancies_objects

    def clear_tags(self, string: str) -> str:
        pattern = r"<[^>]*>"
        s = re.sub(pattern, '', string)
        return s

    def clear_spaces(self, string: str) -> str:
        s = " ".join(string.split())
        return re.sub(" +", " ", s).strip()

    def clear_line(self, line: list) -> list:
        for i in range(len(line)):
            line[i] = self.clear_spaces(self.clear_tags("; ".join(line[i].split("\n"))))
        return line

    def universal_csv_parser(self) -> list:
        with open(self.file_name, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            header = []
            info = []
            for line in reader:
                if (header == []):
                    header = line
                    lineLength = len(header)
                else:
                    if ("" not in line and len(line) == lineLength):
                        info.append(dict(zip(header, self.clear_line(line))))
        if (header == []):
            print("Пустой файл")
            exit()
        return info

class InputConect:
    def __init__(self, data: list, filter: str, sort_param: str, is_reverse_sort: bool, rows_range: list, fields_to_show: list):
        self.__data = data
        self.__filter = filter
        self.__sort_param = sort_param
        self.__is_reverse_sort = is_reverse_sort
        self.__rows_range = rows_range
        self.__fields_to_show = fields_to_show

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, filter):
        self.__filter = filter

    @property
    def sort_param(self):
        return self.__sort_param

    @sort_param.setter
    def sort_param(self, sort_param):
        self.__sort_param = sort_param

    @property
    def is_reverse_sort(self):
        return self.__is_reverse_sort

    @is_reverse_sort.setter
    def is_reverse_sort(self, is_reverse_sort):
        self.__is_reverse_sort = is_reverse_sort

    @property
    def rows_range(self):
        return self.__rows_range

    @rows_range.setter
    def rows_range(self, rows_range):
        self.__rows_range = rows_range

    @property
    def fields_to_show(self):
        return self.__fields_to_show

    @fields_to_show.setter
    def fields_to_show(self, fields_to_show):
        self.__fields_to_show = fields_to_show

    def is_suit_filter(self, vacancy: Vacancy, filter: str) -> bool:
        index = filter.index(":")
        field = filter[:index]
        value = lambda: filter[index + 2:].split(", ") if field == "Навыки" else filter[index + 2:]
        if (field == "Оклад"):
            return float(vacancy.salary.salary_from) <= float(value()) <= float(vacancy.salary.salary_to)
        elif (field == "Навыки"):
            return all(skill in vacancy.key_skills for skill in value())
        elif (field == "Дата публикации вакансии"):
            return value() == datetime.date(int(vacancy.published_at[0:4]),
                                            int(vacancy.published_at[5:7]),
                                            int(vacancy.published_at[8:10])).strftime("%d.%m.%Y")
        elif (field == "Опыт работы"):
            return value() == work_experience_dict[vacancy.experience_id]
        elif (field == "Премиум-вакансия"):
            return value() == translate_dict[vacancy.premium]
        elif (field == "Идентификатор валюты оклада"):
            return value() == currency_dict[vacancy.salary.salary_currency]
        elif (field == "Оклад указан до вычета налогов"):
            return value() == vacancy.salary.salary_gross
        else:
            name = vacancy.__getattribute__(reversed_dict[field])
            return value() == name

    def process_work_experience(self, experience: str) -> str:
        if (experience == "Более 6 лет"):
            return "Я"
        return experience

    def sort_data(self, data: list, sort_param: str, is_reverse_sort: bool) -> list:
        if (sort_param == "Навыки"):
            sorted_data = sorted(data, key=lambda d: len(d.key_skills), reverse=is_reverse_sort)
        elif (sort_param == "Оклад"):
            sorted_data = sorted(data, key=lambda d:
            (float(d.salary.salary_from) + float(d.salary.salary_to)) / 2 * currency_to_rub_dict[d.salary.salary_currency],
                                 reverse=is_reverse_sort)
        elif (sort_param == "Дата публикации вакансии"):
            sorted_data = sorted(data, key=lambda d: int(
                d.published_at[0:4] + d.published_at[5:7] + d.published_at[8:10]) * 86400 +
                                                     (int(d.published_at[11:13]) * 3600 + int(
                                                         d.published_at[14:16]) * 60 +
                                                      int(d.published_at[17:19])), reverse=is_reverse_sort)
        elif (sort_param == "Опыт работы"):
            sorted_data = sorted(data, key=lambda d: self.process_work_experience(work_experience_dict[d.experience_id]),
                                 reverse=is_reverse_sort)
        else:
            sorted_data = sorted(data, key=lambda d: d.__getattribute__(reversed_dict[sort_param]), reverse=is_reverse_sort)
        return sorted_data

    def process_data(self, data: list, filter: str, sort_param: str, is_reverse_sort: bool):
        vacancies = []
        for vacancy in data:
            if (filter != ""):
                if (self.is_suit_filter(vacancy, filter)):
                    vacancies.append(vacancy)
            else:
                vacancies.append(vacancy)
        if (sort_param != ""):
            vacancies = self.sort_data(vacancies, sort_param, is_reverse_sort)
        self.data = vacancies

    def create_list(self, vacancy: dict) -> list:
        res = []
        for key in vacancy.keys():
            res.append(vacancy[key])
        return res

    def process_fields(self, vacancy: Vacancy) -> Vacancy:
        if (len(vacancy.description) > 100):
            vacancy.description = vacancy.description[:100] + "..."
        vacancy.key_skills = "\n".join(vacancy.key_skills)
        if (len(vacancy.key_skills) > 100):
            vacancy.key_skills = vacancy.key_skills[:100] + "..."
        full_date = vacancy.published_at
        date = datetime.date(int(full_date[0:4]), int(full_date[5:7]), int(full_date[8:10]))
        vacancy.published_at = date.strftime("%d.%m.%Y")
        return vacancy

    def create_table(self, header: list) -> PrettyTable:
        my_table = PrettyTable()
        my_table.field_names = header
        for vacancy in self.data:
            vacancy.premium = translate_dict[vacancy.premium]
            vacancy.experience_id = work_experience_dict[vacancy.experience_id]
            vacancy.salary = vacancy.salary.get_salary()
            my_table.add_row(self.process_fields(vacancy).__dict__.values())
        my_table.max_width = 20
        my_table.align = "l"
        my_table.add_autoindex("№")
        my_table.hrules = 1
        return my_table

    def print_table(self):
        self.process_data(self.data, self.filter, self.sort_param, self.is_reverse_sort)
        if (len(self.data) == 0):
            print("Ничего не найдено")
        else:
            header = self.create_list(dic_naming)
            table = self.create_table(header)
            start = lambda: self.rows_range[0] - 1 if len(self.rows_range) > 0 else 0
            end = lambda: self.rows_range[1] - 1 if len(self.rows_range) > 1 else len(self.data)
            fields = lambda: self.fields_to_show if self.fields_to_show[0] != '' else header
            print(table.get_string(start=start(), end=end(), fields=["№"] + fields()))

dic_naming = {
        "name": "Название",
        "description": "Описание",
        "key_skills": "Навыки",
        "experience_id": "Опыт работы",
        "premium": "Премиум-вакансия",
        "employer_name": "Компания",
        "salary": "Оклад",
        "area_name": "Название региона",
        "published_at": "Дата публикации вакансии"
}

translate_dict = {
    "True": "Да",
    "False": "Нет",
    "TRUE": "ДА",
    "FALSE": "НЕТ"
}

work_experience_dict = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"
}

currency_dict = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

fields_dict = {"name": "Название",
        "description": "Описание",
        "key_skills": "Навыки",
        "experience_id": "Опыт работы",
        "premium": "Премиум-вакансия",
        "employer_name": "Компания",
        "salary": "Оклад",
        "area_name": "Название региона",
        "published_at": "Дата публикации вакансии",
        "salary_currency": "Идентификатор валюты оклада",
        "salary_gross": "Оклад указан до вычета налогов"
}

reversed_dict = dict(zip(fields_dict.values(), fields_dict.keys()))

currency_to_rub_dict = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

def create_table_statistics():
    print("Введите название файла: ", end="")
    file_name = input()
    print("Введите параметр фильтрации: ", end="")
    filter = input()
    print("Введите параметр сортировки: ", end="")
    sort_param = input()
    print("Обратный порядок сортировки (Да / Нет): ", end="")
    is_reverse_sort = input()
    print("Введите диапазон вывода: ", end="")
    rows_range = [int(inp) for inp in input().split()]
    print("Введите требуемые столбцы: ", end="")
    fields_to_show = [str(inp) for inp in input().split(", ")]

    if (is_correct_input(filter, sort_param, is_reverse_sort)):
        data = DataSet(file_name).vacancies_objects
        if (data == []):
            print("Нет данных")
        else:
            InputConect(data, filter, sort_param, bool_parse(is_reverse_sort), rows_range, fields_to_show).print_table()

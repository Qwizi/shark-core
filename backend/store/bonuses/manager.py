from django.conf import settings
import importlib


class BonusTypeManager(object):
    __bonus_list = []

    def __init__(self):
        self.__bonus_list = self.get_bonus_list_from_settings()

    @staticmethod
    def get_bonus_list_from_settings():
        return settings.SHARK_CORE['STORE_BONUS_TYPE_LIST']

    def get_bonus_list(self):
        return self.__bonus_list

    def get_bonus_classes(self):
        bonus_instance_list = []

        for m in self.__bonus_list:
            """
            Zamiana stringa na liste.
            ['nazwa_aplikacji','bonuses', 'NazwaBonusu']
            Przykład:
            ['premium_account', 'bonuses', 'PremiumAccountBonus']
            """
            module_split = m.split('.')

            """
            Usuwamy ostatnia pozycje z tablicy. (Klase bonusu)
            Tablica wyglada teraz tak
            ['premium_account', 'bonuses']
            """
            module_split.pop(-1)

            """
            Przekszalcamy tablice w stringa
            Wyglada teraz tak
            'premium_account.bonuses'
            """
            module_join = '.'.join(module_split)

            """
            Importujemy modul
            """
            module = importlib.import_module(module_join)

            """
            Ponownie zamieniamy liste na stringa z ustawien i pobieramy nazwe klasy bonusu
            Wyglada teraz tak
            PremiumAcccountBonus
            """
            class_name = m.split('.')[-1]

            """
            Pobieramy klase
            """
            bonus_class = getattr(module, class_name)

            """
            Dodajemy klase do listy
            """
            bonus_instance_list.append(bonus_class)
        return bonus_instance_list

    def get_bonus(self, bonus_tag):
        """
        Pobieramy bonus za pomocą unikalnego tagu
        """

        bonus_class = None

        for bonus in self.get_bonus_classes():
            if bonus.tag == bonus_tag:
                bonus_class = bonus
        
        """
        Jeżeli nie znaleziono klasy bonusu zwracamy wyjatek
        """
        if bonus_class is None:
            raise Exception('404 - Bonus not found :(')

        return bonus_class


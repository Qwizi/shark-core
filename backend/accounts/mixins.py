from .models import Account


class AccountThreadsPostCounterMixin:
    """
    Klasa pomocznica do licznika tematow/postow
    """

    @staticmethod
    def get_account_threads_counter(account: Account) -> int:
        """
        Metoda zwracajaca licznik tematow dla danego usera
        """
        return account.thread_author_set.all().count()

    @staticmethod
    def get_account_posts_counter(account: Account) -> int:
        """
        Metoda zwracajaca licznik postow dla danego usera
        """
        return account.post_author_set.all().count()

    def format_queryset(self, queryset, many=False):
        """
        Metoda zwracajaca nowa tablice uzytkownikow  z licznikiem tematow/postow
        """
        if many:
            # Tworzymy nowy pusty queryset
            new_queryset = []

            # Iterujemy po liscie uzytkownikow
            for account in queryset:
                account.threads = self.get_account_threads_counter(account)
                account.posts = self.get_account_posts_counter(account)
                account.formatted_username = account.get_formatted_name()
                # Dodajemy zaaktualiwanego uzytkownika do nowej listy
                new_queryset.append(account)

            return new_queryset
        else:
            queryset.threads = self.get_account_threads_counter(queryset)
            queryset.posts = self.get_account_posts_counter(queryset)
            queryset.formatted_username = queryset.get_formatted_name()
            return queryset

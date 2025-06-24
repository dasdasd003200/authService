from config.services import ServiceRegistry


class UserServices:
    @staticmethod
    def get_create_use_case():
        return ServiceRegistry.create("users.create_use_case")

    @staticmethod
    def get_get_use_case():
        return ServiceRegistry.create("users.get_use_case")

    @staticmethod
    def get_update_use_case():
        return ServiceRegistry.create("users.update_use_case")

    @staticmethod
    def get_delete_use_case():
        return ServiceRegistry.create("users.delete_use_case")

    @staticmethod
    def get_search_use_case():
        return ServiceRegistry.create("users.search_use_case")

    @staticmethod
    def get_deactivate_use_case():
        return ServiceRegistry.create("users.deactivate_use_case")


# Funciones directas para simplificar uso
def get_create_user_use_case():
    return UserServices.get_create_use_case()


def get_get_user_use_case():
    return UserServices.get_get_use_case()


def get_update_user_use_case():
    return UserServices.get_update_use_case()


def get_delete_user_use_case():
    return UserServices.get_delete_use_case()


def get_search_users_use_case():
    return UserServices.get_search_use_case()


def get_deactivate_user_use_case():
    return UserServices.get_deactivate_use_case()

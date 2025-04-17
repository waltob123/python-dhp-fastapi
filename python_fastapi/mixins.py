class PersistMixin:
    @staticmethod
    def save(object_to_save: dict, list_of_objects: list[dict]) -> dict:
        """
        Save the object to the list of objects

        :param object_to_save: The object to save
        :param list_of_objects: The list of objects to save to
        :return: dict
        """
        list_of_objects.append(object_to_save)
        return object_to_save

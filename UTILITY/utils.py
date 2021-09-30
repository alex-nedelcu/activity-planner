class Utility:
    @staticmethod
    def convert_ids_string_to_separate_integers(string_of_ids):
        """ e.g. receives the string "438 218 492" and returns the list of integers [438, 218, 492] """
        ids_as_integers = []
        for id_iterator in string_of_ids.split():
            ids_as_integers.append(int(id_iterator))
        return ids_as_integers

    @staticmethod
    def convert_calendar_date_string_to_dictionary(string_calendar_date):
        """ e.g. receives the string "30 11 2019" and returns the dictionary {"year": 2019, "month": 11, "day": 30} """
        calendar_date_parts = string_calendar_date.split()
        day = int(calendar_date_parts[0])
        month = int(calendar_date_parts[1])
        year = int(calendar_date_parts[2])
        return {
            "year": year,
            "month": month,
            "day": day
        }

    @staticmethod
    def convert_list_of_integers_into_string(list_of_integers):
        """ e.g. receives the list of integers [109, 394] and returns the string "109 394" """
        expected_string = ""
        for integer in list_of_integers:
            expected_string += str(integer) + " "
        expected_string = expected_string[:-1]
        return expected_string

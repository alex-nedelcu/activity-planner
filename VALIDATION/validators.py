from EXCEPTIONS.custom_exceptions import PersonValidatorError, ActivityValidatorError, DateValidatorError


class Validator:
    """ Class used to instantiate objects that validate persons and activities """

    def validate_person(self, person):
        """
        Validates the attributes of an object of type Person.
        Raises PersonValidatorError in case one of the object's attributes is invalid.
        To the list of errors, there are inserted the following warning messages for the user:
            "Invalid person ID! Cannot be negative!" in case the person's ID is negative;
            "Invalid person name! Cannot be empty!" in case the person's name is an empty string;
            "Invalid phone number! Cannot be empty!" in case the person's phone number does not contain any digits.
        :param person: the person that is evaluated by the validator
        """
        list_of_errors = ""

        if person.id < 0:
            list_of_errors += "Invalid person ID! Cannot be negative!\n"
        if person.name == "":
            list_of_errors += "Invalid person name! Cannot be empty!\n"
        if person.phone_number == "":
            list_of_errors += "Invalid phone number! Cannot be empty!\n"

        if len(list_of_errors) != 0:
            raise PersonValidatorError(list_of_errors)

    def validate_activity(self, activity):
        """
        Validates the attributes of an object of type Activity.
        Raises ActivityValidatorError in case one of the object's attributes is invalid.
        To the list of errors, there are inserted the following warning messages for the user:
            "Invalid activity ID! Cannot be negative!" in case the activity's ID is negative;
            "An activity must be performed together with at least one person!" in case the activity is performed with no one;
            "Year cannot be negative!" in case the year of the activity is negative
            "Month must be an integer in [1, 12]!" in case the month of the activity is less than 1 or greater than 12
            "Day must be an integer in [1, 31]!" in case the day of the activity is less than 1 or greater than 31
            "Time must be an integer in [0, 23]" in case the time of the activity is less than 0 or greater than 23
                * for simplicity, I assume that the activities can only start at a fixed time during a day (e.g. 10:00)
            "The description of the activity cannot be empty!" in case the activity's description is an empty string
        :param activity: the activity that is evaluated by the validator
        """
        list_of_errors = ""

        if activity.id < 0:
            list_of_errors += "Invalid activity ID! Cannot be negative!\n"
        if not activity.participants_ids:
            list_of_errors += "An activity must be performed together with at least one person!\n"
        if activity.year < 0:
            list_of_errors += "Year cannot be negative!\n"
        if not (1 <= activity.month <= 12):
            list_of_errors += "Month must be an integer in [1, 12]!\n"
        if not (1 <= activity.day <= 31):
            list_of_errors += "Day must be an integer in [1, 31]!\n"
        if not (0 <= activity.time <= 23):
            list_of_errors += "Time must be an integer in [0, 23]!\n"
        if activity.description == "":
            list_of_errors += "The description of the activity cannot be empty!\n"
        for id_iterator in activity.participants_ids:
            if isinstance(id_iterator, int) is False:
                list_of_errors += "The list must contain the participants' IDs (integers)!\n"

        if list_of_errors != "":
            raise ActivityValidatorError(list_of_errors)

    def validate_calendar_date(self, calendar_date):
        """
        Validates a calendar date.
        Raises DateValidatorError in case the year, the month or the day of the calendar date are invalid.
        To the list of errors, there are inserted the following warning messages for the user:
            "Year cannot be negative!" in case the year is negative
            "Month must be an integer in [1, 12]! in case the month is not an integer in the closed interval [1, 12]
            "Day must be an integer in [1, 31]! in case the day is not an integer in the closed interval [1, 31]
        :param calendar_date: the calendar date that needs to be validated
        """
        list_of_errors = ""

        if calendar_date["year"] < 0:
            list_of_errors += "Year cannot be negative!\n"
        if not (1 <= calendar_date["month"] <= 12):
            list_of_errors += "Month must be an integer in [1, 12]!\n"
        if not (1 <= calendar_date["day"] <= 31):
            list_of_errors += "Day must be an integer in [1, 31]!\n"

        if list_of_errors != "":
            raise DateValidatorError(list_of_errors)

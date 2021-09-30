from EXCEPTIONS.custom_exceptions import PersonValidatorError, ActivityValidatorError


class Operation:
    """
    Class used to instantiate operations, each operation having a direct action and the argument necessary to perform it,
    and and inverse action with the necessary argument.
    """

    def __init__(self, direct_action, direct_action_argument, inverse_action, inverse_action_argument):
        """
        The constructor of an operation.
        :param direct_action: string, the name of the direct action performed by the user (e.g. add person)
        :param direct_action_argument: the object needed to perform the direct action (e.g. new_person, new_activity)
        :param inverse_action: string, the name of the inverse action (relative to the direct action performed by
        the user)
        :param inverse_action_argument: the object needed to perform the inverse action
        e.g. direct_action = "add activity"
             direct_action_argument = new_activity (object of type Activity)
             inverse_action = "remove activity"
             inverse_action_argument = new_activity.id
        """
        self.__direct_action = direct_action
        self.__direct_action_argument = direct_action_argument
        self.__inverse_action = inverse_action
        self.__inverse_action_argument = inverse_action_argument

    @property
    def direct_action(self):
        """
        Property used to access the name of the direct action.
        :return: the name of the direct action
        """
        return self.__direct_action

    @property
    def direct_action_argument(self):
        """
        Property used to access the argument of the direct action.
        :return: the object needed to perform the direct action
        """
        return self.__direct_action_argument

    @property
    def inverse_action(self):
        """
        Property used to access the name of the inverse action.
        :return: the name of the inverse action
        """
        return self.__inverse_action

    @property
    def inverse_action_argument(self):
        """
        Property used to access the argument of the direct action.
        :return: the object needed to perform the inverse action
        """
        return self.__inverse_action_argument


class Activity:
    """ Class used to instantiate activities """

    def __init__(self, activity_id, participants_ids, date, time, description):
        """
        The constructor for each new object of type Activity.
        :param activity_id: positive integer; the activity's ID
        :param participants_ids: list of positive integers; cannot be empty; the persons that participate in the activity
        :param date: dictionary; contains the calendar date of the activity
        :param time: positive integer; must be included in [0, 23]; the time when the activity takes places
        :param description: string; cannot be empty; the description of the activity;
        """
        self.__activity_id = activity_id
        self.__participants_ids = participants_ids
        self.__date = date
        self.__time = time
        self.__description = description

    @property
    def id(self):
        """ Getter for the activity's ID """
        return self.__activity_id

    @property
    def participants_ids(self):
        """ Getter for the list of IDs of the persons that participate in the activity """
        return self.__participants_ids

    @participants_ids.setter
    def participants_ids(self, new_participants_ids):
        """
        Setter for the list of IDs of the persons that participate in the activity.
        Raises ActivityValidatorError if the supposed list is actually not a list.
        :param new_participants_ids: the list of IDs
        """
        if isinstance(new_participants_ids, list) is False:
            raise ActivityValidatorError("The new participants' IDs must be in a list!\n")
        self.__participants_ids = new_participants_ids

    @property
    def year(self):
        """ Getter for the year of the activity """
        return self.__date["year"]

    @year.setter
    def year(self, new_year_value):
        """
        Setter for the year of the activity.
        Raises ActivityValidatorError if the new value of the year is negative.
        :param new_year_value: the new value of the activity's year
        """
        if new_year_value < 0:
            raise ActivityValidatorError("Year cannot be negative! (or could it!? xD)\n")
        self.__date["year"] = new_year_value

    @property
    def month(self):
        """ Getter for the month of the activity """
        return self.__date["month"]

    @month.setter
    def month(self, new_month_value):
        """
        Setter for the month of the activity.
        Raises ActivityValidatorError if the new value of the month is not included in [1, 12]
        :param new_month_value: the new value of the activity's month
        """
        if not (1 <= new_month_value <= 12):
            raise ActivityValidatorError("Month must be an integer in [1, 12]!\n")
        self.__date["month"] = new_month_value

    @property
    def day(self):
        """ Getter for the day of the activity """
        return self.__date["day"]

    @day.setter
    def day(self, new_day_value):
        """
        Setter for the day of the activity.
        Raises ActivityValidatorError if the new value of the day is not included in [1, 31]
        :param new_day_value: the new value of the activity's day
        """
        if not (1 <= new_day_value <= 31):
            raise ActivityValidatorError("Day must be an integer in [1, 31]!\n")
        self.__date["day"] = new_day_value

    @property
    def date(self):
        """ Getter for the date of the activity """
        return self.__date

    @date.setter
    def date(self, new_date):
        """
        Setter for the date of the activity.
        Raises ActivityValidatorError if the new date is not a dictionary.
        :param new_date: the new value of the activity's date
        """
        if isinstance(new_date, dict) is False:
            raise ActivityValidatorError("The date format is incorrect!")
        self.__date = new_date

    @property
    def time(self):
        """ Getter for the time of the activity """
        return self.__time

    @time.setter
    def time(self, new_time_value):
        """
        Setter for the time of the activity.
        Raises ActivityValidatorError if the new value of the time is not included in [0, 23]
        :param new_time_value: the new value of the activity's time
        """
        if not (0 <= new_time_value <= 23):
            raise ActivityValidatorError("Time must be an integer in [0, 23]!\n")
        self.__time = new_time_value

    @property
    def description(self):
        """ Getter for the description of the activity """
        return self.__description

    @description.setter
    def description(self, new_description):
        """
        Setter for the description of the activity.
        Raises ActivityValidatorError if the new description is empty.
        :param new_description: the new description of the activity
        """
        if new_description == "":
            raise ActivityValidatorError("The description cannot be empty!\n")
        self.__description = new_description

    def __str__(self):
        """ The overwritten str() method """
        return "ID {}  ⏦  performed together with the persons having the IDs: {}\n" \
               "Description: {}\n" \
               "In {}.{}.{}, at {}:00".format(self.__activity_id, self.__participants_ids, self.__description,
                                              self.day, self.month, self.year, self.__time)

    def __eq__(self, other_activity):
        """
        The overwritten eq() method. Two activities are considered equal if their IDs are the same
        :param other_activity: the activity of comparison
        :return: True if the activities are equal, False otherwise
        """
        return self.id == other_activity.id


class Person:
    """ Class used to instantiate persons """

    def __init__(self, person_id, name, phone_number):
        """
        The constructor for each new object of type Person.
        :param person_id: positive integer; the person's ID
        :param name: string; cannot be empty; the name of the person
        :param phone_number: string; cannot be empty; the phone number of the person
        """
        self.__person_id = person_id
        self.__name = name
        self.__phone_number = phone_number

    @property
    def name(self):
        """ Getter for the name of the person """
        return self.__name

    @name.setter
    def name(self, new_name):
        """
        Setter for the name of the person.
        Raises PersonValidatorError if the new name of the person is empty.
        :param new_name: string, the new name of the person
        """
        if new_name == "":
            raise PersonValidatorError("The name of a person cannot be empty!")
        self.__name = new_name

    @property
    def phone_number(self):
        """ Getter for the person's phone number """
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, new_phone_number):
        """
        Setter for the person's phone number.
        Raises PersonValidatorError if the new phone number is empty.
        :param new_phone_number: string, the new phone number of the person
        """
        if new_phone_number == "":
            raise PersonValidatorError("The phone number of a person cannot be empty!")
        self.__phone_number = new_phone_number

    @property
    def id(self):
        """ Getter for the ID of the person """
        return self.__person_id

    def __str__(self):
        """ The overwritten str() method """
        return "ID {}  ⏦  name: {}  ⏦  phone number: {}".format(self.__person_id,
                                                                self.__name.title(),
                                                                self.__phone_number)

    def __eq__(self, other_person):
        """
        The overwritten eq() method. Two persons are considered equal if their IDs are the same.
        :param other_person: person of comparison
        :return: True if the two persons are equal, False otherwise
        """
        return self.__person_id == other_person.__person_id

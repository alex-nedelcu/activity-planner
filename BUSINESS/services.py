import copy
from datetime import date

from DOMAIN.entities import Person, Activity, Operation
from EXCEPTIONS.custom_exceptions import PersonServiceError, ActivityServiceError, ActivityValidatorError


class UndoService:
    """ Instantiates undo services, which are objects responsible to coordinate the undo operation """

    def __init__(self, person_repository, activity_repository, undo_stack, redo_stack):
        """
        The constructor of the undo service, that has access to the person and activity repositories and to both stacks.
        :param person_repository: the collection of uniquely identifiable persons
        :param activity_repository: the collection of uniquely identifiable activities
        :param undo_stack: the stack containing all the operations that are "undoable"
        :param redo_stack: the stack containing all the operations that are "redoable"
        """
        self.__person_repository = person_repository
        self.__activity_repository = activity_repository
        self.__undo_stack = undo_stack
        self.__redo_stack = redo_stack

    def undo(self):
        """
        Finds the operation on top of the undo stack, identifies its direct action in order to be able to perform
        its reverse by calling a corresponding method, and pushes the operation to the redo stack.
        """
        operation = self.__undo_stack.pop()
        self.__redo_stack.push(operation)

        if operation.direct_action == "add person":
            self.__undo_add_person(operation)
        elif operation.direct_action == "remove person":
            self.__undo_remove_person(operation)
        elif operation.direct_action == "update person":
            self.__undo_update_person(operation)
        elif operation.direct_action == "add activity":
            self.__undo_add_activity(operation)
        elif operation.direct_action == "remove activity":
            self.__undo_remove_activity(operation)
        elif operation.direct_action == "update activity":
            self.__undo_update_activity(operation)

    def __undo_add_person(self, operation):
        """
        Performs the undo for the add person, that is, removes the person that was added.
        :param operation: the operation to be undone
        """
        remove_person_id = operation.inverse_action_argument
        self.__person_repository.remove_person(remove_person_id)

    def __undo_remove_person(self, operation):
        """
        Performs the undo for the remove person, that is, adds back the person that was removed.
        :param operation: the operation to be undone
        """
        previously_removed_person = operation.inverse_action_argument
        self.__person_repository.save_person(previously_removed_person)

    def __undo_update_person(self, operation):
        """
        Performs the undo for the update person, that is, changes the updated person with the old version of the person.
        :param operation: the operation to be undone
        """
        old_version_person = operation.inverse_action_argument
        person_id = old_version_person.id
        self.__person_repository.update_person(person_id, old_version_person)

    def __undo_add_activity(self, operation):
        """
        Performs the undo for the add activity, that is, removes the activity that was added.
        :param operation: the operation to be undone
        """
        remove_activity_id = operation.inverse_action_argument
        self.__activity_repository.remove_activity(remove_activity_id)

    def __undo_remove_activity(self, operation):
        """
        Performs the undo for the remove activity, that is, adds back the activity that was removed.
        :param operation: the operation to be undone
        """
        previously_removed_activity = operation.inverse_action_argument
        self.__activity_repository.save_activity(previously_removed_activity)

    def __undo_update_activity(self, operation):
        """
        Performs the undo for the update activity, that is, changes the updated activity with the old version of the activity.
        :param operation: the operation to be undone
        """
        old_version_activity = operation.inverse_action_argument
        activity_id = old_version_activity.id
        self.__activity_repository.update_activity(activity_id, old_version_activity)


class RedoService:
    """ Instantiates redo services, which are objects responsible to coordinate the redo operation """

    def __init__(self, person_repository, activity_repository, undo_stack, redo_stack):
        """
        The constructor of the redo service, that has access to the person and activity repositories and to both stacks.
        :param person_repository: the collection of uniquely identifiable persons
        :param activity_repository: the collection of uniquely identifiable activities
        :param undo_stack: the stack containing all the operations that are "undoable"
        :param redo_stack: the stack containing all the operations that are "redoable"
        """
        self.__person_repository = person_repository
        self.__activity_repository = activity_repository
        self.__undo_stack = undo_stack
        self.__redo_stack = redo_stack

    def redo(self):
        """
        Finds the operation on top of the redo stack, identifies its direct action and performs it by calling
        a corresponding method, and pushes the operation to the undo stack.
        """
        operation = self.__redo_stack.pop()
        self.__undo_stack.push(operation)

        if operation.direct_action == "add person":
            self.__redo_add_person(operation)
        elif operation.direct_action == "remove person":
            self.__redo_remove_person(operation)
        elif operation.direct_action == "update person":
            self.__redo_update_person(operation)
        elif operation.direct_action == "add activity":
            self.__redo_add_activity(operation)
        elif operation.direct_action == "remove activity":
            self.__redo_remove_activity(operation)
        elif operation.direct_action == "update activity":
            self.__redo_update_activity(operation)

    def __redo_add_person(self, operation):
        """
        Performs the redo action for the add person.
        :param operation: the operation to be redone
        """
        person_to_add = operation.direct_action_argument
        self.__person_repository.save_person(person_to_add)

    def __redo_remove_person(self, operation):
        """
        Performs the redo action for the remove person.
        :param operation: the operation to be redone
        """
        remove_person_id = operation.direct_action_argument
        self.__person_repository.remove_person(remove_person_id)

    def __redo_update_person(self, operation):
        """
        Performs the redo action for the update person.
        :param operation: the operation to be redone
        """
        updated_person = operation.direct_action_argument
        person_id = updated_person.id
        self.__person_repository.update_person(person_id, updated_person)

    def __redo_add_activity(self, operation):
        """
        Performs the redo action for the add activity.
        :param operation: the operation to be redone
        """
        activity_to_add = operation.direct_action_argument
        self.__activity_repository.save_activity(activity_to_add)

    def __redo_remove_activity(self, operation):
        """
        Performs the redo action for the remove activity.
        :param operation: the operation to be redone
        """
        remove_activity_id = operation.direct_action_argument
        self.__activity_repository.remove_activity(remove_activity_id)

    def __redo_update_activity(self, operation):
        """
        Performs the redo action for the update activity.
        :param operation: the operation to be redone
        """
        updated_activity = operation.direct_action_argument
        activity_id = updated_activity.id
        self.__activity_repository.update_activity(activity_id, updated_activity)


class StatisticsService:
    """
    Class used to instantiate statistics services, i.e. the objects that are responsible to create some statistics.
    """

    def __init__(self, activity_repository):
        """
        The constructor for a new object of type StatisticsService.
        A statistics service must have permission to access the activities,
        that is why there is a dependency relationship between the statistics service and the activity repository.
        :param activity_repository: the collection of uniquely identifiable activities
        """
        self.__activity_repository = activity_repository

    @staticmethod
    def check_upcoming_activity(activity):
        """
        Checks whether a given activity is upcoming or it passed.
        :param activity: the activity to be checked
        :return: True if the activity is upcoming, False otherwise
        """
        current_date = date.today()
        current_day = current_date.day
        current_month = current_date.month
        current_year = current_date.year

        return activity.year > current_year or (activity.year == current_year and activity.month > current_month) or (
                activity.year == current_year and activity.month == current_month and activity.day >= current_day)

    def find_busiest_days(self):
        """
        Creates a dictionary whose keys are some tuples, representing a calendar date, and whose values are the
        corresponding number of activities for each day.
        Note that:
            upcoming_dates_dictionary will have the following form: e.g. {(10, 12, 2020): 5, (25, 8, 2019): 3}
            The key (dd, mm, yyyy) is the calendar date and the value is the number of activities in that day
            upcoming_date[1] = the number of activities taking place in that date
            upcoming_date[0][2] = the year of the activities
            upcoming_date[0][1] = the month of the activities
            upcoming_date[0][0] = the day of the activities
        :return: the dictionary sorted in ascending order by the number of activities in each day
        """
        activities_list = self.__activity_repository.get_all_activities_list()
        upcoming_activities = [activity for activity in activities_list if self.check_upcoming_activity(activity)]

        upcoming_dates_dictionary = {}
        for activity in upcoming_activities:
            upcoming_dates_dictionary[(activity.day, activity.month, activity.year)] = 0
        for activity in upcoming_activities:
            upcoming_dates_dictionary[(activity.day, activity.month, activity.year)] += 1

        upcoming_dates = sorted(upcoming_dates_dictionary.items(), key=lambda upcoming_date: (upcoming_date[1],
                                                                                              upcoming_date[0][2],
                                                                                              upcoming_date[0][1],
                                                                                              upcoming_date[0][0]
                                                                                              ))
        return dict(upcoming_dates)


class ActivityService:
    """
    Class used to instantiate activity services, i.e. objects that connect the console to the repository of
    activities and also of persons.
    A service receives data from the console (user), creates and validates objects, then calls the corresponding
    repository methods in order to finalize the operation.
    Each service must be injected at its instantiation with one (or more) repositories and also with a validator.
    """

    def __init__(self, activity_validator, activity_repository, person_repository, undo_stack, redo_stack):
        """
        The constructor for a new object of type ActivityService.
        :param activity_validator: object used to validate newly created activities
        :param activity_repository: the collection of uniquely identifiable activities, which performs CRUD operations
        :param person_repository: the collection of uniquely identifiable persons, needed because an activity is also
        defined using the persons' IDs, so they must be accessible from the activity service
        """
        self.__activity_validator = activity_validator
        self.__activity_repository = activity_repository
        self.__person_repository = person_repository
        self.__undo_stack = undo_stack
        self.__redo_stack = redo_stack

    def service_add_activity(self, activity_id, participants_ids, activity_date, time, description):
        """
        Receives the components for a new activity, creates and validates it and then calls the corresponding
        repository method which adds the newly created activity to the repository.
        Raises ActivityServiceError if the newly created activity is performed with someone's whose ID is not in the
        agenda.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param activity_id: positive integer; the ID of the activity
        :param participants_ids: list of integers; the list containing the IDs of the persons that take part
        in the activity
        :param activity_date: dictionary; the calendar date of the activity
        :param time: positive integer in [0, 23]; the time of the activity
        :param description: string; the description of the activity
        """
        new_activity = Activity(activity_id, participants_ids, activity_date, time, description)
        self.__activity_validator.validate_activity(new_activity)

        # now check whether the persons that participate in the new activity exist in the agenda
        existing_persons_list = self.__person_repository.get_all_persons_list()
        existing_persons_ids = [person.id for person in existing_persons_list]
        for id_checker in participants_ids:
            if id_checker not in existing_persons_ids:
                raise ActivityServiceError(
                    "You are trying to perform an activity together with someone that is not in the agenda!\n")

        self.__activity_repository.save_activity(new_activity)
        direct_action = "add activity"
        direct_action_argument = new_activity
        inverse_action = "remove activity"
        inverse_action_argument = new_activity.id
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def service_get_list_of_activities(self):
        """
        Gets the complete list of activities by calling the corresponding repository method.
        :return: the list of activities, sorted by date and time
        """
        activities_list = self.__activity_repository.get_all_activities_list()
        return activities_list
        # return sorted(activities_list, key=lambda activity: (activity.year, activity.month, activity.day, activity.time))

    def service_remove_activity(self, remove_activity_id):
        """
        Receives an ID and removes the activity having that ID from the repository.
        Raises ActivityValidatorError if the receives ID is negative.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param remove_activity_id: the ID of the activity to be removed
        """
        if remove_activity_id < 0:
            raise ActivityValidatorError("Activity ID cannot be negative!\n")
        activity_to_be_removed = self.__activity_repository.find_activity(remove_activity_id)
        self.__activity_repository.remove_activity(remove_activity_id)

        direct_action = "remove activity"
        direct_action_argument = remove_activity_id
        inverse_action = "add activity"
        inverse_action_argument = activity_to_be_removed
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def service_update_activity(self, activity_id, participants_ids, activity_date, time, description):
        """
        Receives the ID of the activity to be updates and also its updated components, creates a new activity using
        them, validates it and then calls the corresponding repository method that replaces the old activity with
        the updated one.
        Raises ActivityServiceError if the updated list of participants includes someone who is not in the agenda.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param activity_id: integer, must be positive in order to be valid
        :param participants_ids: list of integers, must be non-empty in order to be valid, the updated
        list of participants
        :param activity_date: dictionary, the updated calendar date of the activity
        :param time: integer, must be in [0, 23], the updated time of the activity
        :param description: string, must be non-empty, the updated description of the activity
        """
        updated_activity = Activity(activity_id, participants_ids, activity_date, time, description)
        self.__activity_validator.validate_activity(updated_activity)

        # now check whether the persons that participate in the new activity exist in the agenda
        existing_persons_list = self.__person_repository.get_all_persons_list()
        existing_persons_ids = [person.id for person in existing_persons_list]
        for id_checker in participants_ids:
            if id_checker not in existing_persons_ids:
                raise ActivityServiceError(
                    "You are trying to perform an activity together with someone that is not in the agenda!\n")

        activity_old_version = copy.deepcopy(self.__activity_repository.find_activity(activity_id))
        self.__activity_repository.update_activity(activity_id, updated_activity)
        direct_action = "update activity"
        direct_action_argument = updated_activity
        inverse_action = "update activity"
        inverse_action_argument = activity_old_version
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def find_activities_by_date(self, year, month, day):
        """
        Receives a calendar date and finds all the activities that take place in that day.
        :param year: the year of the activity
        :param month: the month of the activity
        :param day: the day of the activity
        :return: a list containing the activities that take place in the given day
        """
        given_date = {"year": year, "month": month, "day": day}
        self.__activity_validator.validate_calendar_date(given_date)
        activities_list = self.__activity_repository.get_all_activities_list()
        searched_activities = [activity for activity in activities_list if activity.date == given_date]
        return sorted(searched_activities, key=lambda activity: activity.time)

    def find_activities_by_description(self, searched_description):
        """
        Receives a description and finds all the activities whose descriptions contain or are the same with the received
        description (works case insensitive).
        :param searched_description: the searched description
        :return: a list containing the activities whose descriptions contain the received description
        """
        activities_list = self.__activity_repository.get_all_activities_list()
        searched_activities = [activity for activity in activities_list if
                               searched_description in activity.description.lower()]
        return sorted(searched_activities, key=lambda activity: (activity.year,
                                                                 activity.month,
                                                                 activity.day,
                                                                 activity.time))

    def find_activities_by_participant(self, searched_participant_id):
        """
        Receives a person ID and finds all the activities that are performed together with the person having that ID.
        Raises ActivityServiceError if the received person ID is negative or if there is no person having the received ID.
        :param searched_participant_id: the received person ID
        :return: a list containing the activities that are performed together with the person having the received ID
        """
        if searched_participant_id < 0:
            raise ActivityServiceError("The ID of the searched person cannot be negative!\n")
        existing_persons_list = self.__person_repository.get_all_persons_list()
        existing_persons_ids = [person.id for person in existing_persons_list]
        if searched_participant_id not in existing_persons_ids:
            raise ActivityServiceError(f"There is no person having the ID {searched_participant_id} in the agenda!\n")
        activities_list = self.__activity_repository.get_all_activities_list()
        return [activity for activity in activities_list if searched_participant_id in activity.participants_ids]


class PersonService:
    """
    Class used to instantiate person services, i.e. objects that connect the console to the repository of
    persons.
    A service receives data from the console (user), creates and validates objects, then calls the corresponding
    repository methods in order to finalize the operation.
    Each service must be injected at its instantiation with one (or more) repositories and also with a validator.
    """

    def __init__(self, person_validator, person_repository, undo_stack, redo_stack):
        """
        The constructor for a new object of type PersonService.
        :param person_validator: object used to validate newly created persons
        :param person_repository: the collection of uniquely identifiable persons
        """
        self.__person_validator = person_validator
        self.__person_repository = person_repository
        self.__undo_stack = undo_stack
        self.__redo_stack = redo_stack

    def service_add_person(self, person_id, person_name, person_phone_number):
        """
        Receives the components of a new person, uses them to instantiate a new object of type Person, validates it
        and calls the corresponding repository method that adds the newly created person to the repository.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param person_id: integer, must be positive, the ID of the new person
        :param person_name: string, must be non-empty, the name of the new person
        :param person_phone_number: string, must be non-empty, the phone number of the new person
        """
        new_person = Person(person_id, person_name, person_phone_number)
        self.__person_validator.validate_person(new_person)
        self.__person_repository.save_person(new_person)

        direct_action = "add person"
        direct_action_argument = new_person
        inverse_action = "remove person"
        inverse_action_argument = new_person.id
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def service_remove_person(self, remove_person_id):
        """
        Receives an ID and removes from the repository the person having that ID.
        Raises PersonServiceError if the received ID is negative.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param remove_person_id: the ID of the person to be removed
        """
        if remove_person_id < 0:
            raise PersonServiceError("The introduced ID in invalid! Cannot be negative!\n")
        person_to_be_removed = self.__person_repository.find_person(remove_person_id)
        self.__person_repository.remove_person(remove_person_id)

        direct_action = "remove person"
        direct_action_argument = remove_person_id
        inverse_action = "add person"
        inverse_action_argument = person_to_be_removed
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def service_update_person(self, person_id, new_name, new_phone_number):
        """
        Receives an ID and updates the person having that ID by replacing its old attributes with new ones.
        Adds the operation on the undo stack.
        Clears the redo stack.
        :param person_id: integer, the ID of the person to be updated
        :param new_name: string, the updated name of the person
        :param new_phone_number: string, the updated phone number of the person
        """
        updated_person = Person(person_id, new_name, new_phone_number)
        self.__person_validator.validate_person(updated_person)
        person_old_version = copy.deepcopy(self.__person_repository.find_person(person_id))
        self.__person_repository.update_person(person_id, updated_person)

        direct_action = "update person"
        direct_action_argument = updated_person
        inverse_action = "update person"
        inverse_action_argument = person_old_version
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.__undo_stack.push(operation)
        self.__redo_stack.clear_stack()

    def service_get_persons_list(self):
        """
        Gets the complete list of persons by calling the corresponding repository method.
        :return: the list of persons, sorted alphabetically
        """
        return self.__person_repository.get_all_persons_list()

    def get_existing_persons_ids(self):
        """
        Creates a list containing the IDs of all the persons that exist in the list.
        :return: the list containing the persons' IDs
        """
        all_persons_list = self.__person_repository.get_all_persons_list()
        all_persons_ids = [person.id for person in all_persons_list]
        return all_persons_ids

    def find_persons_by_name(self, searched_name):
        """
        Receives a name and finds all the persons whose names contain the received name (works case insensitive).
        :param searched_name: the received name
        :return: a list containing objects of type Person, having the property that each person's name is the same
        with the received name or it contains the received name
        """
        persons_list = self.__person_repository.get_all_persons_list()
        return [person for person in persons_list if searched_name in person.name.lower()]

    def find_persons_by_phone_number(self, searched_phone_number):
        """
        Receives a phone number and finds all the persons whose phone numbers contain the received phone number.
        :param searched_phone_number: the received phone number
        :return: a list containing objects of type Person, having the property that each person's phone number is
        the same with the received phone number or it contains the received phone number
        """
        persons_list = self.__person_repository.get_all_persons_list()
        return [person for person in persons_list if searched_phone_number in person.phone_number]

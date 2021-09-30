from DOMAIN.entities import Person, Activity
from EXCEPTIONS.custom_exceptions import PersonRepositoryError, ActivityRepositoryError


class ActivityRepository:
    """
    Class used to instantiate an activities repository.
    The repository is a collection of uniquely identifiable objects, so there cannot exist two identical activities
        in the repository (i.e. two activities having the same ID).
    """

    def __init__(self):
        """
        The constructor for a new object of type ActivityRepository.
        The repository is represented as a list of activities, so it is initialized with an empty list.
        """
        self._activities_list = []

    @property
    def activities_list(self):
        """ Getter for the list of activities (i.e. all the activities that are in the repository) """
        return self._activities_list

    @activities_list.setter
    def activities_list(self, new_activities_list):
        """
        Setter for the list of activities.
        Raises ActivityRepositoryError if the supposed new list of activities is actually not a list, or if it does not
            contain activities.
        :param new_activities_list: the new list of activities
        """
        if isinstance(new_activities_list, list) is False:
            raise ActivityRepositoryError("The list of activities was assigned an invalid data type!\n")

        for activity_checker in new_activities_list:
            if isinstance(activity_checker, Activity) is False:
                raise ActivityRepositoryError("The list does not contain activities!\n")

        self._activities_list = new_activities_list

    def save_activity(self, new_activity):
        """
        Method that adds a new activity in the repository of activities.
        Raises ActivityRepositoryError if there already exists an activity having the same ID as the new activity or
            if there is another activity in the repository that takes place in the same time time as the new activity.
        :param new_activity: the new activity that is wanted to be introduced in the repository
        """
        if new_activity in self._activities_list:
            raise ActivityRepositoryError("An activity with this ID already exists in your agenda!\n")

        for activity in self._activities_list:
            if activity.date == new_activity.date and activity.time == new_activity.time:
                raise ActivityRepositoryError("Two different activities cannot be performed in the same time!\n")

        self._activities_list.append(new_activity)

    def find_activity(self, searched_activity_id):
        """
        Receives an ID and finds the activity from the repository having that ID.
        :param searched_activity_id: the ID of the searched activity
        :return: the activity having the received ID, or None if there is no activity having that ID
        """
        for activity in self._activities_list:
            if activity.id == searched_activity_id:
                return activity
        return None

    def check_activity_existence(self, searched_activity_id):
        """
        Checks whether there is(exists) any activity in the repository having a certain ID.
        :param searched_activity_id: the ID to check
        :return: True if there is an activity having the received ID, False otherwise
        """
        activities_ids_list = [activity.id for activity in self._activities_list]
        return searched_activity_id in activities_ids_list

    def remove_activity(self, remove_activity_id):
        """
        Removes an activity from the repository by its ID.
        Raises ActivityRepositoryError if there is no activity having the received ID.
        :param remove_activity_id: the ID of the activity that needs to be removed
        """
        if self.check_activity_existence(remove_activity_id) is False:
            raise ActivityRepositoryError("The activity you want to remove was not found in the list!\n")

        for remove_candidate in self._activities_list:
            if remove_candidate.id == remove_activity_id:
                self._activities_list.remove(remove_candidate)

    def update_activity(self, to_update_activity_id, updated_activity):
        """
        Receives an activity ID and an updated version of that activity, and replaces the attributes of the old activity
            with the updated attributes.
        Raises ActivityRepositoryError if there is no activity in the repository having the given ID or if the new
            activity takes place in the same time with another activity already existing in the repository.
        :param to_update_activity_id: the ID of the activity that needs to be updated
        :param updated_activity: the updated version of the searched activity
        """
        if self.check_activity_existence(to_update_activity_id) is False:
            raise ActivityRepositoryError("The activity you are trying to update was not found in the agenda!\n")

        for activity in self._activities_list:
            if activity.date == updated_activity.date and activity.time == updated_activity.time and activity.id != updated_activity.id:
                raise ActivityRepositoryError("There is already an activity taking place at that time!\n")
        for activity in self._activities_list:
            if activity.id == to_update_activity_id:
                activity.participants_ids = updated_activity.participants_ids
                activity.day = updated_activity.day
                activity.month = updated_activity.month
                activity.year = updated_activity.year
                activity.time = updated_activity.time
                activity.description = updated_activity.description

    def get_all_activities_list(self):
        """ Returns the complete list of activities """
        return self._activities_list

    def get_number_of_activities(self):
        """ Returns the number of activities in the repository """
        return len(self._activities_list)

    def __len__(self):
        """ Overwritten len() method. The length of the repository is actually the length of the list of activities """
        return len(self._activities_list)

    def clear_repository(self):
        """ Clears the list of activities """
        self._activities_list.clear()

    def populate_repository(self):
        """ Populates the list of activities """
        self._activities_list = [
            Activity(9500, [100, 150], {"year": 2020, "month": 12, "day": 15}, 11, "clean the house"),
            Activity(7800, [750, 200], {"year": 2020, "month": 11, "day": 28}, 9, "study"),
            Activity(2150, [350, 500, 100], {"year": 2020, "month": 12, "day": 24}, 10, "shopping"),
            Activity(1500, [350], {"year": 2020, "month": 12, "day": 31}, 6, "New Year's party"),
            Activity(5000, [100, 200, 750], {"year": 2020, "month": 12, "day": 25}, 19, "Christmas dinner")
        ]


class PersonRepository:
    """
    Class used to instantiate a persons repository.
    The repository is a collection of uniquely identifiable objects, so there cannot exist two identical persons
        in the repository (i.e. two persons having the same ID).
    """

    def __init__(self):
        """
        The constructor for a new object of type PersonRepository.
        The repository is represented as a list of persons, so it is initialized with an empty list.
        """
        self._person_list = []

    @property
    def person_list(self):
        """ Getter for the list of persons in the repository """
        return self._person_list

    @person_list.setter
    def person_list(self, new_persons_list):
        """
        Setter for the list of persons in the repository.
        Raises PersonRepositoryError if the new value of the list of persons is actually not a list or if the list
            does not contain objects of type Person.
        :param new_persons_list: the new list of persons
        """
        if isinstance(new_persons_list, list) is False:
            raise PersonRepositoryError("The list of persons was assigned an invalid data type!\n")

        for person_checker in new_persons_list:
            if isinstance(person_checker, Person) is False:
                raise PersonRepositoryError("The list does not contain persons!\n")

        self._person_list = new_persons_list

    def save_person(self, new_person):
        """
        Adds a new person to the repository.
        Raises PersonRepositoryError if there already exists a person having the same ID with the new person.
        :param new_person: the new person that is wanted to be added to the repository
        """
        if new_person in self._person_list:
            raise PersonRepositoryError("A person with this ID already exists in your agenda!\n")
        self._person_list.append(new_person)

    def check_person_existence(self, searched_person_id):
        """
        Checks whether a certain person (identified by the ID) exist in the repository.
        :param searched_person_id: the ID of the searched person
        :return: True if it exists a person having the given ID, False otherwise
        """
        ids_list = [person.id for person in self._person_list]
        return searched_person_id in ids_list

    def find_person(self, searched_person_id):
        """
        Receives an ID and looks for the person having the given ID.
        :param searched_person_id: the ID of the searched person
        :return: the person having the given ID if the person is found in the repository, None otherwise
        """
        if self.check_person_existence(searched_person_id) is False:
            return None

        for person in self._person_list:
            if person.id == searched_person_id:
                return person

    def remove_person(self, remove_person_id):
        """
        Removes a person from the repository by a given ID.
        Raises PersonRepositoryError if there is no person having the given ID in the repository.
        :param remove_person_id: the ID of the person to be removed
        """
        if self.check_person_existence(remove_person_id) is False:
            raise PersonRepositoryError("The person you want to remove was not found in the list!\n")

        for remove_candidate in self._person_list:
            if remove_candidate.id == remove_person_id:
                self._person_list.remove(remove_candidate)

    def update_person(self, person_to_update_id, updated_person):
        """
        Receives the ID of the person to be updated, and also the updated object (i.e. person) replacing the old
            object from the repository with the new one.
        Raises PersonRepositoryError if there is no person having the given ID.
        :param person_to_update_id: positive integer, the ID of the person to be updated
        :param updated_person: the updated person
        """
        if self.check_person_existence(person_to_update_id) is False:
            raise PersonRepositoryError("The person you are trying to update was not found in the list!\n")

        if person_to_update_id != updated_person.id:
            raise PersonRepositoryError("The updated person's ID does not match the old person's ID!\n")

        for person in self._person_list:
            if person.id == person_to_update_id:
                person.name = updated_person.name
                person.phone_number = updated_person.phone_number

    def get_all_persons_list(self):
        """ Returns the list persons in the repository """
        return self._person_list

    def get_number_of_persons(self):
        """ Returns the number of persons in the repository """
        return len(self._person_list)

    def __len__(self):
        """
        Overwritten len() method. We assume that the length of the repository is equal to the number of persons
        in the repository.
        """
        return len(self._person_list)

    def clear_repository(self):
        """ Clears the list of persons """
        self._person_list.clear()

    def populate_repository(self):
        """ Populates the list of persons """
        self._person_list = [
            Person(100, "Joshua Bates", "287967392"),
            Person(150, "Dillon Mendez", "659892114"),
            Person(200, "Amber Cotton", "367282906"),
            Person(350, "Isabel Fox", "947285735"),
            Person(500, "Evie Rogers", "59825723"),
            Person(700, "John Turner", "548824995")
        ]

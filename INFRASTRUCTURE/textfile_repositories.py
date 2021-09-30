from DOMAIN.entities import Person, Activity
from INFRASTRUCTURE.inmemory_repositories import PersonRepository, ActivityRepository
from UTILITY.utils import Utility

"""
- create a file: right click on package name -> new -> File -> a.txt
Open an existing file without losing already existing data:
    with open("a.txt", mode=access_mode) - access_mode == "r" / "a" / "a+"
    file = open("a.txt", access_mode) - access_mode == "r" / "a" / "a+"
Open an existing file and deleting the already existing data:
    with open("a.txt", mode=access_mode) - access_mode == "w" / "w+"
    file = open("a.txt", access_mode) - access_mode == "w" / "w+"
    
Create a file named "b.txt" using file commands:
    file = open("b.txt", access_mode) - access_mode == "w" / "w+"
        (or clears the content of b.txt if it already exists)

Close a file: file_object.close()

Write into a file:
    file.write(string) -> adds a string to the file, starting from where the position pointer is left
    file.writelines([string1, string2...]) -> adds more strings to a file, starting as in the previous case

Read from a file:
file.read() -> returns a string containing everything written in the file
file.readline() -> returns the current line from the file and moves focus to the next line
file.readlines() -> returns a list of strings: ["line 1 contents", "line 2 contents" ...]

Append data to a file:
file = open("filename", "a+")
file.write("\nI append this text to the file")
or file.writelines(["\nAdd a new line\n", "Add another line\n"])

Setting the position/pointer in a text file:
file.seek(offset, from)
    from = {0, 1, 2} 
        0 = start counting the characters from the beginning
        1 = start counting the characters from the current position
        2 = start counting the characters from the end
    offset = the number of characters we want to move from the specified starting position
"""


class TextFileActivityRepository(ActivityRepository):
    """
    Class used to instantiate activities repositories based on text files.
    Inherits from the base class ActivityRepository.
    """

    def __init__(self, filename):
        """
        Constructor of a text file based activity repository, which calls the __init__ of the base class, but in addition,
        receives a filename from which the data must be loaded and into which the data must be saved.
        :param filename: the name of the file
        """
        super().__init__()
        self.__filename = filename

    def __load_activities_from_file_into_memory(self):
        """
        Reads the file contents and transfers them into memory (i.e. the list of activities).
        Each activity should be represented in the file as it follows:
        1000;204 159;30 11 2020;19;dinner -> object of type Activity for which the attributes are:
        activity.id == 1000
        activity.participants_ids == [204, 159]
        activity.day == 30
        activity.month == 11
        activity.year == 2020
        activity.time == 19
        activity.description == "dinner"
        """
        with open(self.__filename, mode="r") as activities_file:
            super().clear_repository()
            activities_lines = activities_file.readlines()
            for activity_line in activities_lines:
                activity_line = activity_line.strip()
                if activity_line != "":
                    activity_components = activity_line.split(";")

                    # e.g. activity_components -> ["7543", "193 201", "20 12 2019", "19", "shopping"]
                    activity_id = int(activity_components[0])
                    string_of_participants_ids = activity_components[1]
                    participants_ids = Utility.convert_ids_string_to_separate_integers(string_of_participants_ids)
                    string_calendar_date = activity_components[2]
                    calendar_date = Utility.convert_calendar_date_string_to_dictionary(string_calendar_date)
                    time = int(activity_components[3])
                    description = activity_components[4]
                    activity = Activity(activity_id, participants_ids, calendar_date, time, description)
                    super().save_activity(activity)

    def __save_activities_from_memory_to_file(self):
        """
        Transfers the data from memory (i.e. the list of activities) into the file.
        """
        with open(self.__filename, mode="w") as activities_file:
            for activity in self._activities_list:
                participants_ids_as_string = Utility.convert_list_of_integers_into_string(activity.participants_ids)
                calendar_date_as_string = f"{activity.day} {activity.month} {activity.year}"
                activity_line = f"{activity.id};{participants_ids_as_string};{calendar_date_as_string};" \
                                f"{activity.time};{activity.description}\n"
                activities_file.write(activity_line)

    @property
    def activities_list(self):
        """
        Loads all the activities from the file into the list of activities.
        Returns the list of activities.
        """
        self.__load_activities_from_file_into_memory()
        return self._activities_list

    @activities_list.setter
    def activities_list(self, new_activities_list):
        """
        Setter for the list of activities.
        Raises ActivityRepositoryError if the supposed new list of activities is actually not a list, or if it does not
            contain activities.
        :param new_activities_list: the new list of activities
        Saves all the activities from the list of activities into the file.
        """
        self._activities_list = new_activities_list
        self.__save_activities_from_memory_to_file()

    def save_activity(self, new_activity):
        """
        Loads all the activities from the file into the list of activities.
        Method that adds a new activity in the repository of activities.
        Raises ActivityRepositoryError if there already exists an activity having the same ID as the new activity or
            if there is another activity in the repository that takes place in the same time time as the new activ
        Saves all the activities from the list of activities into the file.
        """
        self.__load_activities_from_file_into_memory()
        super().save_activity(new_activity)
        self.__save_activities_from_memory_to_file()

    def remove_activity(self, remove_activity_id):
        """
        Loads all the activities from the file into the list of activities.
        Removes an activity from the repository by its ID.
        Raises ActivityRepositoryError if there is no activity having the received ID.
        :param remove_activity_id: the ID of the activity that needs to be removed
        Saves all the activities from the list of activities into the file.
        """
        self.__load_activities_from_file_into_memory()
        super().remove_activity(remove_activity_id)
        self.__save_activities_from_memory_to_file()

    def update_activity(self, to_update_activity_id, updated_activity):
        """
        Loads all the activities from the file into the list of activities.
        Receives an activity ID and an updated version of that activity, and replaces the attributes of the old activity
            with the updated attributes.
        Raises ActivityRepositoryError if there is no activity in the repository having the given ID or if the new
            activity takes place in the same time with another activity already existing in the repository.
        :param to_update_activity_id: the ID of the activity that needs to be updated
        :param updated_activity: the updated version of the searched activity
        Saves all the activities from the list of activities into the file.
        """
        self.__load_activities_from_file_into_memory()
        super().update_activity(to_update_activity_id, updated_activity)
        self.__save_activities_from_memory_to_file()

    def find_activity(self, searched_activity_id):
        """
        Loads all the activities from the file into the list of activities.
        Receives an ID and finds the activity from the repository having that ID.
        :param searched_activity_id: the ID of the searched activity
        :return: the activity having the received ID, or None if there is no activity having that ID
        """
        self.__load_activities_from_file_into_memory()
        return super().find_activity(searched_activity_id)

    def check_activity_existence(self, searched_activity_id):
        """
        Loads all the activities from the file into the list of activities.
         Checks whether there is(exists) any activity in the repository having a certain ID.
        :param searched_activity_id: the ID to check
        :return: True if there is an activity having the received ID, False otherwise
        """
        self.__load_activities_from_file_into_memory()
        return super().check_activity_existence(searched_activity_id)

    def get_all_activities_list(self):
        """
        Loads all the activities from the file into the list of activities.
        Returns the complete list of activities.
        """
        self.__load_activities_from_file_into_memory()
        return super().get_all_activities_list()

    def get_number_of_activities(self):
        """
        Loads all the activities from the file into the list of activities.
        Returns the total number of activities.
        """
        self.__load_activities_from_file_into_memory()
        return super().get_number_of_activities()

    def __len__(self):
        """
        Loads all the activities from the file into the list of activities.
        Overwritten __len__ method -> the length of the repository is the same with the number of activities in the repository.
        """
        self.__load_activities_from_file_into_memory()
        return super().__len__()


class TextFilePersonRepository(PersonRepository):
    """
    Class used to instantiate persons repositories based on text files.
    Inherits from the base class PersonRepository.
    """

    def __init__(self, filename):
        """
        Constructor of a text file based person repository, which calls the __init__ of the base class, but in addition,
        receives a filename from which the data must be loaded and into which the data must be saved.
        :param filename: the name of the file
        """
        super().__init__()
        self.__filename = filename

    def __load_persons_from_file_into_memory(self):
        """
        Reads the file contents and transfers them into memory (i.e. the list of persons).
        Each person should be represented in the file as it follows:
        100;Alex;48327329 -> object of type Person for which the attributes are:
        person.id == 100
        person.name == "Alex"
        person.phone_number == "48327329"
        """
        with open(self.__filename, mode="r") as persons_file:
            super().clear_repository()
            persons_lines = persons_file.readlines()
            for person_line in persons_lines:
                person_line = person_line.strip()
                if person_line != "":
                    person_components = person_line.split(";")
                    person_id = int(person_components[0])
                    person_name = person_components[1]
                    person_phone_number = person_components[2]
                    person = Person(person_id, person_name, person_phone_number)
                    super().save_person(person)

    def __save_persons_from_memory_to_file(self):
        """
        Transfers the data from memory (i.e. the list of activities) into the file following the next syntax:
        Person(100, "Alex", "085482") -> 100;Alex;085482
        """
        with open(self.__filename, mode="w") as persons_file:
            for person in self._person_list:
                person_line = f"{person.id};{person.name.title()};{person.phone_number}\n"
                persons_file.write(person_line)

    @property
    def person_list(self):
        """
        Loads all the persons from file into the list of persons.
        Returns the list of persons.
        """
        self.__load_persons_from_file_into_memory()
        return self._person_list

    @person_list.setter
    def person_list(self, new_persons_list):
        """
        Setter for the list of persons.
        Raises PersonRepositoryError if the new value of the list of persons is actually not a list or if the list
            does not contain objects of type Person.
        :param new_persons_list: the new list of persons
        Saves all the persons from the list of persons into the file.
        """
        self._person_list = new_persons_list
        self.__save_persons_from_memory_to_file()

    def save_person(self, new_person):
        """
        Loads all the persons from file into the list of persons.
        Adds a new person to the repository.
        Raises PersonRepositoryError if there already exists a person having the same ID with the new person.
        :param new_person: the new person that is wanted to be added to the repository
        Saves all the persons from the list of persons into the file.
        """
        self.__load_persons_from_file_into_memory()
        super().save_person(new_person)
        self.__save_persons_from_memory_to_file()

    def remove_person(self, remove_person_id):
        """
        Loads all the persons from file into the list of persons.
        Removes a person from the repository by a given ID.
        Raises PersonRepositoryError if there is no person having the given ID in the repository.
        :param remove_person_id: the ID of the person to be removed
        Saves all the persons from the list of persons into the file.
        """
        self.__load_persons_from_file_into_memory()
        super().remove_person(remove_person_id)
        self.__save_persons_from_memory_to_file()

    def check_person_existence(self, searched_person_id):
        """
        Loads all the persons from file into the list of persons.
        Checks whether a certain person (identified by the ID) exist in the repository.
        :param searched_person_id: the ID of the searched person
        :return: True if it exists a person having the given ID, False otherwise
        """
        self.__load_persons_from_file_into_memory()
        return super().check_person_existence(searched_person_id)

    def find_person(self, searched_person_id):
        """
        Loads all the persons from file into the list of persons.
        Receives an ID and looks for the person having the given ID.
        :param searched_person_id: the ID of the searched person
        :return: the person having the given ID if the person is found in the repository, None otherwise
        """
        self.__load_persons_from_file_into_memory()
        return super().find_person(searched_person_id)

    def update_person(self, person_to_update_id, updated_person):
        """
        Loads all the persons from file into the list of persons.
        Receives the ID of the person to be updated, and also the updated object (i.e. person) replacing the old
            object from the repository with the new one.
        Raises PersonRepositoryError if there is no person having the given ID.
        :param person_to_update_id: positive integer, the ID of the person to be updated
        :param updated_person: the updated person
        Saves all the persons from the list of persons into the file.
        """
        self.__load_persons_from_file_into_memory()
        super().update_person(person_to_update_id, updated_person)
        self.__save_persons_from_memory_to_file()

    def get_all_persons_list(self):
        """
        Loads all the persons from file into the list of persons.
        Returns the list persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().get_all_persons_list()

    def get_number_of_persons(self):
        """
        Loads all the persons from file into the list of persons.
        Returns the number of persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().get_number_of_persons()

    def __len__(self):
        """
        Loads all the persons from file into the list of persons.
        Overwritten __len__ method -> the length of the repository is the same with the number of persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().__len__()

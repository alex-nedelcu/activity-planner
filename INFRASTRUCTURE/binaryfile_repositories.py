import pickle

from INFRASTRUCTURE.inmemory_repositories import PersonRepository, ActivityRepository

"""
    Binary files:
        access modes:
            - rb - opens the file for reading in binary format -> FileNotFoundError if the file does not exist
            - rb+ - opens the file for reading and writing in binary format -> FileNotFoundError if the file does not exist
            - wb - opens the file for writing in binary format -> creates the file if it does not exist
            - wb+ - opens the file for reading and writing in binary format -> creates the file if it does not exist
            - ab - opens the file for appending in binary format -> creates the file if it does not exist
            - ab+ - opens the file for reading and appending in binary format -> creates the file if it does not exist

    SERIALIZATION = process of converting an object in memory to a byte stream that can be stored on disk or sent over a network
    DESERIALIZATION = process of converting a byte stream to Python object.
        * byte stream = ordered sequence of bytes

    serialization = pickling = marshalling
    deserialization = unpickling = unmarshalling

Store data from memory into a binary file:
    pickle.dump(data_from_memory, filename)
    data = pickle.load(filename)
    
            with open("a.pickle", mode="wb") as my_file:
                my_list = ["abc", 1, "Alex", 100.51]
                pickle.dump(my_list, my_file)
        
            with open("a.pickle", mode="rb") as my_file:
                my_list = pickle.load(my_file)
"""


class BinaryFilePersonRepository(PersonRepository):
    """
    Class used to instantiate persons repositories based on binary files.
    Inherits from the base class PersonRepository.
    """

    def __init__(self, filename):
        """
        The constructor of a person repository based on a binary file, which calls the __init__ method of the base class,
        but in addition receives the name of the binary file from which data is loaded and into which data is saved.
        :param filename: the name of the binary file
        """
        super().__init__()
        self.__filename = filename

    def __save_persons_from_memory_to_file(self):
        """
        Dumps the list of persons from the memory into the binary file.
        """
        with open(self.__filename, mode="wb") as persons_binary_file:
            pickle.dump(self._person_list, persons_binary_file)

    def __load_persons_from_file_into_memory(self):
        """
        Takes the list of persons from the binary file and loads it into memory.
        """
        with open(self.__filename, mode="rb") as persons_binary_file:
            super().clear_repository()
            self._person_list = pickle.load(persons_binary_file)

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

    def find_person(self, searched_person_id):
        """
        Loads all the persons from file into the list of persons.
        Receives an ID and looks for the person having the given ID.
        :param searched_person_id: the ID of the searched person
        :return: the person having the given ID if the person is found in the repository, None otherwise
        """
        self.__load_persons_from_file_into_memory()
        return super().find_person(searched_person_id)

    def check_person_existence(self, searched_person_id):
        """
        Loads all the persons from file into the list of persons.
        Checks whether a certain person (identified by the ID) exist in the repository.
        :param searched_person_id: the ID of the searched person
        :return: True if it exists a person having the given ID, False otherwise
        """
        self.__load_persons_from_file_into_memory()
        return super().check_person_existence(searched_person_id)

    def get_number_of_persons(self):
        """
        Loads all the persons from file into the list of persons.
        Returns the number of persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().get_number_of_persons()

    def get_all_persons_list(self):
        """
        Loads all the persons from file into the list of persons.
        Returns the list persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().get_all_persons_list()

    def __len__(self):
        """
        Loads all the persons from file into the list of persons.
        Overwritten __len__ method -> the length of the repository is the same with the number of persons in the repository
        """
        self.__load_persons_from_file_into_memory()
        return super().__len__()


class BinaryFileActivityRepository(ActivityRepository):
    """
    Class used to instantiate activities repositories based on binary files.
    Inherits from the base class ActivityRepository.
    """

    def __init__(self, filename):
        """
        The constructor of an activity repository based on a binary file, which calls the __init__ method of the base class,
        but in addition receives the name of the binary file from which data is loaded and into which data is saved.
        :param filename: the name of the binary file
        """
        super().__init__()
        self.__filename = filename

    def __save_activities_from_memory_to_file(self):
        """
        Dumps the list of activities from the memory into the binary file.
        """
        with open(self.__filename, mode="wb") as activities_binary_file:
            pickle.dump(self._activities_list, activities_binary_file)

    def __load_activities_from_file_into_memory(self):
        """
        Takes the list of activities from the binary file and loads it into memory.
        """
        with open(self.__filename, mode="rb") as activities_binary_file:
            super().clear_repository()
            self._activities_list = pickle.load(activities_binary_file)

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

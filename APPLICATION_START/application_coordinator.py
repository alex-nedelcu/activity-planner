import json
import pickle

from BUSINESS.services import PersonService, ActivityService, UndoService, RedoService, StatisticsService
from DOMAIN.entities import Person, Activity
from EXCEPTIONS.custom_exceptions import ApplicationStartError
from INFRASTRUCTURE.binaryfile_repositories import BinaryFileActivityRepository, BinaryFilePersonRepository
from INFRASTRUCTURE.inmemory_repositories import PersonRepository, ActivityRepository
from INFRASTRUCTURE.json_repositories import JsonFilePersonRepository, JsonFileActivityRepository
from INFRASTRUCTURE.stacks import UndoStack, RedoStack
from INFRASTRUCTURE.textfile_repositories import TextFilePersonRepository, TextFileActivityRepository
from PRESENTATION.UI import UI
from VALIDATION.validators import Validator


class ApplicationCoordinator:
    """ Instantiates objects used to start the application """

    def __init__(self, application_setter):
        """
        The constructor of an application coordinator, having a dependency relationship with an application setter.
        :param application_setter: the application setter injected into the application coordinator
        """
        self.__application_setter = application_setter

    def start_application(self):
        """
        The method that runs the application.
        """
        person_validator = Validator()
        activity_validator = Validator()
        undo_stack = UndoStack()
        redo_stack = RedoStack()

        if self.__application_setter.repository_type == "inmemory":
            person_repository = PersonRepository()
            activity_repository = ActivityRepository()
            person_repository.populate_repository()
            activity_repository.populate_repository()
        elif self.__application_setter.repository_type == "textfile":
            persons_text_file_name = self.__application_setter.persons_file
            activities_text_file_name = self.__application_setter.activities_file
            person_repository = TextFilePersonRepository(persons_text_file_name)
            activity_repository = TextFileActivityRepository(activities_text_file_name)
        elif self.__application_setter.repository_type == "binaryfile":
            persons_binary_file_name = self.__application_setter.persons_file
            activities_binary_file_name = self.__application_setter.activities_file

            persons = [
                Person(100, "Joshua Bates", "287967392"),
                Person(150, "Dillon Mendez", "659892114"),
                Person(200, "Amber Cotton", "367282906"),
                Person(350, "Isabel Fox", "947285735"),
                Person(500, "Evie Rogers", "59825723"),
                Person(700, "John Turner", "548824995")
            ]
            with open(persons_binary_file_name, mode="wb") as persons_binary_file:
                pickle.dump(persons, persons_binary_file)

            activities = [
                Activity(9500, [100, 150], {"year": 2020, "month": 12, "day": 15}, 11, "clean the house"),
                Activity(7800, [750, 200], {"year": 2020, "month": 11, "day": 28}, 9, "study"),
                Activity(2150, [350, 500, 100], {"year": 2020, "month": 12, "day": 24}, 10, "shopping"),
                Activity(1500, [350], {"year": 2020, "month": 12, "day": 31}, 6, "New Year's party"),
                Activity(5000, [100, 200, 750], {"year": 2020, "month": 12, "day": 25}, 19, "Christmas dinner")
            ]
            with open(activities_binary_file_name, mode="wb") as activities_binary_file:
                pickle.dump(activities, activities_binary_file)

            person_repository = BinaryFilePersonRepository(persons_binary_file_name)
            activity_repository = BinaryFileActivityRepository(activities_binary_file_name)
        elif self.__application_setter.repository_type == "jsonfile":
            persons_json_file_name = self.__application_setter.persons_file
            activities_json_file_name = self.__application_setter.activities_file
            persons = [
                Person(100, "Jason Bob", "287967392"),
                Person(150, "Jason Dilan", "659892114"),
                Person(200, "Jason Casper", "367282906"),
                Person(350, "Jason Mike", "947285735"),
                Person(500, "Jason Elizabeth", "59825723"),
                Person(700, "Jason Lorelei", "548824995")
            ]
            with open(persons_json_file_name, mode="w") as persons_json_file:
                """
                -> the dictionary we'll introduce in the json file has the following form:
                
                    persons_list_as_dictionary == 
                                {
                                    "persons": [person_1_dictionary ... person_n_dictionary]
                                }
                    where person_n_dictionary ==
                                {
                                    "id": person.id,
                                    "name": person.name,
                                    "phone_number": person.phone_number
                                }
                """
                persons_list_as_dictionary = {}
                persons_list_as_dictionary["persons"] = []
                for person in persons:
                    person_dictionary = {
                        "id": person.id,
                        "name": person.name,
                        "phone_number": person.phone_number
                    }
                    persons_list_as_dictionary["persons"].append(person_dictionary)
                pretty_printed_persons_dictionary = json.dumps(persons_list_as_dictionary, indent=4)
                persons_json_file.write(pretty_printed_persons_dictionary)

            activities = [
                Activity(9500, [100, 150], {"year": 2020, "month": 12, "day": 15}, 11, "clean the house"),
                Activity(7800, [750, 200], {"year": 2020, "month": 11, "day": 28}, 9, "study"),
                Activity(2150, [350, 500, 100], {"year": 2020, "month": 12, "day": 24}, 10, "shopping")
            ]
            with open(activities_json_file_name, mode="w") as activities_json_file:
                """
                -> the dictionary we'll introduce in the json file has the following form:
                
                    activities_list_as_dictionary == 
                                {
                                    "activities": [activity_1_dictionary ... activity_n_dictionary]
                                }
                    where activity_n_dictionary ==
                                {
                                    "id": activity.id,
                                    "participants_ids": activity.participants_ids -> list,
                                    "date": activity.date,
                                    "time": activity.time,
                                    "description": activity.description
                                }
                """
                activities_list_as_dictionary = {}
                activities_list_as_dictionary["activities"] = []
                for activity in activities:
                    activity_dictionary = {
                        "id": activity.id,
                        "participants_ids": activity.participants_ids,
                        "date": activity.date,
                        "time": activity.time,
                        "description": activity.description
                    }
                    activities_list_as_dictionary["activities"].append(activity_dictionary)
                pretty_printed_activities_dictionary = json.dumps(activities_list_as_dictionary, indent=4)
                activities_json_file.write(pretty_printed_activities_dictionary)

            person_repository = JsonFilePersonRepository(persons_json_file_name)
            activity_repository = JsonFileActivityRepository(activities_json_file_name)
        else:
            raise ApplicationStartError("The settings are invalid!\n")

        person_service = PersonService(person_validator, person_repository, undo_stack, redo_stack)
        activity_service = ActivityService(activity_validator, activity_repository, person_repository, undo_stack,
                                           redo_stack)
        undo_service = UndoService(person_repository, activity_repository, undo_stack, redo_stack)
        redo_service = RedoService(person_repository, activity_repository, undo_stack, redo_stack)
        statistics_service = StatisticsService(activity_repository)

        console = UI(person_service, activity_service, statistics_service, undo_service, redo_service)
        console.run()

import unittest

from BUSINESS.services import StatisticsService, ActivityService, PersonService, UndoService, RedoService
from DOMAIN.entities import Activity, Person, Operation
from EXCEPTIONS.custom_exceptions import ActivityServiceError, DateValidatorError, ActivityValidatorError, \
    PersonValidatorError, ActivityRepositoryError, PersonRepositoryError, PersonServiceError, StackError
from INFRASTRUCTURE.inmemory_repositories import ActivityRepository, PersonRepository
from INFRASTRUCTURE.stacks import UndoStack, RedoStack
from VALIDATION.validators import Validator


class UndoServiceTest(unittest.TestCase):
    def setUp(self):
        self.__person_repository = PersonRepository()
        self.__activity_repository = ActivityRepository()
        self.__undo_stack = UndoStack()
        self.__redo_stack = RedoStack()
        self.__person_validator = Validator()
        self.__activity_validator = Validator()
        self.__person_service = PersonService(self.__person_validator, self.__person_repository, self.__undo_stack,
                                              self.__redo_stack)
        self.__activity_service = ActivityService(self.__activity_validator, self.__activity_repository,
                                                  self.__person_repository, self.__undo_stack, self.__redo_stack)
        self.__person_repository.person_list = [
            Person(876, "Alex", "223543"),
            Person(456, "Ion", "64765"),
            Person(534, "Radu", "65432")
        ]
        self.__activity_repository.activities_list = [
            Activity(1145, [241, 356, 524], {"year": 2020, "month": 11, "day": 27}, 23, "go to Shanghai"),
            Activity(9842, [143, 356, 978], {"year": 2020, "month": 11, "day": 29}, 20, "shopping"),
            Activity(1237, [524], {"year": 2020, "month": 8, "day": 29}, 14, "trip to Cluj")
        ]
        self.__undo_service = UndoService(self.__person_repository, self.__activity_repository, self.__undo_stack,
                                          self.__redo_stack)

    def test_undo_add_person(self):
        self.__person_service.service_add_person(548, "Mihai", "54354534")
        self.assertEqual(len(self.__undo_stack), 1)
        self.assertTrue(Person(548, "Mihai", "54354534") in self.__person_repository.person_list)
        self.__undo_service.undo()
        self.assertFalse(Person(548, "Mihai", "54354534") in self.__person_repository.person_list)

    def test_undo_remove_person(self):
        self.assertEqual(len(self.__person_repository), 3)
        self.__person_service.service_remove_person(456)
        self.assertEqual(len(self.__person_repository), 2)
        self.assertTrue(Person(456, None, None) not in self.__person_repository.person_list)
        self.__undo_service.undo()
        self.assertTrue(Person(456, "Ion", "64765") in self.__person_repository.person_list)
        self.assertEqual(len(self.__person_repository), 3)
        self.assertEqual(self.__person_repository.person_list[-1], Person(456, "Ion", "64765"))

    def test_undo_update_person(self):
        self.assertEqual(self.__person_repository.person_list[-1].name, "Radu")
        self.assertEqual(self.__person_repository.person_list[-1].phone_number, "65432")
        self.__person_service.service_update_person(534, "Radu v2.0", "111111")
        self.assertEqual(self.__person_repository.person_list[-1].name, "Radu v2.0")
        self.assertEqual(self.__person_repository.person_list[-1].phone_number, "111111")
        self.__undo_service.undo()
        self.assertEqual(self.__person_repository.person_list[-1].name, "Radu")
        self.assertEqual(self.__person_repository.person_list[-1].phone_number, "65432")

    def test_undo_add_activity(self):
        self.assertEqual(len(self.__activity_repository), 3)
        self.__activity_service.service_add_activity(5341, [876], {"year": 2019, "month": 9, "day": 5}, 10, "idk")
        self.assertEqual(len(self.__activity_repository), 4)
        self.assertEqual(len(self.__undo_stack), 1)
        self.assertTrue(Activity(5341, None, None, None, None) in self.__activity_repository.activities_list)
        self.__undo_service.undo()
        self.assertTrue(Activity(5341, None, None, None, None) not in self.__activity_repository.activities_list)
        self.assertEqual(len(self.__activity_repository), 3)

    def test_undo_remove_activity(self):
        self.assertEqual(len(self.__activity_repository), 3)
        self.__activity_service.service_remove_activity(1145)
        self.assertEqual(len(self.__activity_repository), 2)
        self.__undo_service.undo()
        activity = Activity(1145, [241, 356, 524], {"year": 2020, "month": 11, "day": 27}, 23, "go to Shanghai")
        self.assertTrue(activity in self.__activity_repository.activities_list)

    def test_undo_update_activity(self):
        self.__activity_service.service_update_activity(1145, [534], {"year": 2015, "month": 10, "day": 10}, 10,
                                                        "updated description")
        self.assertEqual(self.__activity_repository.activities_list[0].description, "updated description")
        self.__undo_service.undo()
        self.assertEqual(self.__activity_repository.activities_list[0].description, "go to Shanghai")


class RedoServiceTest(unittest.TestCase):
    def setUp(self):
        self.__person_repository = PersonRepository()
        self.__activity_repository = ActivityRepository()
        self.__undo_stack = UndoStack()
        self.__redo_stack = RedoStack()
        self.__person_validator = Validator()
        self.__activity_validator = Validator()
        self.__person_service = PersonService(self.__person_validator, self.__person_repository, self.__undo_stack,
                                              self.__redo_stack)
        self.__activity_service = ActivityService(self.__activity_validator, self.__activity_repository,
                                                  self.__person_repository, self.__undo_stack, self.__redo_stack)
        self.__person_repository.person_list = [
            Person(100, "Bob", "75656856"),
            Person(200, "John", "23423423"),
            Person(300, "Tom", "6456456546")
        ]
        self.__activity_repository.activities_list = [
            Activity(1500, [100, 200, 300], {"year": 2020, "month": 10, "day": 25}, 23, "go to Berlin"),
            Activity(5000, [200], {"year": 2020, "month": 12, "day": 18}, 20, "business call"),
            Activity(1000, [100, 300], {"year": 2019, "month": 8, "day": 11}, 14, "go to seaside")
        ]
        self.__undo_service = UndoService(self.__person_repository, self.__activity_repository, self.__undo_stack,
                                          self.__redo_stack)
        self.__redo_service = RedoService(self.__person_repository, self.__activity_repository, self.__undo_stack,
                                          self.__redo_stack)

    def test_redo_add_person(self):
        self.__person_service.service_add_person(400, "Josh", "43345434")
        self.assertTrue(Person(400, "Josh", "43345434") in self.__person_repository.person_list)
        self.__undo_service.undo()
        self.assertTrue(Person(400, "Josh", "43345434") not in self.__person_repository.person_list)
        self.__redo_service.redo()
        self.assertTrue(Person(400, "Josh", "43345434") in self.__person_repository.person_list)

    def test_redo_remove_person(self):
        self.__person_service.service_remove_person(100)
        self.assertTrue(Person(100, "Bob", "75656856") not in self.__person_repository.person_list)
        self.__undo_service.undo()
        self.assertTrue(Person(100, "Bob", "75656856") in self.__person_repository.person_list)
        self.__redo_service.redo()
        self.assertTrue(Person(100, "Bob", "75656856") not in self.__person_repository.person_list)

    def test_redo_update_person(self):
        self.__person_service.service_update_person(100, "Bob v2", "911")
        self.assertEqual(self.__person_repository.person_list[0].name, "Bob v2")
        self.__undo_service.undo()
        self.assertEqual(self.__person_repository.person_list[0].name, "Bob")
        self.__redo_service.redo()
        self.assertEqual(self.__person_repository.person_list[0].name, "Bob v2")

    def test_redo_add_activity(self):
        self.__activity_service.service_add_activity(9999, [100, 200], {"year": 2020, "month": 10, "day": 25}, 7, "gym")
        self.assertTrue(Activity(9999, None, None, None, None) in self.__activity_repository.activities_list)
        self.__undo_service.undo()
        self.assertTrue(Activity(9999, None, None, None, None) not in self.__activity_repository.activities_list)
        self.__redo_service.redo()
        self.assertTrue(Activity(9999, None, None, None, None) in self.__activity_repository.activities_list)

    def test_redo_remove_activity(self):
        self.__activity_service.service_remove_activity(1500)
        self.assertTrue(self.__activity_repository.check_activity_existence(1500) is False)
        self.__undo_service.undo()
        self.assertTrue(self.__activity_repository.check_activity_existence(1500) is True)
        self.__redo_service.redo()
        self.assertTrue(self.__activity_repository.check_activity_existence(1500) is False)

    def test_redo_update_activity(self):
        self.__activity_service.service_update_activity(1000, [200, 300], {"year": 2020, "month": 10, "day": 15}, 10,
                                                        "updated description")
        self.assertEqual(self.__activity_repository.activities_list[2].description, "updated description")
        self.__undo_service.undo()
        self.assertEqual(self.__activity_repository.activities_list[2].description, "go to seaside")
        self.__redo_service.redo()
        self.assertEqual(self.__activity_repository.activities_list[2].description, "updated description")


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.__activity_validator = Validator()
        self.__person_validator = Validator()
        self.__date_validator = Validator()

    def test_validate_activity(self):
        invalid_activity_0 = Activity(-1041, [], {"year": -439, "month": 49, "day": -11}, 29, "")
        self.assertRaises(ActivityValidatorError, self.__activity_validator.validate_activity, invalid_activity_0)
        valid_activity = Activity(9542, [100], {"year": 2020, "month": 10, "day": 11}, 5, "description")
        self.assertIsNone(self.__activity_validator.validate_activity(valid_activity))
        invalid_activity_1 = Activity(-1041, ["a", 312], {"year": 2019, "month": 10, "day": 12}, 20, "not empty")
        invalid_activity_2 = Activity(5941, [542], {"year": -439, "month": 10, "day": 20}, 21, "blabla")
        self.assertRaises(ActivityValidatorError, self.__activity_validator.validate_activity, invalid_activity_1)
        self.assertRaises(ActivityValidatorError, self.__activity_validator.validate_activity, invalid_activity_2)

    def test_validate_person(self):
        invalid_person_0 = Person(-454, "", "")
        self.assertRaises(PersonValidatorError, self.__person_validator.validate_person, invalid_person_0)
        valid_person = Person(439, "Robert", "329423")
        self.assertIsNone(self.__person_validator.validate_person(valid_person))
        invalid_person_1 = Person(-454, "Mihai", "4933")
        invalid_person_2 = Person(123, "", "654654")
        invalid_person_3 = Person(439, "Robi", "")
        self.assertRaises(PersonValidatorError, self.__person_validator.validate_person, invalid_person_1)
        self.assertRaises(PersonValidatorError, self.__person_validator.validate_person, invalid_person_2)
        self.assertRaises(PersonValidatorError, self.__person_validator.validate_person, invalid_person_3)

    def test_validate_calendar_date(self):
        invalid_date_0 = {"year": -439, "month": 29, "day": 54}
        self.assertRaises(DateValidatorError, self.__date_validator.validate_calendar_date, invalid_date_0)
        invalid_date_1 = {"year": -439, "month": 29, "day": 54}
        invalid_date_2 = {"year": 2019, "month": 10, "day": 54}
        invalid_date_3 = {"year": 2013, "month": -5, "day": 10}
        invalid_date_4 = {"year": 2010, "month": 14, "day": -4}
        self.assertRaises(DateValidatorError, self.__date_validator.validate_calendar_date, invalid_date_1)
        self.assertRaises(DateValidatorError, self.__date_validator.validate_calendar_date, invalid_date_2)
        self.assertRaises(DateValidatorError, self.__date_validator.validate_calendar_date, invalid_date_3)
        self.assertRaises(DateValidatorError, self.__date_validator.validate_calendar_date, invalid_date_4)


class ActivityRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.__activity_repository = ActivityRepository()
        self.__activity_repository.activities_list = [
            Activity(1237, [524], {"year": 2020, "month": 8, "day": 29}, 14, "trip to Cluj"),
            Activity(9874, [143, 241], {"year": 2020, "month": 11, "day": 28}, 11, "clean the house"),
            Activity(8731, [356, 654], {"year": 2018, "month": 11, "day": 13}, 9, "study"),
            Activity(9933, [241, 876, 978], {"year": 2020, "month": 11, "day": 29}, 10, "drive to Bucharest"),
        ]

    def test_activities_list_property(self):
        self.__activity_repository.activities_list = [
            Activity(9493, [100], {"year": 2010, "month": 10, "day": 15}, 9, "holiday")]
        self.assertEqual(self.__activity_repository.activities_list,
                         [Activity(9493, [100], {"year": 2010, "month": 10, "day": 15}, 9, "holiday")])

    def test_activities_list_property_setter(self):
        with self.assertRaises(ActivityRepositoryError):
            self.__activity_repository.activities_list = [10, 20, "not an activity object obviously"]
        with self.assertRaises(ActivityRepositoryError):
            self.__activity_repository.activities_list = "not a list of activities"

    def test_save_activity(self):
        new_activity = Activity(9494, [130], {"year": 2008, "month": 3, "day": 16}, 20, "go to theatre")
        self.assertTrue(len(self.__activity_repository), 4)
        self.__activity_repository.save_activity(new_activity)
        self.assertTrue(len(self.__activity_repository), 5)
        self.assertTrue(new_activity in self.__activity_repository.activities_list)
        another_activity = Activity(1000, [304], {"year": 2011, "month": 1, "day": 8}, 9, "go to museum")
        self.assertFalse(another_activity in self.__activity_repository.activities_list)
        invalid_activity = Activity(9494, [500], {"year": 1999, "month": 9, "day": 1}, 3, "party")
        with self.assertRaises(ActivityRepositoryError):
            self.__activity_repository.save_activity(invalid_activity)
        invalid_activity = Activity(1034, [506], {"year": 2008, "month": 3, "day": 16}, 20, "go to the market")
        with self.assertRaises(ActivityRepositoryError):
            self.__activity_repository.save_activity(invalid_activity)

    def test_find_activity(self):
        searched_activity = Activity(8731, [356, 654], {"year": 2018, "month": 11, "day": 13}, 9, "study")
        self.assertTrue(self.__activity_repository.find_activity(8731) == searched_activity)
        self.assertTrue(self.__activity_repository.find_activity(0000) is None)

    def test_check_activity_existence(self):
        self.assertTrue(self.__activity_repository.check_activity_existence(9933) is True)
        self.assertTrue(self.__activity_repository.check_activity_existence(1000) is False)
        self.assertFalse(self.__activity_repository.check_activity_existence(1237) is False)

    def test_remove_activity(self):
        self.assertEqual(len(self.__activity_repository), 4)
        self.assertIsNotNone(self.__activity_repository.find_activity(9933))
        remove_activity_id = 9933
        self.__activity_repository.remove_activity(remove_activity_id)
        self.assertEqual(len(self.__activity_repository), 3)
        self.assertIsNone(self.__activity_repository.find_activity(9933))
        remove_activity_id = 9933
        self.assertRaises(ActivityRepositoryError, self.__activity_repository.remove_activity, remove_activity_id)

    def test_update_activity(self):
        updated_activity = Activity(9933, [241], {"year": 2020, "month": 12, "day": 1}, 8, "drive to airport")
        self.__activity_repository.update_activity(9933, updated_activity)
        self.assertEqual(self.__activity_repository.activities_list[-1].time, 8)
        self.assertEqual(self.__activity_repository.activities_list[-1].date, {"year": 2020, "month": 12, "day": 1})
        self.assertRaises(ActivityRepositoryError, self.__activity_repository.update_activity, 1049, updated_activity)
        invalid_updated_activity = Activity(8731, [356, 654], {"year": 2020, "month": 11, "day": 28}, 11, "study")
        self.assertRaises(ActivityRepositoryError, self.__activity_repository.update_activity, 8731,
                          invalid_updated_activity)

    def test_activity_repository_getters(self):
        self.assertEqual(self.__activity_repository.get_number_of_activities(), 4)
        new_activity = Activity(9494, [130], {"year": 2008, "month": 3, "day": 16}, 20, "go to theatre")
        self.__activity_repository.save_activity(new_activity)
        self.assertEqual(self.__activity_repository.get_number_of_activities(), 5)
        expected_list = [
            Activity(1237, [524], {"year": 2020, "month": 8, "day": 29}, 14, "trip to Cluj"),
            Activity(9874, [143, 241], {"year": 2020, "month": 11, "day": 28}, 11, "clean the house"),
            Activity(8731, [356, 654], {"year": 2018, "month": 11, "day": 13}, 9, "study"),
            Activity(9933, [241, 876, 978], {"year": 2020, "month": 11, "day": 29}, 10, "drive to Bucharest"),
            Activity(9494, [130], {"year": 2008, "month": 3, "day": 16}, 20, "go to theatre")
        ]
        self.assertTrue(self.__activity_repository.get_all_activities_list() == expected_list)


class PersonRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.__person_repository = PersonRepository()
        self.__person_repository.person_list = [
            Person(456, "Ion", "64765"),
            Person(534, "Radu", "65432"),
            Person(241, "Cosmin", "435436"),
            Person(423, "Tibi", "895334"),
            Person(978, "Andrei", "6539434"),
            Person(356, "Sorin", "832923")
        ]

    def test_person_list_property(self):
        expected_list = [
            Person(456, "Ion", "64765"),
            Person(534, "Radu", "65432"),
            Person(241, "Cosmin", "435436"),
            Person(423, "Tibi", "895334"),
            Person(978, "Andrei", "6539434"),
            Person(356, "Sorin", "832923")
        ]
        self.assertEqual(self.__person_repository.person_list, expected_list)

    def test_person_list_property_setter(self):
        self.__person_repository.person_list = [Person(100, "Gigi", "543534")]
        expected_list = [Person(100, "Gigi", "543534")]
        self.assertEqual(self.__person_repository.person_list, expected_list)
        with self.assertRaises(PersonRepositoryError):
            self.__person_repository.person_list = "not a list"
        with self.assertRaises(PersonRepositoryError):
            self.__person_repository.person_list = ["a list", "but not with", "persons", 1]

    def test_save_person(self):
        self.assertEqual(len(self.__person_repository), 6)
        new_person = Person(103, "John", "548765")
        self.__person_repository.save_person(new_person)
        self.assertEqual(len(self.__person_repository), 7)
        self.assertTrue(new_person in self.__person_repository.person_list)
        self.assertRaises(PersonRepositoryError, self.__person_repository.save_person, new_person)

    def test_find_person(self):
        self.assertEqual(self.__person_repository.find_person(356), Person(356, "Sorin", "832923"))
        self.assertIsNone(self.__person_repository.find_person(1493))

    def test_check_person_existence(self):
        self.assertTrue(self.__person_repository.check_person_existence(978))
        self.assertTrue(self.__person_repository.check_person_existence(423))
        self.assertFalse(self.__person_repository.check_person_existence(999))

    def test_remove_person(self):
        self.assertTrue(self.__person_repository.check_person_existence(423))
        self.__person_repository.remove_person(423)
        self.assertFalse(self.__person_repository.check_person_existence(423))
        self.assertRaises(PersonRepositoryError, self.__person_repository.remove_person, 423)

    def test_update_person(self):
        updated_person = Person(456, "Ionel", "102938")
        self.assertFalse(self.__person_repository.person_list[0].name == updated_person.name)
        self.assertFalse(self.__person_repository.person_list[0].phone_number == updated_person.phone_number)
        self.__person_repository.update_person(456, updated_person)
        self.assertEqual(self.__person_repository.person_list[0], updated_person)
        updated_person = Person(499, "Raul", "430222")
        self.assertRaises(PersonRepositoryError, self.__person_repository.update_person, 499, updated_person)
        self.assertRaises(PersonRepositoryError, self.__person_repository.update_person, 423, updated_person)

    def test_person_repository_getters(self):
        self.assertEqual(self.__person_repository.get_number_of_persons(), 6)
        new_person = Person(667, "Rob", "898654")
        self.__person_repository.save_person(new_person)
        self.assertEqual(self.__person_repository.get_number_of_persons(), 7)
        expected_list = [
            Person(456, "Ion", "64765"),
            Person(534, "Radu", "65432"),
            Person(241, "Cosmin", "435436"),
            Person(423, "Tibi", "895334"),
            Person(978, "Andrei", "6539434"),
            Person(356, "Sorin", "832923"),
            Person(667, "Rob", "898654")
        ]
        self.assertEqual(self.__person_repository.get_all_persons_list(), expected_list)


class DomainTest(unittest.TestCase):
    def test_operation(self):
        person = Person(134, "Bob", "534543")
        direct_action = "remove person"
        direct_action_argument = 134
        inverse_action = "add person"
        inverse_action_argument = person
        operation = Operation(direct_action, direct_action_argument, inverse_action, inverse_action_argument)
        self.assertEqual(operation.direct_action, "remove person")
        self.assertEqual(operation.inverse_action, "add person")
        self.assertEqual(operation.direct_action_argument, 134)
        self.assertEqual(operation.inverse_action_argument, person)

    def test_activity(self):
        activity_id = 4184
        participants_ids = [193, 438]
        date = {"year": 2020, "month": 10, "day": 15}
        time = 21
        description = "basketball"
        activity = Activity(activity_id, participants_ids, date, time, description)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(activity.id, 4184)
        self.assertEqual(participants_ids, [193, 438])
        self.assertEqual(activity.date, {"year": 2020, "month": 10, "day": 15})
        self.assertEqual(activity.year, 2020)
        self.assertEqual(activity.month, 10)
        self.assertEqual(activity.day, 15)
        self.assertEqual(activity.time, 21)
        self.assertEqual(activity.description, "basketball")
        self.assertFalse(activity.description == "football")
        activity.participants_ids = [100]
        self.assertEqual(activity.participants_ids, [100])
        with self.assertRaises(ActivityValidatorError):
            activity.participants_ids = "abc"
        with self.assertRaises(ActivityValidatorError):
            activity.year = -139
        with self.assertRaises(ActivityValidatorError):
            activity.month = 39
        with self.assertRaises(ActivityValidatorError):
            activity.day = 59
        with self.assertRaises(ActivityValidatorError):
            activity.time = 93
        with self.assertRaises(ActivityValidatorError):
            activity.date = "not a correct format"
        with self.assertRaises(ActivityValidatorError):
            activity.description = ""
        activity.date = {"year": 2018, "month": 11, "day": 25}
        self.assertEqual(activity.date, {"year": 2018, "month": 11, "day": 25})
        activity.year = 2021
        activity.month = 8
        activity.day = 30
        activity.time = 10
        self.assertEqual(activity.year, 2021)
        self.assertEqual(activity.month, 8)
        self.assertEqual(activity.day, 30)
        self.assertEqual(activity.time, 10)
        activity.description = "new description"
        self.assertEqual(activity.description, "new description")
        self.assertEqual(str(activity), "ID {}  ⏦  performed together with the persons having the IDs: {}\n"
                                        "Description: {}\n"
                                        "In {}.{}.{}, at {}:00".format(activity.id, activity.participants_ids,
                                                                       activity.description, activity.day,
                                                                       activity.month,
                                                                       activity.year, activity.time))
        new_activity = Activity(4184, [310], {"year": 2015, "month": 1, "day": 29}, 20, "testing")
        self.assertEqual(activity, new_activity)

    def test_person(self):
        person_id = 193
        person_name = "George"
        person_phone_number = "9252085"
        person = Person(person_id, person_name, person_phone_number)
        self.assertTrue(isinstance(person, Person))
        self.assertEqual(person.id, 193)
        self.assertEqual(person.name, "George")
        self.assertEqual(person.phone_number, "9252085")
        person.name = "Mihai"
        self.assertEqual(person.name, "Mihai")
        with self.assertRaises(PersonValidatorError):
            person.name = ""
        person.phone_number = "1944442"
        self.assertTrue(person.phone_number == "1944442")
        with self.assertRaises(PersonValidatorError):
            person.phone_number = ""
        another_person = Person(493, "Andra", "3595494")
        self.assertNotEqual(person, another_person)
        self.assertEqual(Person(100, None, None), Person(100, None, None))
        self.assertEqual(str(person), "ID {}  ⏦  name: {}  ⏦  phone number: {}".format(person.id,
                                                                                       person.name.title(),
                                                                                       person.phone_number))


class StatisticsServiceTest(unittest.TestCase):
    def setUp(self):
        self.__activity_repository = ActivityRepository()
        self.__activity_repository.activities_list = [
            Activity(9933, [241, 876, 978], {"year": 2020, "month": 11, "day": 29}, 10, "drive to Bucharest"),
            Activity(1393, [356], {"year": 2020, "month": 11, "day": 28}, 6, "city-break"),
            Activity(4832, [423, 356], {"year": 2020, "month": 12, "day": 18}, 19, "yoga")
        ]
        self.__statistics_service = StatisticsService(self.__activity_repository)

    def test_check_upcoming_activity(self):
        activity = Activity(4819, [100], {"year": 2020, "month": 12, "day": 15}, 10, "sumo class")
        self.assertTrue(self.__statistics_service.check_upcoming_activity(activity))
        activity = Activity(6575, [100], {"year": 2019, "month": 12, "day": 15}, 10, "sumo class")
        self.assertFalse(self.__statistics_service.check_upcoming_activity(activity))

    def test_find_busiest_days(self):
        dates_dictionary = self.__statistics_service.find_busiest_days()
        expected_dictionary = {(18, 12, 2020): 1}
        self.assertEqual(dates_dictionary, expected_dictionary)


class PersonServiceTest(unittest.TestCase):
    def setUp(self):
        self.__person_repository = PersonRepository()
        self.__person_validator = Validator()
        self.__undo_stack = UndoStack()
        self.__redo_stack = RedoStack()
        self.__person_repository.person_list = [
            Person(654, "Dan", "645423"),
            Person(143, "Mihai", "534543"),
            Person(876, "Alex", "223543")
        ]
        self.__person_service = PersonService(self.__person_validator, self.__person_repository, self.__undo_stack,
                                              self.__redo_stack)

    def test_service_add_person(self):
        self.assertEqual(len(self.__person_repository), 3)

        self.__person_service.service_add_person(554, "Robert", "654645")

        self.assertEqual(len(self.__person_repository), 4)
        self.assertEqual(self.__person_repository.person_list[-1].id, 554)
        self.assertEqual(self.__person_repository.person_list[-1].name, "Robert")
        self.assertNotEqual(self.__person_repository.person_list[-1].name, "Mihai")
        self.assertEqual(self.__person_repository.person_list[-1].phone_number, "654645")

    def test_service_remove_person(self):
        self.assertEqual(len(self.__person_repository), 3)
        self.assertIsNotNone(self.__person_repository.find_person(876))

        self.__person_service.service_remove_person(876)

        self.assertEqual(len(self.__person_repository), 2)
        self.assertIsNone(self.__person_repository.find_person(876))

        self.assertRaises(PersonServiceError, self.__person_service.service_remove_person, -19)

    def test_service_update_person(self):
        self.__person_service.service_update_person(654, "Dan Oprea", "555555")
        self.assertEqual(self.__person_repository.person_list[0].name, "Dan Oprea")
        self.assertEqual(self.__person_repository.person_list[0].phone_number, "555555")

    def test_service_get_persons_list(self):
        persons_list = self.__person_service.service_get_persons_list()
        expected_list = [Person(654, "Dan", "645423"), Person(143, "Mihai", "534543"), Person(876, "Alex", "223543")]
        self.assertEqual(persons_list, expected_list)

    def test_get_existing_persons_ids(self):
        existing_persons_ids = self.__person_service.get_existing_persons_ids()
        expected_list = [654, 143, 876]
        self.assertEqual(existing_persons_ids, expected_list)

    def test_find_persons_by_name(self):
        searched_name = "Alex"
        searched_persons = self.__person_service.find_persons_by_name(searched_name.lower().strip())
        self.assertEqual(len(searched_persons), 1)
        self.assertEqual(searched_persons, [Person(876, "Alex", "223543")])
        another_searched_name = "John"
        searched_persons = self.__person_service.find_persons_by_name(another_searched_name)
        self.assertEqual(len(searched_persons), 0)

    def test_find_persons_by_phone_number(self):
        searched_phone_number = "54"
        searched_persons = self.__person_service.find_persons_by_phone_number(searched_phone_number.strip())
        self.assertEqual(len(searched_persons), 3)
        self.assertEqual(searched_persons[0], Person(654, "Dan", "645423"))


class ActivityServiceTest(unittest.TestCase):
    def setUp(self):
        self.__activity_validator = Validator()
        self.__person_repository = PersonRepository()
        self.__undo_stack = UndoStack()
        self.__redo_stack = RedoStack()
        self.__person_repository.person_list = [
            Person(654, "Dan", "645423"),
            Person(143, "Mihai", "534543"),
            Person(876, "Alex", "223543")
        ]
        self.__activity_repository = ActivityRepository()
        self.__activity_repository.activities_list = [
            Activity(1145, [654, 143, 876], {"year": 2018, "month": 5, "day": 1}, 23, "go to Shanghai"),
            Activity(9842, [143], {"year": 2017, "month": 12, "day": 23}, 20, "shopping"),
            Activity(1237, [876], {"year": 2019, "month": 8, "day": 15}, 14, "trip to Cluj")
        ]
        self.__activity_service = ActivityService(self.__activity_validator,
                                                  self.__activity_repository,
                                                  self.__person_repository,
                                                  self.__undo_stack,
                                                  self.__redo_stack)

    def test_service_add_activity(self):
        self.assertEqual(len(self.__activity_repository), 3)
        activity_id = 3910
        participants_ids = [654, 143]
        date = {"year": 2018, "month": 10, "day": 18}
        time = 18
        description = "gym"
        self.__activity_service.service_add_activity(activity_id, participants_ids, date, time, description)
        self.assertEqual(len(self.__activity_repository), 4)

        activity_id = 8051
        participants_ids = [905, 111]
        date = {"year": 2001, "month": 12, "day": 5}
        time = 19
        description = "pool"
        self.assertRaises(ActivityServiceError, self.__activity_service.service_add_activity, activity_id,
                          participants_ids, date, time, description)
        self.assertEqual(len(self.__activity_repository), 4)

    def test_service_remove_activity(self):
        self.assertRaises(ActivityValidatorError, self.__activity_service.service_remove_activity, -29)
        self.assertEqual(len(self.__activity_repository), 3)
        self.__activity_service.service_remove_activity(9842)
        self.assertEqual(len(self.__activity_repository), 2)
        self.assertIsNone(self.__activity_repository.find_activity(9842))

    def test_service_get_list_of_activities(self):
        list_of_activities = self.__activity_service.service_get_list_of_activities()
        expected_list = [Activity(1145, [654, 143, 876], {"year": 2018, "month": 5, "day": 1}, 23, "go to Shanghai"),
                         Activity(9842, [143], {"year": 2017, "month": 12, "day": 23}, 20, "shopping"),
                         Activity(1237, [876], {"year": 2019, "month": 8, "day": 15}, 14, "trip to Cluj")
                         ]
        self.assertEqual(list_of_activities, expected_list)

    def test_service_update_activity(self):
        activity_id = 1237
        participants_ids = [654]
        date = {"year": 2020, "month": 8, "day": 12}
        time = 15
        description = "go to beach"
        self.__activity_service.service_update_activity(activity_id, participants_ids, date, time, description)
        updated_activity = self.__activity_repository.activities_list[2]
        self.assertEqual(updated_activity.participants_ids, [654])
        self.assertEqual(updated_activity.date, {"year": 2020, "month": 8, "day": 12})
        self.assertEqual(updated_activity.time, 15)
        self.assertEqual(updated_activity.description, "go to beach")

        activity_id = 1145
        participants_ids = [100, 198]
        date = {"year": 2019, "month": 3, "day": 12}
        time = 21
        description = "basketball"
        self.assertRaises(ActivityServiceError, self.__activity_service.service_update_activity,
                          activity_id, participants_ids, date, time, description)

    def test_find_activities_by_date(self):
        day = 15
        month = 8
        year = 2019
        searched_activities = self.__activity_service.find_activities_by_date(year, month, day)
        self.assertEqual(len(searched_activities), 1)
        self.assertEqual(searched_activities[0],
                         Activity(1237, [876], {"year": 2019, "month": 8, "day": 15}, 14, "trip to Cluj"))
        day = 29
        month = 18
        year = 2020
        self.assertRaises(DateValidatorError, self.__activity_service.find_activities_by_date, year, month, day)

        day = 18
        month = 1
        year = 1999
        searched_activities = self.__activity_service.find_activities_by_date(year, month, day)
        self.assertEqual(len(searched_activities), 0)

    def test_find_activities_by_description(self):
        searched_description = "  tRiP   "
        searched_activities = self.__activity_service.find_activities_by_description(
            searched_description.strip().lower())
        self.assertEqual(len(searched_activities), 1)
        self.assertEqual(searched_activities,
                         [Activity(1237, [876], {"year": 2019, "month": 8, "day": 15}, 14, "trip to Cluj")])
        searched_description = "fjksdfjkhs"
        searched_activities = self.__activity_service.find_activities_by_description(searched_description)
        self.assertEqual(searched_activities, [])

    def test_find_activities_by_participant(self):
        participant_id = 143
        searched_activities = self.__activity_service.find_activities_by_participant(143)
        self.assertEqual(len(searched_activities), 2)
        self.assertTrue(
            Activity(9842, [143], {"year": 2017, "month": 12, "day": 23}, 20, "shopping") in searched_activities)
        self.assertTrue(Activity(1145, [654, 143, 876], {"year": 2018, "month": 5, "day": 1}, 23,
                                 "go to Shanghai") in searched_activities)
        self.assertTrue(
            Activity(1237, [876], {"year": 2019, "month": 8, "day": 15}, 14, "trip to Cluj") not in searched_activities)
        participant_id = -11
        self.assertRaises(ActivityServiceError, self.__activity_service.find_activities_by_participant, participant_id)
        participant_id = 999
        self.assertRaises(ActivityServiceError, self.__activity_service.find_activities_by_participant, participant_id)


class UndoStackTest(unittest.TestCase):
    def setUp(self):
        self.__undo_stack = UndoStack()
        activity = Activity(4324, [431, 321], {"year": 2020, "month": 10, "day": 9}, 18, "idk")
        operation = Operation("add activity", activity, "remove activity", activity.id)
        self.__undo_stack.push(operation)

    def test_push(self):
        activity = Activity(4811, [865], {"year": 2020, "month": 11, "day": 19}, 12, "idk x2")
        another_operation = Operation("remove activity", activity.id, "add activity", activity)
        self.assertEqual(len(self.__undo_stack), 1)
        self.__undo_stack.push(another_operation)
        self.assertEqual(len(self.__undo_stack), 2)
        self.assertEqual(self.__undo_stack.operations[-1], another_operation)

    def test_pop(self):
        self.assertEqual(len(self.__undo_stack), 1)
        operation = self.__undo_stack.pop()
        self.assertEqual(len(self.__undo_stack), 0)
        activity = Activity(4324, [431, 321], {"year": 2020, "month": 10, "day": 9}, 18, "idk")
        self.assertEqual(operation.direct_action, "add activity")
        self.assertEqual(operation.inverse_action, "remove activity")
        self.assertEqual(operation.direct_action_argument, activity)
        self.assertEqual(operation.inverse_action_argument, 4324)
        self.assertRaises(StackError, self.__undo_stack.pop)


class RedoStackTest(unittest.TestCase):
    def setUp(self):
        self.__redo_stack = RedoStack()
        activity = Activity(5832, [100, 200], {"year": 2018, "month": 5, "day": 10}, 5, "testing")
        operation = Operation("add activity", activity, "remove activity", activity.id)
        self.__redo_stack.push(operation)

    def test_push(self):
        activity = Activity(765, [300, 500], {"year": 2019, "month": 5, "day": 10}, 5, "again testing")
        another_operation = Operation("remove activity", activity.id, "add activity", activity)
        self.assertEqual(len(self.__redo_stack), 1)
        self.__redo_stack.push(another_operation)
        self.assertEqual(len(self.__redo_stack), 2)
        self.assertEqual(self.__redo_stack.operations[-1], another_operation)

    def test_pop(self):
        self.assertEqual(len(self.__redo_stack), 1)
        operation = self.__redo_stack.pop()
        self.assertEqual(len(self.__redo_stack), 0)
        activity = Activity(5832, [100, 200], {"year": 2018, "month": 5, "day": 10}, 5, "testing")
        self.assertEqual(operation.direct_action, "add activity")
        self.assertEqual(operation.inverse_action, "remove activity")
        self.assertEqual(operation.direct_action_argument, activity)
        self.assertEqual(operation.inverse_action_argument, 5832)
        self.assertRaises(StackError, self.__redo_stack.pop)

    def test_clear_stack(self):
        self.assertEqual(len(self.__redo_stack), 1)
        self.__redo_stack.clear_stack()
        self.assertEqual(len(self.__redo_stack), 0)
        self.assertTrue(not self.__redo_stack.operations)

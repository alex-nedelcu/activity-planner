import datetime

from EXCEPTIONS.custom_exceptions import StackError, DateValidatorError, ActivityRepositoryError, PersonRepositoryError, \
    ActivityValidatorError, PersonValidatorError, ActivityServiceError, PersonServiceError


class UI:
    def __init__(self, person_service, activity_service, statistics_service, undo_service, redo_service):
        self.__person_service = person_service
        self.__activity_service = activity_service
        self.__statistics_service = statistics_service
        self.__undo_service = undo_service
        self.__redo_service = redo_service
        self.__options_dictionary = {
            "1": self.__ui_list_all_persons,
            "2": self.__ui_add_new_person,
            "3": self.__ui_update_person,
            "4": self.__ui_remove_person,
            "5": self.__ui_list_all_activities,
            "6": self.__ui_add_new_activity,
            "7": self.__ui_update_activity,
            "8": self.__ui_remove_activity,
            "9": self.__ui_choose_search_criteria_for_persons,
            "10": self.__ui_choose_search_criteria_for_activities,
            "11": self.__ui_choose_statistics,
            "12": self.__undo_service.undo,
            "13": self.__redo_service.redo
        }

    def __ui_choose_statistics(self):
        """ Asks the user to pick one of the statistics he/she wants to see """
        print("Please choose one statistic from below:\n"
              "     1. Find all activities for a given date, in the order of their start time\n"
              "     2. Check the availability of the upcoming days\n"
              "     3. Find all the activities performed together with a certain person\n")
        user_choice = input("Type your option: ").strip()
        print("")
        if user_choice == "1":
            self.__ui_search_activities_by_date()
        elif user_choice == "2":
            self.__ui_find_busiest_days()
        elif user_choice == "3":
            self.__ui_find_activities_by_participant()
        else:
            print("Invalid option!\n")
            return

    def __ui_find_busiest_days(self):
        dates_dictionary = self.__statistics_service.find_busiest_days()

        if dates_dictionary == {}:
            print("You have no activities in the upcoming days\n")
        else:
            current_date = datetime.date.today()
            current_day = current_date.day
            current_month = current_date.month
            current_year = current_date.year
            print("The availability of the upcoming days (today's date is {}.{}.{}):".format(current_day,
                                                                                             current_month,
                                                                                             current_year))

        for date, number_of_activities in zip(dates_dictionary.keys(), dates_dictionary.values()):
            day = date[0]
            month = date[1]
            year = date[2]
            if number_of_activities > 1:
                print(
                    f"    {day}.{month}.{year} • {number_of_activities} activities planned • "
                    f"{12 - number_of_activities} hours available")
            elif number_of_activities == 1:
                print(
                    f"    {day}.{month}.{year} • {number_of_activities} activity planned • "
                    f"{12 - number_of_activities} hours available")
        print("")

    def __ui_find_activities_by_participant(self):
        """ Asks the user for the ID of the person for whom the activities he/she took part in are displayed """
        existing_persons_ids = self.__person_service.get_existing_persons_ids()
        searched_participant_id = int(
            input(f"Introduce the ID of one person (you can choose from  the list: {existing_persons_ids})\n   > "))

        searched_activities = self.__activity_service.find_activities_by_participant(searched_participant_id)
        print("")

        if len(searched_activities) == 0:
            print("There is no such an activity!\n")
        else:
            for activity in searched_activities:
                print(activity)
                print("")

    def __ui_choose_search_criteria_for_activities(self):
        """ Asks the user for the criteria he/she wants to find activities by """
        print("By which criteria do you want to search activities?\n"
              "     1. By date\n"
              "     2. By description\n")
        user_choice = input("Type your option: ").strip()
        if user_choice == "1":
            self.__ui_search_activities_by_date()
        elif user_choice == "2":
            self.__ui_search_activities_by_description()
        else:
            print("Invalid option!\n")
            return

    def __ui_search_activities_by_date(self):
        year = int(input("Introduce the year: "))
        month = int(input("Introduce the month: "))
        day = int(input("Introduce the day: "))

        searched_activities = self.__activity_service.find_activities_by_date(year, month, day)

        if len(searched_activities) == 0:
            print("")
            print("There is no activity scheduled for {}.{}.{}!\n".format(day, month, year))
        else:
            print("")
            for activity in searched_activities:
                print(activity)
                print("")

    def __ui_search_activities_by_description(self):
        """ Asks the user for the description of the activity he/she looks for """
        searched_description = input("Introduce the description: ").strip().lower()
        if searched_description == "":
            print("You cannot search activities by an empty description!\n")
            return

        searched_activities = self.__activity_service.find_activities_by_description(searched_description)

        if len(searched_activities) == 0:
            print('There is no activity whose description contains "{}"!\n'.format(searched_description))
        else:
            print("")
            for activity in searched_activities:
                print(activity)
                print("")

    def __ui_choose_search_criteria_for_persons(self):
        """ Asks the user for the criteria he/she wants to find persons by """
        print("By which criteria do you want to search persons?\n"
              "     1. By name\n"
              "     2. By phone number\n")
        user_choice = input("Type your option: ").strip()
        if user_choice == "1":
            self.__ui_search_persons_by_name()
        elif user_choice == "2":
            self.__ui_search_persons_by_phone_number()
        else:
            print("Invalid option!\n")
            return

    def __ui_search_persons_by_name(self):
        """ Asks the user for the name of the person he/she looks for """
        searched_name = input("Introduce the name: ").strip().lower()
        if searched_name == "":
            print("You cannot search persons by an empty name!\n")
            return

        searched_persons = self.__person_service.find_persons_by_name(searched_name)

        if len(searched_persons) == 0:
            print('There is no person whose name contains "{}"!\n'.format(searched_name))
        else:
            print("")
            for person in searched_persons:
                print(person)
            print("")

    def __ui_search_persons_by_phone_number(self):
        """ Asks the user for the phone number of the person he/she looks for """
        searched_phone_number = input("Introduce the phone number: ").strip().lower()
        if searched_phone_number == "":
            print("You cannot search persons by an empty phone number!\n")
            return

        searched_persons = self.__person_service.find_persons_by_phone_number(searched_phone_number)

        if len(searched_persons) == 0:
            print('There is no person whose phone number matches with "{}"!\n'.format(searched_phone_number))
        else:
            print("")
            for person in searched_persons:
                print(person)
            print("")

    def __ui_list_all_activities(self):
        """ Displays all the activities the user has in his/her agenda """
        activities_list = self.__activity_service.service_get_list_of_activities()
        if len(activities_list) == 0:
            print("The list of activities is empty!\n")
        else:
            for activity in activities_list:
                print(activity)
                print("")

    def __ui_add_new_activity(self):
        """
        Asks the user for the activity's input data, then sends the data to the corresponding service method in order
        to add the activity to the agenda.
        """
        activity_id = int(input("Activity ID: "))
        existing_persons_ids = self.__person_service.get_existing_persons_ids()
        string_of_participants_ids = input(
            f"Participants' IDs (you can choose from  the list: {existing_persons_ids})\n   > ")
        list_of_participants_ids = self.__ui_convert_ids_string_to_list(string_of_participants_ids)
        activity_description = input("Describe the activity: ")
        activity_date = {
            "year": int(input("Year: ")),
            "month": int(input("Month: ")),
            "day": int(input("Day: "))
        }
        activity_time = int(input("Time: "))

        self.__activity_service.service_add_activity(activity_id,
                                                     list_of_participants_ids,
                                                     activity_date,
                                                     activity_time,
                                                     activity_description)
        print("Activity successfully added to your agenda!\n")

    @staticmethod
    def __ui_convert_ids_string_to_list(string_of_ids):
        """ e.g. string_of_ids == "192, 491, 540, 932" --> returns [192, 491, 540, 932] (list of integers) """
        if string_of_ids == "":
            return []
        string_of_ids = string_of_ids.strip()
        string_of_ids = string_of_ids.replace(",", " ")

        done = False
        while not done:
            if string_of_ids.find("  ") == -1:
                done = True
            else:
                string_of_ids = string_of_ids.replace("  ", " ")
        list_of_ids = string_of_ids.split(" ")
        for id_index in range(len(list_of_ids)):
            list_of_ids[id_index] = int(list_of_ids[id_index])
        return list_of_ids

    def __ui_remove_activity(self):
        """
        Asks the user for the ID of the activity to be removed, then calls the corresponding service method to
        remove the activity.
        """
        remove_activity_id = int(input("The ID of the activity you want to remove: "))
        self.__activity_service.service_remove_activity(remove_activity_id)
        print("Activity successfully removed from your agenda!\n")

    def __ui_update_activity(self):
        """
        Asks the user for the updates attributes of the activity, and also for its ID, then calls the corresponding
        service method in order to perform the update.
        """
        to_update_activity_id = int(input("The ID of the activity you want to update: "))
        existing_persons_ids = self.__person_service.get_existing_persons_ids()
        string_of_participants_ids = input(
            f"New participants IDs (you can choose from  the list: {existing_persons_ids})\n   > ")
        updated_list_of_participants_ids = self.__ui_convert_ids_string_to_list(string_of_participants_ids)
        updated_activity_description = input("Updated description: ")
        updated_activity_date = {
            "year": int(input("Updated year: ")),
            "month": int(input("Updated month: ")),
            "day": int(input("Updated day: "))
        }
        updated_activity_time = int(input("Updated time: "))
        self.__activity_service.service_update_activity(to_update_activity_id,
                                                        updated_list_of_participants_ids,
                                                        updated_activity_date,
                                                        updated_activity_time,
                                                        updated_activity_description)
        print("Activity successfully updated!\n")

    def __ui_list_all_persons(self):
        """ Displays all the persons the user has in his/her agenda """
        persons_list = self.__person_service.service_get_persons_list()

        if len(persons_list) == 0:
            print("The list of persons is empty!")
        else:
            print("The list of persons in your agenda:")
            for person in persons_list:
                print("    " + str(person))
            print("")

    def __ui_add_new_person(self):
        """
        Asks the user for the new person's input data, then calls the corresponding service method in order to add
        the new person to the agenda.
        """
        person_id = int(input("ID: "))
        person_name = input("Name: ").strip()
        person_phone_number = input("Phone number: ").strip()
        self.__person_service.service_add_person(person_id, person_name, person_phone_number)
        print("Person successfully added to your agenda!\n")

    def __ui_remove_person(self):
        """ Asks the user for an ID, then calls the service method that removes the person having the received ID """
        remove_person_id = int(input("Introduce the ID of the person you want to remove: "))
        self.__person_service.service_remove_person(remove_person_id)
        print("Person successfully removed from your agenda!\n")

    def __ui_update_person(self):
        """
        Asks the user for the updated attributes of a person, and also for his/her ID, then calls the service method
        that performs the update.
        """
        to_update_person_id = int(input("Introduce the ID of the person you want to update: "))
        updated_person_name = input("Updated name: ").strip()
        updated_phone_number = input("Updated phone number: ").strip()
        self.__person_service.service_update_person(to_update_person_id, updated_person_name, updated_phone_number)
        print("Person successfully updated!\n")

    def __print_menu_options(self):
        print(
            "         ❮PERSONS COMMANDS❯ \n"
            "         1. List persons\n"
            "         2. Add a new person\n"
            "         3. Update a person's details\n"
            "         4. Remove a person\n\n"
            "         ❮ACTIVITIES COMMANDS❯ \n"
            "         5. List activities\n"
            "         6. Add a new activity\n"
            "         7. Update an activity's details\n"
            "         8. Remove an activity\n\n"
            "         ❮SEARCH OPTIONS❯ \n"
            "         9. Search persons\n"
            "         10. Search activities\n\n"
            "         ❮STATISTICS❯ \n"
            "         11. Show available statistics\n\n"
            "         ❮EXTRA❯ \n"
            "         12. Undo\n"
            "         13. Redo\n"
            "         x. Exit the menu\n"
        )

    def run(self):
        done = False
        while not done:
            try:
                self.__print_menu_options()
                user_option = input("Choose your option: ")
                print("")
                if user_option in ["0", "exit", "x", "q", "quit"]:
                    done = True
                    print("Goodbye!\n")
                elif user_option in self.__options_dictionary.keys():
                    self.__options_dictionary[user_option]()
                else:
                    print("Invalid option!")
            except ValueError as ve:
                print("INVALID NUMERICAL INPUT: " + str(ve) + "\n")
            except PersonServiceError as pse:
                print("PERSON SERVICE ERROR: " + str(pse))
            except ActivityServiceError as ase:
                print("ACTIVITY SERVICE ERROR: " + str(ase))
            except PersonValidatorError as pve:
                print("VALIDATION ERROR:\n" + str(pve))
            except ActivityValidatorError as ave:
                print("VALIDATION ERROR:\n" + str(ave))
            except PersonRepositoryError as pre:
                print("PERSON REPOSITORY ERROR: " + str(pre))
            except ActivityRepositoryError as are:
                print("ACTIVITY REPOSITORY ERROR: " + str(are))
            except DateValidatorError as dve:
                print(dve)
            except StackError as se:
                print("STACK ERROR: " + str(se))
            print("●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●\n")

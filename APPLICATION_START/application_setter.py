class Settings:
    """
    Class used to instantiate application setters, i.e. objects used to translate the data from the configuration file
    to the application.
    """

    def __init__(self, filename):
        """
        The constructor of an application setter, receiving the file containing the application configurations.
        """
        self.__filename = filename
        self.__settings_dictionary = {}
        self.__read_settings_from_file()

    @property
    def repository_type(self):
        """ Property used to access the repository type chosen by the user """
        return self.__settings_dictionary["repository"]

    @property
    def persons_file(self):
        """ Property used to access the input file for the persons """
        return self.__settings_dictionary["persons"]

    @property
    def activities_file(self):
        """ Property used to access the input file for the activities """
        return self.__settings_dictionary["activities"]

    def __read_settings_from_file(self):
        """
        Reads the configuration of the application and creates a dictionary containing all the needed information.
        """
        with open(self.__filename, mode="r") as settings_file:
            settings_lines = settings_file.readlines()
            for setting_line in settings_lines:
                setting_line = setting_line.strip()
                if setting_line != "":
                    [application_property, value] = setting_line.split("=")
                    application_property = application_property.strip()
                    value = value.strip()
                    self.__settings_dictionary[application_property] = value

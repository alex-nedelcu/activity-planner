from APPLICATION_START.application_coordinator import ApplicationCoordinator
from APPLICATION_START.application_setter import Settings
from EXCEPTIONS.custom_exceptions import ApplicationStartError

if __name__ == '__main__':
    """
    settings.properties should contain:
    repository = inmemory /   textfile         / binaryfile             / json
    persons    =   ""     /   persons.txt      / persons.pickle         / persons.json
    activities =   ""     /   activities.txt   / activities.pickle      / activities.json
    """
    application_setter = Settings("settings.properties")
    application_coordinator = ApplicationCoordinator(application_setter)
    try:
        application_coordinator.start_application()
    except ApplicationStartError as ase:
        print(ase)

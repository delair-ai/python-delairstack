from ..resources_manager_base import ResourcesManagerBase
from ..resource import Resource


class Flights(ResourcesManagerBase):
    _name = 'flights'


class Flight(Resource):
    def __init__(self, **kwargs):
        """Flight resource.

        Args:
            id: Flight identifier.

            name: Flight name.

            survey_date: Survey date (format: ``YYYY-MM-DDTHH:MM:SS.sssZ``).

            project: Project identifier.

            mission: Mission identifier.

            number_of_photos: Number of images in the flight.

            created: Flight creation date.

            user: Flight creation user.

        Returns:
            Flight: A flight resource.
        """
        return super().__init__(**kwargs)

from django.core.management.base import BaseCommand
from core.models import Place

class Command(BaseCommand):
    help = "Load barangay halls and police stations into the database"

    def handle(self, *args, **kwargs):
        barangays = [
            {"name": "Bagumbayan", "address": "Purok 3, Bagumbayan, Taguig City", "latitude": 14.5201, "longitude": 121.0500, "type": "barangay_hall"},
            {"name": "Bambang", "address": "M.L. Quezon St., Bambang, Taguig City", "latitude": 14.5252, "longitude": 121.0456, "type": "barangay_hall"},
            {"name": "Calzada", "address": "3 Ruhale Street, Calzada, Taguig City", "latitude": 14.5284, "longitude": 121.0423, "type": "barangay_hall"},
            {"name": "Central Bicutan", "address": "Sunflower Street, Central Bicutan, Taguig City", "latitude": 14.5295, "longitude": 121.0367, "type": "barangay_hall"},
            {"name": "Central Signal Village", "address": "Ballecer St., Central Signal Village, Taguig City", "latitude": 14.5453, "longitude": 121.0409, "type": "barangay_hall"},
            {"name": "Fort Bonifacio", "address": "Motortown, Market Market, BGC, Taguig City", "latitude": 14.5502, "longitude": 121.0565, "type": "barangay_hall"},
            {"name": "Hagonoy", "address": "M.L. Quezon Street, Hagonoy, Taguig City", "latitude": 14.5367, "longitude": 121.0302, "type": "barangay_hall"},
            {"name": "Ibayo-Tipas", "address": "17 Dr. Natividad St., Ibayo-Tipas, Taguig City", "latitude": 14.5378, "longitude": 121.0285, "type": "barangay_hall"},
            {"name": "Katuparan", "address": "Pag-Asa Avenue, Katuparan, Taguig City", "latitude": 14.5401, "longitude": 121.0322, "type": "barangay_hall"},
            {"name": "Ligid-Tipas", "address": "79 Labo Street, Ligid-Tipas, Taguig City", "latitude": 14.5413, "longitude": 121.0257, "type": "barangay_hall"},
            {"name": "Lower Bicutan", "address": "M.L. Quezon Street, Lower Bicutan, Taguig City", "latitude": 14.5445, "longitude": 121.0344, "type": "barangay_hall"},
            {"name": "Maharlika Village", "address": "1 Maharlika Road, Maharlika Village, Taguig City", "latitude": 14.5467, "longitude": 121.0389, "type": "barangay_hall"},
            {"name": "Napindan", "address": "20 M.L. Quezon Street, Napindan, Taguig City", "latitude": 14.5489, "longitude": 121.0415, "type": "barangay_hall"},
            {"name": "New Lower Bicutan", "address": "P. Cruz Street, New Lower Bicutan, Taguig City", "latitude": 14.5523, "longitude": 121.0441, "type": "barangay_hall"},
            {"name": "North Daang Hari", "address": "Daang Hari Road, North Daang Hari, Taguig City", "latitude": 14.5551, "longitude": 121.0457, "type": "barangay_hall"},
            {"name": "North Signal Village", "address": "Signal Village, Taguig City", "latitude": 14.5582, "longitude": 121.0489, "type": "barangay_hall"},
            {"name": "Palingon-Tipas", "address": "Palingon Street, Palingon-Tipas, Taguig City", "latitude": 14.5312, "longitude": 121.0385, "type": "barangay_hall"},
            {"name": "Pinagsama", "address": "C5 Service Road, Pinagsama, Taguig City", "latitude": 14.5409, "longitude": 121.0364, "type": "barangay_hall"},
            {"name": "San Miguel", "address": "San Miguel Street, San Miguel, Taguig City", "latitude": 14.5334, "longitude": 121.0407, "type": "barangay_hall"},
            {"name": "Santa Ana", "address": "Santa Ana Street, Santa Ana, Taguig City", "latitude": 14.5356, "longitude": 121.0429, "type": "barangay_hall"},
            {"name": "South Daang Hari", "address": "Daang Hari Road, South Daang Hari, Taguig City", "latitude": 14.5539, "longitude": 121.0445, "type": "barangay_hall"},
            {"name": "South Signal Village", "address": "Signal Village, Taguig City", "latitude": 14.5573, "longitude": 121.0478, "type": "barangay_hall"},
            {"name": "Tanyag", "address": "Tanyag Street, Tanyag, Taguig City", "latitude": 14.5517, "longitude": 121.0433, "type": "barangay_hall"},
            {"name": "Tuktukan", "address": "Gen. Luna Street, Tuktukan, Taguig City", "latitude": 14.5223, "longitude": 121.0512, "type": "barangay_hall"},
            {"name": "Upper Bicutan", "address": "1 A. Bonifacio Street, Upper Bicutan, Taguig City", "latitude": 14.5601, "longitude": 121.0503, "type": "barangay_hall"},
            {"name": "Ususan", "address": "1 Tomasa Avenue, Ususan, Taguig City", "latitude": 14.5624, "longitude": 121.0529, "type": "barangay_hall"},
            {"name": "Wawa", "address": "Wawa Street, Wawa, Taguig City", "latitude": 14.5345, "longitude": 121.0298, "type": "barangay_hall"}
        ]

        police_stations = [
            {"name": "Fort Bonifacio Police Sub-station (SS1)", "address": "40th Street corner 9th Avenue, Bonifacio Global City, Fort Bonifacio", "latitude": 14.5537, "longitude": 121.0559, "type": "police_station"},
            {"name": "Western Bicutan Police Sub-station (SS2)", "address": "Radian Street, Arca South, Western Bicutan", "latitude": 14.5298, "longitude": 121.0352, "type": "police_station"},
            {"name": "Pinagsama Police Sub-station (SS3)", "address": "C5 Service Road, Palar Village, Pinagsama", "latitude": 14.5409, "longitude": 121.0364, "type": "police_station"},
            {"name": "STUB Police Sub-station (SS4)", "address": "Tomasa Avenue, Ususan", "latitude": 14.5621, "longitude": 121.0523, "type": "police_station"},
            {"name": "Tipas Police Sub-station (SS5)", "address": "Dr. A. Natividad Street, Ibayo-Tipas", "latitude": 14.5371, "longitude": 121.0280, "type": "police_station"},
            {"name": "Signal Village Police Sub-station (SS6)", "address": "Ballecer Street, Central Signal Village", "latitude": 14.5453, "longitude": 121.0409, "type": "police_station"},
            {"name": "MCU Police Sub-station (SS7)", "address": "A. Bonifacio Avenue corner Maharlika Road, Upper Bicutan", "latitude": 14.5603, "longitude": 121.0505, "type": "police_station"},
            {"name": "Tanyag-Daang Hari Police Sub-station (SS8)", "address": "Mañalac Avenue, Tanyag", "latitude": 14.5527, "longitude": 121.0478, "type": "police_station"},
            {"name": "Hagonoy Police Sub-station (SS9)", "address": "Cadena de Amor Street, Wawa", "latitude": 14.5369, "longitude": 121.0304, "type": "police_station"},
            {"name": "SPD Police Precinct 1 (SS10)", "address": "J.P. Rizal Avenue Extension corner T. Alonzo Street, West Rembo", "latitude": 14.5610, "longitude": 121.0560, "type": "police_station"},
            {"name": "SPD Police Precinct 2 (SS11)", "address": "Anahaw Street, Comembo", "latitude": 14.5540, "longitude": 121.0530, "type": "police_station"},
            {"name": "Bagumbayan-Lower Bicutan Police Sub-station (SS12)", "address": "M.L. Quezon Street, Cayetano Complex, Purok 3, Bagumbayan", "latitude": 14.5201, "longitude": 121.0500, "type": "police_station"}
        ]

        # Convert dictionaries to model instances
        barangay_instances = [Place(**entry) for entry in barangays]
        police_instances = [Place(**entry) for entry in police_stations]

        # Use bulk_create for efficiency
        Place.objects.bulk_create(barangay_instances + police_instances)

        self.stdout.write(self.style.SUCCESS("Dataset inserted successfully!"))

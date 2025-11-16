from faker import Faker
import random
fake = Faker()

my_dict = {
    "city":lambda: fake.city() ,
    "country":lambda: fake.country() ,
    "text":lambda **kwargs: fake.text(**kwargs).replace("\n"," "),
    "latitude":lambda: str(fake.latitude()),
    "longitude":lambda: str(fake.longitude()),
    "podium": lambda : fake.random_int(min=0,max=200),
    "distance": lambda **kwargs: fake.pyfloat(min_value=kwargs.get("min",3), max_value=kwargs.get("max",6), right_digits=2),
    "int": lambda **kwargs: fake.random_int(**kwargs),
    "email":lambda: fake.email(),
    "hostname": lambda: fake.hostname(),
    "image": lambda:fake.image_url(),
    "domain": lambda: fake.domain_name(),
    "mac": lambda: fake.mac_address(),
    "port": lambda: fake.port_number(),
    "currency": lambda:fake.currency(),
    "ip": lambda:fake.ipv4(),
    "number":lambda:fake.phone_number(),
    "driver":lambda **kwargs: extra(**kwargs),
    "team":lambda **kwargs: extra(**kwargs),
    "circuit":lambda **kwargs: extra(**kwargs),
    "weather":lambda **kwargs: extra(**kwargs),
    "tyres":lambda **kwargs: extra(**kwargs),
    "name":lambda: fake.name(),
    "first_name":lambda: fake.first_name(),
    "last_name":lambda: fake.last_name(),
    "username":lambda:fake.user_name(),
    "date":lambda :str(fake.date()),
    "dob": lambda: str(fake.date_of_birth())
}

full_list = [
    {"driver":[
         {'first_name': 'Lando', 'last_name': 'Norris', 'name': 'Lando Norris'},
         {'first_name': 'George', 'last_name': 'Russell', 'name': 'George Russell'},
         {'first_name': 'Max', 'last_name': 'Verstappen', 'name': 'Max Verstappen'},
         {'first_name': 'Esteban', 'last_name': 'Ocon', 'name': 'Esteban Ocon'},
         {'first_name': 'Kimi', 'last_name': 'Antonelli', 'name': 'Kimi Antonelli'},
         {'first_name': 'Alexander', 'last_name': 'Albon', 'name': 'Alexander Albon'},
         {'first_name': 'Oliver', 'last_name': 'Bearman', 'name': 'Oliver Bearman'},
         {'first_name': 'Lance', 'last_name': 'Stroll', 'name': 'Lance Stroll'},
         {'first_name': 'Carlos', 'last_name': 'Sainz', 'name': 'Carlos Sainz'},
         {'first_name': 'Isack', 'last_name': 'Hadjar', 'name': 'Isack Hadjar'},
         {'first_name': 'Liam', 'last_name': 'Lawson', 'name': 'Liam Lawson'},
         {'first_name': 'Jack', 'last_name': 'Doohan', 'name': 'Jack Doohan'},
         {'first_name': 'Gabriel', 'last_name': 'Bortoleto', 'name': 'Gabriel Bortoleto'},
         {'first_name': 'Nico', 'last_name': 'Hulkenberg', 'name': 'Nico Hulkenberg'},
         {'first_name': 'Yuki', 'last_name': 'Tsunoda', 'name': 'Yuki Tsunoda'},
         {'first_name': 'Fernando', 'last_name': 'Alonso', 'name': 'Fernando Alonso'},
         {'first_name': 'Charles', 'last_name': 'Leclerc', 'name': 'Charles Leclerc'},
         {'first_name': 'Lewis', 'last_name': 'Hamilton', 'name': 'Lewis Hamilton'},
         {'first_name': 'Pierre', 'last_name': 'Gasly', 'name': 'Pierre Gasly'}
             ]
     },
    {"team":["McLaren", "Mercedes", "Red Bull Racing", "Haas F1 Team", "Mercedes", "Williams", "Haas F1 Team", "Aston Martin", "Williams", "Racing Bulls", "Red Bull Racing", "Alpine", "Kick Sauber", "Kick Sauber", "Racing Bulls", "Aston Martin", "Ferrari", "Ferrari", "Alpine" ]},
    {"circuit":["Albert Park Grand Prix Circuit", "Sepang International Circuit", "Bahrain International Circuit", "Circuit de Barcelona-Catalunya", "Istanbul Park", "Circuit de Monaco", "Circuit Gilles Villeneuve", "Circuit de Nevers Magny-Cours", "Silverstone Circuit", "Hockenheimring", "Hungaroring", "Valencia Street Circuit", "Circuit de Spa-Francorchamps", "Autodromo Nazionale di Monza", "Marina Bay Street Circuit", "Fuji Speedway", "Shanghai International Circuit", "Indianapolis Motor Speedway", "Autodromo Enzo e Dino Ferrari", "Suzuka Circuit", "Las Vegas Strip Street Circuit", "Yas Marina Circuit", "Circuito de Jerez", "Okayama International Circuit", "Adelaide Street Circuit", "Kyalami", "Donington Park", "Phoenix Street Circuit", "Circuit Paul Ricard", "Korean International Circuit", "Detroit Street Circuit", "Brands Hatch", "Circuit Park Zandvoort", "Zolder", "Dijon-Prenois", "Fair Park", "Long Beach", "Las Vegas Street Circuit", "Jarama", "Watkins Glen", "Scandinavian Raceway", "Mosport International Raceway", "Nivelles-Baulers", "Charade Circuit", "Circuit Mont-Tremblant", "Rouen-Les-Essarts", "Le Mans", "Reims-Gueux", "Prince George Circuit", "Zeltweg", "Aintree", "Circuito da Boavista", "Riverside International Raceway", "AVUS", "Monsanto Park Circuit", "Sebring International Raceway", "Ain Diab", "Pescara Circuit", "Circuit Bremgarten", "Circuit de Pedralbes", "Buddh International Circuit", "Circuit of the Americas", "Red Bull Ring", "Sochi Autodrom", "Baku City Circuit", "Autodromo Internazionale del Mugello", "Jeddah Corniche Circuit", "Losail International Circuit", "Miami International Autodrome"]},
    {"weather":["Dry", "Wet", "Sunny", "Light Rain", "Cloudy", "Foggy"]},
    {"tyres":["Soft", "Medium", "Hard", "Intermediate", "Full Wet"]}
]

def generate_fake_data(schema, num_of_dicts):
    storage =[]
    schema.pop("count", None)#remove count key as not needed
    for l in range(num_of_dicts):#num of data dicts to create
        temp_schema = schema.copy()# copied schema
        for key,values in temp_schema.items():
            if isinstance(values, dict):# if values are dict
                my_type = values.get("type")#get the type
                new_dict = {k:v for k,v in values.items() if k != "type"}#stores arguments in dict
                if my_type in (list(item.keys())[0] for item in full_list):#compares to full list keys
                    temp_schema[key] = my_dict[my_type](values=my_type)
                elif new_dict:
                    temp_schema[key] = my_dict[my_type](**new_dict)
                else:
                    temp_schema[key] = my_dict[my_type]()
            else:
                if values in (list(item.keys())[0] for item in full_list):
                    temp_schema[key] = my_dict[values](values=values)
                else:
                    temp_schema[key] = my_dict[values]()
        #new_temp = linking_words(schema, schema.values(),schema.keys(), temp_schema)
        storage.append(temp_schema)
    return storage

def extra(values):
    x = next(random.choice(f[values]) for f in full_list if values in list(f.keys()))
    return x
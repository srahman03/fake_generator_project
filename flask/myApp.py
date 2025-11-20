
from faker import Faker
import random
import re
import json

fake = Faker()
#Dictionaries to reference faker methods and my own methods
my_dict = {
    "city":lambda: fake.city() ,
    "country":lambda: fake.country() ,
    "text":lambda **kwargs: fake.text(**kwargs).replace("\n"," "),
    "latitude":lambda: str(fake.latitude()),
    "longitude":lambda: str(fake.longitude()),
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
    "dob": lambda: str(fake.date_of_birth()),
    "log": lambda **kwargs: extra(**kwargs),
    "timestamp":lambda: str(fake.iso8601())
}
#Main function to handle schema formats
def generate_fake_data(schema, num_of_copies):
    storage =[] # Will return this to api to be formatted with json
    schema.pop("count", None)#remove count key is not needed
    for l in range(num_of_copies):#num of copies to create
        temp_schema = schema.copy()# copied schema
        for key,values in temp_schema.items():
            with open("data_store.json", "r") as f: # Retrieve file which contains more data types and info
                data = json.load(f) #loads in json format
            if isinstance(values, dict):# Handling different types of schema formats i,e dicts or words
                my_type = values.get("type")#get the data_type
                new_dict = {k:v for k,v in values.items() if k != "type"}#stores arguments in dict
                if my_type in (list(item.keys())[0] for item in data):#compares to prev mentioned file with keys there to match data type
                    temp_schema[key] = my_dict[my_type](values=my_type) #Passes correct arguments to functions
                elif new_dict:
                    temp_schema[key] = my_dict[my_type](**new_dict)
                else:
                    temp_schema[key] = my_dict[my_type]()
            else:
                if values in (list(item.keys())[0] for item in data):
                    temp_schema[key] = my_dict[values](values=values)
                else:
                    temp_schema[key] = my_dict[values]()
        new_temp = linking_words(schema, temp_schema)#Next link username,name,email,first and last name together
        storage.append(new_temp)#adds dict to list
    return storage

#Function to handle extra data_types as specified in file
def extra(values):
    with open("data_store.json", "r") as f:
        data = json.load(f)
        if values == "log":#log formatting
            #log_line = []
            log_string = ""
            for first_layer in data:#loops over list but it is only 1 for now
                if values in list(first_layer.keys()):
                    for k in first_layer[values]:
                        for keys,values in k.items():#enters nested dicts of log key
                            if keys == "date":
                                #log_line.append(my_dict["int"](min=1, max=30))
                                log_string+=str(my_dict["int"](min=1, max=30))+ " "#adds to string or line
                            elif keys == "timestamp":
                                #log_line.append(my_dict["timestamp"]())
                                log_string+=str(my_dict["timestamp"]()) + " "
                            elif keys == "ip":
                                #log_line.append(my_dict["ip"]())
                                log_string+=str(my_dict["ip"]()) + " "
                            elif keys == "pid":
                                x = "Systemd" + " " + str(my_dict["int"](min=300, max=1000))
                                #log_line.append(x)
                                log_string+=x + " "
                            elif keys == "log_term":
                                #log_line.append("Caught" + " " + random.choice(values) + "," + "shutting down")
                                log_string+=("Caught" + " " + random.choice(values)+ "," + "shutting down") + " "
                            else:
                                #log_line.append(random.choice(values))
                                log_string+=(random.choice(values)) + " "
                        #print(log_string)
                    return log_string.strip()
        x = next(random.choice(f[values]) for f in data if values in list(f.keys())) # lazy looping for the other types of data
        return x

def linking_words(my_list, temp):
    my_name_dict ={}
    key_list = []#tracks key and value
    value_list = []

    for i,v in my_list.items():#loop to create my keys and value and my dictionary to use for this function
        if isinstance(v, dict):
            my_type = v.get("type")
        else:
            my_type = v
        if my_type in ["last_name","first_name","name","username","email"]:
            key_list.append(i)
            value_list.append(my_type)
            my_name_dict[my_type] = temp[i]

    if len(my_name_dict) == 0:
        return temp

    name = extract_names(my_name_dict)#variable stored can have value or none
    if name is not None:
        email = create_email(my_name_dict,name)
        username = create_username(my_name_dict,name)
    else:
        email = None
        username = None
    if name is None and email is None and username is None:
        return temp

    for index,key in enumerate(key_list):#function to rewrite new values to temp_schema
        i = value_list[index]
        if i == "name":
            if isinstance(name, tuple):
                last_name, first_name = name
                if i == last_name:
                    temp[key] = last_name
                elif i == first_name:
                    temp[key] = first_name
                elif i == "name":
                    temp[key] = first_name + " " + last_name
        if i == "last_name" or i == "first_name":
            temp[key] = name
        elif i == "username":
            temp[key] = username
        elif i == "email":
            temp[key] = email
    return temp

def extract_names(my_name_dict):
    if "name" in my_name_dict:
        x = re.split("\\s", my_name_dict["name"])
        if ("first_name" in my_name_dict and "last_name" in my_name_dict) or ("first_name" not in my_name_dict and "last_name" not in my_name_dict):
            first_name = x[0]
            last_name = x[1]
            return last_name,first_name
        elif "first_name" in my_name_dict and "last_name" not in my_name_dict:
            first_name = x[0]
            return first_name
        elif "first_name" not in my_name_dict and "last_name" in my_name_dict:
            last_name = x[1]
            return last_name
    return None

def create_email(my_name_dict,name):
    if "email" in my_name_dict and name is not None:
        if isinstance(name,tuple):
            new_email = (
                    name[0][:random.randint(3, len(name[0]))] +
                    random.choice([".", "_", ""]) +
                    name[1][:random.randint(3, len(name[1]))] +
                    str(random.randint(0, 9999)) +
                    "@" +
                    random.choice(["gmail.com", "hotmail.co.uk", "outlook.com"])
            )
            return new_email
        else:
            new_email = (
                    name[0][:random.randint(3, len(name[0]))] +
                    random.choice([".", "_", ""]) +
                    str(random.randint(0, 9999)) +
                    "@" +
                    random.choice(["gmail.com", "hotmail.co.uk", "outlook.com"])
            )
            return new_email
    return None


def create_username(my_name_dict,name):
    if "username" in my_name_dict and name is not None:
        if isinstance(name,tuple):
            new_username = (
                    name[0][:1] +
                    name[0][1:random.randint(2, len(name[0]))] +
                    name[1][:random.randint(0, len(name[1]))] +
                    random.choice("@-_") +
                    str(random.randint(0, 9999))
            )
            return new_username
        else:
            new_username = (
                    name[0][:1] +
                    name[0][1:random.randint(2, len(name[0]))] +
                    random.choice("@-_") +
                    str(random.randint(0, 9999))
            )
            return new_username
    return None







from faker import Faker

import random
fake = Faker()

def validate_input(prompt):
    while True:
        try:
            response = int(input(prompt))
            if response <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a number")
    return response

my_dict = {
    "int": "fake.random_int(min=1, max=9999)",
    "name":"fake.name()" ,
    "first_name":"fake.first_name()",
    "last_name":"fake.last_name()" ,
    "username":"fake.user_name()",
    "address":"fake.address().replace(\"\\n\",\",\")",
    "email":"fake.email()",
    "number":"fake.phone_number()" ,
    "city":"fake.city()" ,
    "country":"fake.country()" ,
    "text":"fake.text().replace(\"\\n\", \" \")" ,
    "log":"fake.text().replace(\"\\n\", \" \")" ,
    "link":"fake.url()" ,
    "date":"str(fake.date())" ,
    "time":"str(fake.time())" ,
    "word":"fake.word()" ,
    "hostname":"fake.hostname()" ,
    "image":"fake.image_url()" ,
    "domain":"fake.domain_name()" ,
    "mac":"fake.mac_address()" ,
    "port":"fake.port_number()" ,
    "char":"fake.country_code()" ,
    "currency":"fake.currency()" ,
    "ip":"fake.ipv4()" ,
    "level": ("ADMIN", "INFO", "WARN", "ERROR","DEBUG","EXTREME","WARNING")
    }



def generate_fake_data(my_list,number):
    """prompt = "Please enter the number of requests you would like to make:"
    req_num = validate_input(prompt)"""
    storage =[]
    if my_list.get("count"):
        del my_list["count"]

    for l in range(number):
        temp =my_list.copy()
        print (f"temp: {temp}")
        for i,v in temp.items():
            searching_words(my_dict, v.lower(), temp, i)
        linking_name(temp,list(temp.values()),list(my_list.keys()),list(my_list.values()))
        storage.append(temp)
    return storage


def searching_words(my_dict,key,my_list,i):
    for l,v in my_dict.items():
        if l == key:
            if key == "level":
                my_list[i] = random.choice(my_dict["level"])
                return my_list
            my_list[i] = eval(v)
            return my_list
    my_list[i] = fake.word()
    return my_list


def linking_name(temp,new_dict_values, old_dict_keys,old_dict_values):
    #print(temp)
    #print(f"Edited values:{new_dict_values}")
    #print(f"keys:{old_dict_keys}")
    #print(f"Old values:{old_dict_values}")

    if not "name" in old_dict_values:
        return temp

    my_list = list(create_name_list(new_dict_values, old_dict_values))
    new_dict = {
        "username": my_list[0],
        "email": my_list[1],
    }
    second_dict={
        "first_name":my_list[2],
        "last_name":my_list[3]
    }
    if "username" in old_dict_values and "email" in old_dict_values and "name" in old_dict_values:
        for i,v in new_dict.items():
            index = old_dict_values.index(i)
            temp[old_dict_keys[index]] = "".join(str(new_dict[i]))

    elif "username" in old_dict_values and "name" in old_dict_values and not "email" in old_dict_values:
        index = old_dict_values.index("username")
        temp[old_dict_keys[index]] = "".join(str(new_dict["username"]))

    elif "email" in old_dict_values and "name" in old_dict_values and not "username" in old_dict_values:
        index = old_dict_values.index("email")
        temp[old_dict_keys[index]] = "".join(str(new_dict["email"]))

    if "first_name" in old_dict_values and "last_name" in old_dict_values:
        for i,v in second_dict.items():
            index = old_dict_values.index(i)
            temp[old_dict_keys[index]] = "".join(str(second_dict[i]))

    elif "first_name" in old_dict_values and not "last_name" in old_dict_values:
        index = old_dict_values.index("first_name")
        temp[old_dict_keys[index]] = "".join(str(second_dict["first_name"]))

    elif not "first_name" in old_dict_values and "last_name" in old_dict_values:
        index = old_dict_values.index("last_name")
        temp[old_dict_keys[index]] = "".join(str(second_dict["last_name"]))

    return temp


def create_name_list(new_dict_values,old_dict_values):
    current_name = new_dict_values[old_dict_values.index("name")].rstrip()
    last_name = current_name.split()[-1]
    first_name = current_name.split()[0]
    new_username = (
            first_name[:1] +
            first_name[1:random.randint(2, len(first_name))] +
            last_name[:random.randint(0, len(last_name))] +
            random.choice("@-_") +
            str(random.randint(0, 9999))
    )
    new_email = (
            first_name[:random.randint(3, len(first_name))] +
            random.choice([".", "_", ""]) +
            last_name[:random.randint(3, len(last_name))] +
            str(random.randint(0, 9999)) +
            "@" +
            random.choice(["gmail.com", "hotmail.co.uk", "outlook.com"])
    )

    return new_username, new_email,first_name,last_name

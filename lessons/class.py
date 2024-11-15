import dataclasses
from uuid import (
    UUID,
    uuid4,
)

@dataclasses.dataclass
class Person:
    """
    Информация о пользователе.

    Attrs:
        login: логин пользователя.
        password: пароль пользователя.
        username: имя пользователя.
        metadata: дополнительные сведения о пользователе.
    """

    login: str
    password: str
    username: str
    metadata: str = ""

class PersonDB:
    _database: dict[UUID, Person]
    _login_registry: set[str]

    _password_length = 10

    _upper_set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    _lower_set = set("abcdefghijklmnopqrstuvwxyz")
    _number_set = set("1234567890")


    def __init__(self, database = None, login_registr = None) -> None:
        """Инициализирует базу данных."""

        self._database = {}
        self._login_registry = set()
    


    def _validate_login(self, person: Person) -> bool:
        """
        Проверка логина на валидность

        Args:
            person: Данные о пользователе, из которых будет браться login

        Return:
            bool - прошел ли логин проверку

        """

        if (person.login not in self._login_registry) and (person.login.isalnum()):
            return True
        else: raise ValueError("Bad password or login")    


    def _validate_password(self, person: Person) -> bool:

        """
        Проверка пароля на валидность

        Args:
            person: Данные о пользователе, из которых будет браться password

        Return:
            bool - прошел ли логин проверку

        """

        password_set = set(person.password)

        if len(person.password) >= 10 and (person.password.isalnum()) and (password_set & self._upper_set and \
            password_set & self._lower_set and  password_set & self._number_set):
            return True
        else:
            raise ValueError("Bad password or login")
        
        
            

    def create_person(self, person: Person, person_id: UUID = None) -> UUID:
        """
        Создает новую запись о пользователе в базе данных или обновляет старую запись.

        Args:
            person: данные о пользователе, которые будут помещены в БД.

        Returns:
            UUID - идентификатор, который будет связан с созданной записью.

        Raises:
            ValueError, если логин или пароль не удовлетворяют требованиям.
        """
    
        if self._validate_password(person) and self._validate_login(person):                    #запись нового пользователя

                uuid_of_person = uuid4()

                self._login_registry.add(person.login)

                self._database[uuid_of_person] = person

                return uuid_of_person
            
        else:  raise ValueError("Bad password or login")                         
            
            
    
    def read_person_info(self, person_id: UUID) -> Person:
        """
        Читает актуальные данные пользователя из базы данных.

        Args:
            person_id: идентификатор пользователя в формате UUID.

        Returns:
            Данные о пользователе, упакованные в структуру Person.

        Raises:
            KeyError, если в базе данных нет пользователя с person_id.
        """

        if person_id in self._database:         #проверка UUID на наличие в database
            return self._database[person_id] 
        else: raise KeyError("Invalid UUID")
    
    def update_person_info(self, person_id: UUID, person_info_new: Person) -> None:
        """
        Обновляет данные о пользователе.

        Args:
            person_id: идентификатор пользователя в формате UUID.
            person_info_new: модель со значениями на обновление. Будут обновлены
                только те поля, чье значение отличается от пустой строки '',
                остальные поля будут оставлены без изменений.

        Raises:
            ValueError, если при обновлении логина или пароля логин или пароль
                не прошли этап валидации.
            KeyError, если в базе данных нет пользователя с person_id.
        """

        if person_id not in self._database:         #проверка UUID на наличие в database
            raise KeyError("Invalid UUID")
        
        
        new_person = dataclasses.replace(self._database[person_id])         #содание копии старой информации о пользователе


        if (person_info_new.login != ""):       #запись нового логина(если он передан)
            if (self._validate_login(person_info_new) and 
             
             ((person_info_new.login not in self._login_registry) or (person_info_new.login == self._database[person_id].login))):
                
                new_person.login = person_info_new.login 
                
            else: 
                raise ValueError("Bad password or login")
            
        
        if (person_info_new.password != ""):            #запись нового пароля(если он передан)
            if (self._validate_password(person_info_new)):
                new_person.password = person_info_new.password
            else: 
                raise ValueError("Bad password or login")

        if (person_info_new.username != ""):            #запись нового ника(если он передан)
            new_person.username = person_info_new.username

        
        if (person_info_new.metadata != ""):            #запись новых метаданных(если они передан)
            new_person.metadata = person_info_new.metadata



        self._login_registry.remove(self._database[person_id].login)                    #перезапись данных о пользователе

        del(self._database[person_id])                  

        self._database[person_id] = new_person

        self._login_registry.add(new_person.login)
        
    
    def delete_person(self, person_id: UUID) -> None:
        """
        Удаляет запись о пользователе.

        Args:
            person_id: идентификатор пользователя в формате UUID.

        Raises:
            KeyError, если в базе данных нет пользователя с person_id.
        """
        if person_id in self._database: #проверка UUID на наличие в database

            self._login_registry.remove(self._database[person_id].login) #удаление логина из login_registry

            del self._database[person_id] #удаление пользователя из database

        else: raise KeyError("Invalid UUID")

#Проверки


#CreatePerson
person1 = Person(
    password="Aa1Bb2Cc3Dd4",
    login="login1",
    username="user#1",
)

database = PersonDB()
person1_id = database.create_person(person1)

assert len(database._database) == 1
assert len(database._login_registry) == 1
assert person1_id in database._database
assert person1.login in database._login_registry
assert database._database[person1_id] == person1

persons_wrong = {
    "no-login": Person(
        password="Aa1Bb2Cc3Dd4",
        login="",
        username="user#2",
    ),
    "existed-login": Person(
        password="Aa1Bb2Cc3Dd4",
        login="login1",
        username="user#2",
    ),
    "too-short-password": Person(
        password="12345",
        login="login2",
        username="user#2",
    ),
    "no-lower": Person(
        password="A1B2C3D4E5F",
        login="login2",
        username="user#2",
    ),
    "no-upper": Person(
        password="a1b2c3d4e5f",
        login="login2",
        username="user#2",
    ),
    "no-digits": Person(
        password="aAbBcCdDeEf",
        login="login2",
        username="user#2",
    ),
    "something wrong": Person(
        password="aaaAAAaa19aaaaaA!",
        login="login52",
        username="pidisyatdva",
    ),
}

for test_name, wrong_person in persons_wrong.items():
    try:
        database.create_person(wrong_person)
        assert False, test_name

    except ValueError:
        assert True
        assert len(database._database) == 1
        assert len(database._login_registry) == 1


#ReadPerson
person = database.read_person_info(person1_id)
assert person1 == person
assert len(database._database) == 1
assert len(database._login_registry) == 1

try:
    fake_id = uuid4()
    person = database.read_person_info(fake_id)
    assert False

except KeyError:
    assert True
    assert len(database._database) == 1
    assert len(database._login_registry) == 1


#UpdatePerson
person2 = Person(
    password="AaBbcC1234Dd",
    login="login2",
    username="user#2"
)
person2_id = database.create_person(person2)
assert len(database._database) == 2
assert len(database._login_registry) == 2
assert person2_id in database._database
assert person2.login in database._login_registry
assert database._database[person2_id] == person2
person2_updated = Person(
    password="abcDEF123456",
    login="LOGIN2",
    username="user#2",
)
person2_update = Person(
    password="abcDEF123456",
    login="LOGIN2",
    username="",
)
database.update_person_info(person2_id, person2_update)
assert len(database._database) == 2
assert len(database._login_registry) == 2
assert person2_id in database._database
assert person2.login not in database._login_registry
assert person2_updated.login in database._login_registry
assert database._database[person2_id] == person2_updated


#DeletePerson
try:
    fake_id = uuid4()
    database.delete_person(fake_id)
    assert False

except KeyError:
    assert True
    assert len(database._database) == 2
    assert len(database._login_registry) == 2

database.delete_person(person2_id)
assert len(database._database) == 1
assert len(database._login_registry) == 1
assert person2_id not in database._database
assert person2_updated.login not in database._login_registry


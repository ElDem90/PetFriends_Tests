from api import *
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_api_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pets_with_valid_data(name='Люся', animal_type='Кошка',
                                     age='13', pet_photo='image/elUHDh_Gixw.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_update_pet_info(name='Мурка', animal_type='Киса', age=12):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
    # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Не найдено ни одно животное")

def test_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_new_pets(auth_key, "Суперкот", "кот", "3", "image/elUHDh_Gixw.jpg")
        _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#Test_1
def test_create_pet_simple(name='Люся', animal_type='Кошка', age=4):
    '''Проверяем возможность упрощенного добавления питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#Test_2
def test_post_new_pet_with_id(pet_photo='image/elUHDh_Gixw.jpg'):
    '''Проверка добавления фото по id питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, 'my_pets')

    status, result = pf.post_new_pet_with_id(auth_key, my_pets['pets'][0]['id'], pet_photo)
    _, my_pets = pf.get_api_pets(auth_key, 'my_pets')

    assert status == 200
    assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']

#Test_3
def test_get_api_key_with_wrong_password(email=valid_email, password='12345'):
    '''Негативный тест попытки получить ключ с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200

#Test_4
def test_get_api_key_with_wrong_email(email='test1012@mail.com', password=valid_password):
    '''Негативный тест попытки получить ключ с неверной почтой'''
    status, result = pf.get_api_key(email, password)
    assert status != 200

#Test_5
def test_create_pet_simple_with_empty_values(name='', animal_type='', age=''):
    '''Проверяем возможность добавления нового питомца с пустыми значениями переменных.
     В случае добавления на сайт, тест считается проваленным'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что питомец добавлен на сайт( тест не пройден)
    assert status == 200
    assert result['name'] == ''
    assert result['animal_type'] == ''
    assert result['age'] == ''

#Test_6
def test_post_pet_with_invalid_animal_type(name='Люся',animal_type = '123 54 89 345', age='13', pet_photo='image/elUHDh_Gixw.jpg'):
    '''Негативный тест. Добавление питомца с название породы, состоящей из чисел
    Тест будет провален, если питомец будет добавлен на сайт'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)

  #  Питомец добавлен (тест провален)
    assert status == 200
    assert result['animal_type'] == animal_type

#Test_7
def test_post_pet_with_special_symbols_in_animal_type(name='Люся', animal_type = '№?&$#%@<>~', age='13', pet_photo='image/elUHDh_Gixw.jpg'):
    '''Негативный тест. Добавление питомца с специальными символами вместо букв в переменной animal_type.
    Тест будет провален, если питомец будет добавлен на сайт.'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)

# Питомец добавлен (тест провален)
    assert status == 200
    assert result['animal_type'] == animal_type

#Test_8
def test_post_pet_negative_age_number(name='Люся', animal_type='Кошка', age='-13', pet_photo='image/elUHDh_Gixw.jpg'):
    '''Негативный тест. Добавление питомца с отрицательным числом в переменной age.
    Тест будет провален, если питомец будет добавлен на сайт'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)

# проверяем, что питомец добавлен на сайт(тест не пройден)
    assert status == 200
    assert result['age'] in age

#Test_9
def test_post_pet_with_text_in_age(name='Лиса', animal_type='Киса', age='абра-кадабра'):
    '''Негативный тест. Добавление питомца с текстом в переменной age.
    Тест будет провален, если питомец будет добавлен на сайт'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    # проверяем, что питомец добавлен на сайт(тест не пройден)
    assert status == 200
    assert result['age'] in age


#Test_10
def test_post_pet_with_empty_values_but_photo(name='', animal_type='', age='', pet_photo='image/elUHDh_Gixw.jpg'):
    '''Негативный тест. Добавление питомца с фото, но с пустыми значениями в переменных.
    Тест будет провален, если питомец будет добавлен на сайт'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_new_pets(auth_key, name, animal_type, age, pet_photo)

# Питомец добавлен (тест провален)
    assert status == 200
    assert result['name'] == ''
    assert result['animal_type'] == ''
    assert result['age'] == ''


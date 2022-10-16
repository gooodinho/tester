import re
import csv
import os
import xml.etree.ElementTree as ET

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import datetime, get_current_timezone
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import Union

from .models import Profile


def check_if_user_with_username_exists(username: str) -> bool:
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


def login_user_handler(request) -> bool:
    """Check if user with given credentials exists. Create session and return True if exists, return False if not."""
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'You are successfully logged in')
        return True
    else:
        if check_if_user_with_username_exists(username):
            messages.warning(request, 'Password is incorrect!')
        else:
            messages.warning(request, 'User with this username does not exist!')
    return False


def logout_handler(request) -> None:
    logout(request)
    messages.success(request, 'You were successfully logouted!')


def create_profile(user: User, avatar: str = None) -> Profile:
    profile = Profile.objects.create(user=user, avatar=avatar)
    profile.save()
    return profile


def save_checked_users(users) -> None:
    for user in users:
        try:
            new_user = User.objects.create(
                username=user['username'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                date_joined=datetime.fromtimestamp(float(user['date_joined']), tz=get_current_timezone()),
                )
            new_user.set_password(user['password'])
            new_user.save()
            new_user.profile.avatar = user['avatar']
            new_user.profile.save()
        except:
            pass


def check_users_from_files(xml_users: list[dict[str, str]], csv_users: list[dict[str, str]]) -> list:
    users = []
    for xml_user in xml_users:
        xml_username = f"{xml_user['first_name'][0].upper()}.{xml_user['last_name'].capitalize()}"
        for csv_user in csv_users:
            if xml_username == csv_user['username']:
                user = {**xml_user, **csv_user}
                users.append(user)
                csv_users.remove(csv_user)
                break
            else:
                continue
    return users


def file_text_filter(text: Union[str, None]) -> Union[str, ValueError]:
    """Raise execption if text is None or there are data in brackets, else return text."""
    if text is None or text == '':
        raise ValueError
    elif re.findall(r'\(.*?\)|\[.*?\]', text):
        raise ValueError
    else:
        return text


def get_xml_users(xml_file: str) -> list[dict[str, str]]:
    """Parse xml file with users data and return list of dictionaries about users."""
    mytree = ET.parse(f'media/{xml_file}')
    myroot = mytree.getroot()
    users = myroot[0].find("users")
    xml_users = []
    for user in users: 
        try:
            first_name = file_text_filter(user.find('first_name').text)
            last_name = file_text_filter(user.find('last_name').text)
            avatar = user.find('avatar').text
            temp_dict = {'first_name': first_name, 'last_name': last_name, 'avatar': avatar}
            xml_users.append(temp_dict)
        except ValueError:
            continue
    return xml_users


def get_csv_users(csv_file: str) -> list[dict[str, str]]:
    """Parse csv file with users data and return list of dictionaries about users."""
    csv_users = []
    with open(f'media/{csv_file}', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                file_text_filter(row['username'])
                file_text_filter(row['password'])
                file_text_filter(row['date_joined'])
                csv_users.append(row)
            except ValueError:
                continue
    return csv_users


def files_handler(csv_file: InMemoryUploadedFile, xml_file: InMemoryUploadedFile) -> None:
    """Save files, parse users data from them, save collected users, delete files."""
    fs = FileSystemStorage()
    saved_csv_file = fs.save(csv_file.name, csv_file)
    saved_xml_file = fs.save(xml_file.name, xml_file)

    csv_users = get_csv_users(saved_csv_file)
    xml_users = get_xml_users(saved_xml_file)

    checked_users = check_users_from_files(xml_users, csv_users)
    save_checked_users(checked_users)

    os.remove(f'media/{saved_csv_file}')
    os.remove(f'media/{saved_xml_file}')


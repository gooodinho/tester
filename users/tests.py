from django.test import TestCase
from .service import *

class FileTextFilterTestCase(TestCase):
    def test_file_text_filter_none(self):
        with self.assertRaises(ValueError):
            file_text_filter(None)
    
    def test_file_text_filter_circle_brakets(self):
        test_data1 = 'User(name)testing'
        test_data2 = '(SELECT * FROM USERS;)'
        with self.assertRaises(ValueError):
            file_text_filter(test_data1)
        with self.assertRaises(ValueError):
            file_text_filter(test_data2)

    def test_file_text_filter_square_brakets(self):
        test_data1 = 'User[name]testing'
        test_data2 = '[SELECT * FROM USERS;]'
        with self.assertRaises(ValueError):
            file_text_filter(test_data1)
        with self.assertRaises(ValueError):
            file_text_filter(test_data2)

    def test_file_text_filter_empty_text(self):
        test_data = ''
        with self.assertRaises(ValueError):
            file_text_filter(test_data)

    def test_file_text_filter_text(self):
        test_data = 'User-name-testing'
        self.assertEqual(test_data, file_text_filter(test_data))


class GetXmlUsersTestcase(TestCase):
    def test_xml_test_file(self):
        xml_file = "test_task.xml"
        xml_users = get_xml_users(xml_file)
        validation_data = [
            {'first_name': 'Anton', 'last_name': 'Mechailov', 'avatar': 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg'}, 
            {'first_name': 'Valerii', 'last_name': 'Jmishenko', 'avatar': 'https://static.boredpanda.com/blog/wp-content/uploads/2017/04/Virrappan2-58f79980ae6fb__880.jpg'}, 
            {'first_name': 'McMarry', 'last_name': 'Stone', 'avatar': 'https://photos.lensculture.com/large/5dd2fa6e-fe8d-469f-959b-46299ced511d.jpg'}
        ]
        self.assertEqual(validation_data, xml_users)


class GetCsvUsersTestcase(TestCase):
    def test_csv_test_file(self):
        csv_file = "test_task.csv"
        csv_users = get_csv_users(csv_file)
        validation_data = [
            {'username': 'M.Steam', 'password': 'ASDf43f#$dsD', 'date_joined': '1638700932'},
            {'username': 'V.Markus', 'password': 'DSA4FSFF54w%$#df', 'date_joined': '1464014817'}, 
            {'username': 'M.Stone', 'password': 'Lkds(*dsdadf', 'date_joined': '1466078973'}, 
            {'username': 'A.Mecman', 'password': 'MKds#$DSd', 'date_joined': '1437646911'}, 
            {'username': 'A.Mechailov', 'password': '35050Dsa', 'date_joined': '1587145969'}, 
            {'username': 'V.Jmishenko', 'password': 'MDsa4wtwefS', 'date_joined': '1391924984'}, 
            {'username': 'H.Snom', 'password': 'DSA3r34tdfsFd', 'date_joined': '1523147737'}, 
            {'username': 'Stus', 'password': 'DAScaf34gDF4%', 'date_joined': '1421161336'}, 
            {'username': 'Mavic', 'password': 'MK43trfDSv', 'date_joined': '1524509311'}, 
            {'username': 'K.hex', 'password': 'mkSArwefd', 'date_joined': '1435699667'}
        ]
        self.assertEqual(validation_data, csv_users)


class CheckUsersFromFilesTestCase(TestCase):
    def test_valid_users(self):
        xml_file = "test_task.xml"
        xml_users = get_xml_users(xml_file)
        csv_file = "test_task.csv"
        csv_users = get_csv_users(csv_file)
        test_users = check_users_from_files(xml_users, csv_users)
        validation_data = [
            {'first_name': 'Anton', 'last_name': 'Mechailov', 'avatar': 'https://mir-s3-cdn-cf.behance.net/project_modules/2800_opt_1/35af6a41332353.57a1ce913e889.jpg', 'username': 'A.Mechailov', 'password': '35050Dsa', 'date_joined': '1587145969'}, 
            {'first_name': 'Valerii', 'last_name': 'Jmishenko', 'avatar': 'https://static.boredpanda.com/blog/wp-content/uploads/2017/04/Virrappan2-58f79980ae6fb__880.jpg', 'username': 'V.Jmishenko', 'password': 'MDsa4wtwefS', 'date_joined': '1391924984'}, 
            {'first_name': 'McMarry', 'last_name': 'Stone', 'avatar': 'https://photos.lensculture.com/large/5dd2fa6e-fe8d-469f-959b-46299ced511d.jpg', 'username': 'M.Stone', 'password': 'Lkds(*dsdadf', 'date_joined': '1466078973'}
        ]
        self.assertEqual(validation_data, test_users)


class SaveCheckedUsersTestCase(TestCase):
    def test_if_saved_users_exists(self):
        xml_file = "test_task.xml"
        xml_users = get_xml_users(xml_file)
        csv_file = "test_task.csv"
        csv_users = get_csv_users(csv_file)
        test_checked_users = check_users_from_files(xml_users, csv_users)
        save_checked_users(test_checked_users)
        for test_user in test_checked_users:
            result = User.objects.filter(username=test_user['username']).exists()
            self.assertEqual(True, result)  


    def test_if_saved_users_have_password(self):
        xml_file = "test_task.xml"
        xml_users = get_xml_users(xml_file)
        csv_file = "test_task.csv"
        csv_users = get_csv_users(csv_file)
        test_checked_users = check_users_from_files(xml_users, csv_users)
        save_checked_users(test_checked_users)
        for test_user in test_checked_users:
            result_user = User.objects.get(username=test_user['username'])
            self.assertEqual(True, result_user.has_usable_password())  


    def test_if_saved_users_have_avatar(self):
        xml_file = "test_task.xml"
        xml_users = get_xml_users(xml_file)
        csv_file = "test_task.csv"
        csv_users = get_csv_users(csv_file)
        test_checked_users = check_users_from_files(xml_users, csv_users)
        save_checked_users(test_checked_users)
        for test_user in test_checked_users:
            result_user = User.objects.get(username=test_user['username'])
            self.assertIsNotNone(result_user.profile.avatar)

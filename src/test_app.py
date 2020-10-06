import unittest
from app import app
class FlaskrTestCase(unittest.TestCase):
      
    def setUp(self):
        pass

    def test_connection(self):
        tester = app.test_client(self)
        response = tester.get('/employees')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_limit(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='limit=1')
        response = str(response.get_json())
        test_response = "[{'department': 5, 'first': 'Patricia', 'id': 1, 'last': 'Diaz', 'manager': None, 'office': 2}]"
        self.assertEqual(response, test_response)


    def test_offset_limit(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='offset=1&limit=1')
        data = str(response.get_json())
        test_data = "[{'department': 5, 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': 1, 'office': 2}]"
        self.assertEqual(data, test_data)


    def test_manager_in_employees(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='expand=manager&limit=1&offset=1')
        data = str(response.get_json())
        test_data = "[{'department': 5, 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': [{'department': 5, 'first': 'Patricia', 'id': 1, 'last': 'Diaz', 'manager': None, 'office': 2}], 'office': 2}]"
        self.assertEqual(data, test_data)

    def test_office_in_employees(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='expand=office&limit=1&offset=1')
        data = str(response.get_json())
        test_data = "[{'department': 5, 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': 1, 'office': {'address': '20 W 34th St', 'city': 'New York', 'country': 'United States', 'id': 2}}]" 
        self.assertEqual(data, test_data)

    def test_department_in_employees(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='limit=1&expand=department&offset=1')
        data = str(response.get_json())
        test_data = "[{'department': [{'id': 5, 'name': 'Inbound Sales', 'superdepartment': 1}], 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': 1, 'office': 2}]"
        self.assertEqual(data, test_data)

    def test_example1(self):        
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='limit=3&expand=department')
        data = str(response.get_json())
        test_data = "[{'department': [{'id': 5, 'name': 'Inbound Sales', 'superdepartment': 1}], 'first': 'Patricia', 'id': 1, 'last': 'Diaz', 'manager': None, 'office': 2}, {'department': [{'id': 5, 'name': 'Inbound Sales', 'superdepartment': 1}], 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': 1, 'office': 2}, {'department': [{'id': 4, 'name': 'Design', 'superdepartment': 3}], 'first': 'Thomas', 'id': 3, 'last': 'Parker', 'manager': None, 'office': None}]"
        self.assertEqual(data, test_data)

    def test_example2(self):
        tester = app.test_client(self)
        response = tester.get('/employees',query_string='limit=3&expand=department.superdepartment&expand=manager.office')
        data = str(response.get_json())
        test_data = "[{'department': [{'id': 5, 'name': 'Inbound Sales', 'superdepartment': [{'id': 1, 'name': 'Sales', 'superdepartment': None}]}], 'first': 'Patricia', 'id': 1, 'last': 'Diaz', 'manager': None, 'office': 2}, {'department': [{'id': 5, 'name': 'Inbound Sales', 'superdepartment': [{'id': 1, 'name': 'Sales', 'superdepartment': None}]}], 'first': 'Daniel', 'id': 2, 'last': 'Smith', 'manager': [{'department': 5, 'first': 'Patricia', 'id': 1, 'last': 'Diaz', 'manager': None, 'office': {'address': '20 W 34th St', 'city': 'New York', 'country': 'United States', 'id': 2}}], 'office': 2}, {'department': [{'id': 4, 'name': 'Design', 'superdepartment': [{'id': 3, 'name': 'Product', 'superdepartment': 1}]}], 'first': 'Thomas', 'id': 3, 'last': 'Parker', 'manager': None, 'office': None}]"
        self.assertEqual(data, test_data)

    def test_example3(self):
        tester = app.test_client(self)
        response = tester.get('/departments/9',query_string='expand=superdepartment.superdepartment')
        data = str(response.get_json())
        test_data = "[{'id': 9, 'name': 'Sales Development', 'superdepartment': [{'id': 6, 'name': 'Outbound Sales', 'superdepartment': [{'id': 1, 'name': 'Sales', 'superdepartment': None}]}]}]"
        self.assertEqual(data, test_data)

if __name__ == '__main__':
    unittest.main()
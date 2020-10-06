import requests
from flask import Flask, jsonify, request
import json
import copy

app = Flask(__name__)

URL_EMPLOYEES = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees'

def add_info(entity, expand_detail_recursive, total_data):
        if expand_detail_recursive: 
            expand = expand_detail_recursive[0]
            if entity[expand]:
                if expand == "department" or expand == "superdepartment" or expand == "manager":
                    entity[expand] = list(filter(lambda x: x['id'] == entity[expand], total_data))
                    expand_detail_recursive.remove(expand)
                    add_info(entity[expand][0],expand_detail_recursive, total_data)
                if expand == "office":
                    entities = []
                    entities.append(entity)
                    expand_office(entities)
        return entity

def expand_office(employees):    
    file_offices = open('../files/offices.json')
    data_offices = json.load(file_offices)
    for employee in employees:       
        if employee["office"]:  
            employee["office"] = data_offices[employee["office"]-1]        
    file_offices.close()
    return employees

def expand_department(employees,expand_detail):
    file_departments = open('../files/departments.json')
    data_departments = json.load(file_departments)
    for employee in employees:         
        if employee["department"]:    
            expand_detail_recursive = expand_detail.copy()
            data_departments_recursive = copy.deepcopy(data_departments)
            add_info(employee, expand_detail_recursive, data_departments_recursive)
    file_departments.close()

def expand_manager(employees,expand_detail):
    total_employee_list = copy.deepcopy(employees)
    set_managers_ids = set()       
    set_employees_ids = set()

    for expand in expand_detail:

        for employee in total_employee_list:
            set_employees_ids.add(employee["id"])
            if employee[expand]:
                set_managers_ids.add(employee[expand])
        set_managers_ids = set_managers_ids.difference(set_employees_ids)
        id_params = ""
        if set_managers_ids:
            for manager_id in set_managers_ids:
                set_employees_ids.add(manager_id)
                id_params += "id=" + str(manager_id) + "&"
            #Quito el ultimo &
            id_params = id_params[0:len(id_params)-1]

            resp = requests.get(url = URL_EMPLOYEES, params = id_params)
            total_employee_list.extend(resp.json())

    
    for employee in employees:  
        expand_detail_recursive = expand_detail.copy()
        total_employee_list_recursive = copy.deepcopy(total_employee_list)
        add_info(employee,expand_detail_recursive,total_employee_list_recursive)

@app.route('/employees', defaults={'employee_id': None})
@app.route('/employees/<int:employee_id>')
def get_employees(employee_id):       

    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    list_expand = request.args.getlist('expand', type = str)

    if limit > 1000:
        limit = 1000

    if employee_id:
        resp = requests.get(url = URL_EMPLOYEES, params = {"id":employee_id})
    else:        
        resp = requests.get(url = URL_EMPLOYEES, params = {"limit":limit, "offset": offset})
    if resp.status_code != 200:
        return jsonify({'message': 'Employee not found'})
    employees = resp.json()

    for expand in list_expand:
        expand_detail = expand.split(".")
        if expand_detail[0] == "manager":   
            expand_manager(employees,expand_detail)

    for expand in list_expand:
        expand_detail = expand.split(".")
        if expand_detail[0] == "department":
            expand_department(employees,expand_detail)
        if expand_detail[0] == "office":
            expand_office(employees)

    return jsonify(employees)

@app.route('/offices', defaults={'office_id': None})
@app.route('/offices/<int:office_id>')
def get_offices(office_id):    

    f = open('../files/offices.json')    

    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)

    data = json.load(f)
    if office_id:
        data = list(filter(lambda x: x['id'] == office_id, data))
    if not data:         
        return jsonify({'message': 'Office not found'})
    
    data = data[offset:offset+limit]

    f.close()
    return jsonify(data)

@app.route('/departments', defaults={'department_id': None})
@app.route('/departments/<int:department_id>')
def get_departments(department_id):    

    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    list_expand = request.args.get('expand', type = str)

    f = open('../files/departments.json')
    data = json.load(f)
    data_departments = copy.deepcopy(data)

    if department_id:
        data_departments = list(filter(lambda x: x['id'] == department_id, data_departments))    
    if not data_departments:         
        return jsonify({'message': 'Department not found'})

    data_departments = data_departments[offset:offset+limit]
    if list_expand:
        expand_detail = list_expand.split(".")

        if expand_detail[0] == "superdepartment":        
            for department in data_departments:         
                if department["superdepartment"]:     
                    expand_detail_recursive = expand_detail.copy()
                    data_departments_recursive = copy.deepcopy(data)
                    add_info(department, expand_detail_recursive, data_departments_recursive)

    f.close()
    return jsonify(data_departments)
    
if __name__ == '__main__':
    app.run(debug=True)
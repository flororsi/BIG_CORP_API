# BIG_CORP_API
##Overview

Your task is to build a web app with a read-only JSON api for 3
resources, employees , departments , offices , you can use any framework or language for
building your app.
Data Sources
The data source for employees is the api:
https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees
it supports two ways of querying, with limit in offset
https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees?
limit=10&offset=20 (gets 21th through 31st record) or querying multiple ids
https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees?
id=3&id=4&id=5 (returns records with id=3, id=4, id=5)
The data source for offices and departments are the files offices.json, departments.json. These
are the entire list of offices and departments, and you can just read all the data for each and keep it
in memory in your app.

#API
Your app should support GET requests to two endpoints (list & detail) for each resource following a
standard REST convention
detail e.g. /employees/1
list e.g. /employees
list should support query limit and offset to support pagination.
limit is the max number of records returned, and offset is the index at which to start.
for instance /employees?limit=10&offset=17 returns the 18th through 27th employee By
default, limit is 100 and the max limit is 1000
in addition, both methods should support a query parameter called expand that lets you expand
data along paths of to-one relationships
There are four relationships that can be expanded,
manager in employees (expands to employees )
office in employees (expands to offices )
department in employees (expands to departments )
superdepartment in departments (expands to departments )

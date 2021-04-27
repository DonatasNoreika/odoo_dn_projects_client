import functools
import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'projects'
USER = 'admin'
PASS = 'admin'
ROOT = f'http://{HOST}:{PORT}/xmlrpc/'

uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print(f"Logged in as {USER} (uid:{uid})")

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

def print_all_projects():
    # Read the projects
    projects = call('dn_projects.project', 'search_read', [], ['name', 'description', 'start_date', 'end_date', 'client_id', 'leader_id'])

    for project in projects:
        print(f"Projektas {project['id']} {project['name']}, nuo: {project['start_date']} iki {project['end_date']} klientas: {project['client_id'][1] if project['client_id'] else None}, vadovas: {project['leader_id'][1] if project['leader_id'] else None}")

def print_all_clients():
    clients = call('res.partner', 'search_read', [], ['name'])
    for client in clients:
        print(client['id'], client['name'])

def print_all_leaders():
    leaders = call('hr.employee', 'search_read', [('leader','=',True)], ['name'])
    for leader in leaders:
        print(leader['id'], leader['name'])

print_all_leaders()

# def create_project():

# 3.create a new session

# course_id = call('openacademy.course', 'search', [('name','ilike','Course 3')])[0]
# instructor_id = call('res.partner', 'search', [('name','ilike','Admin')])[0]
#
# project_id = call('dn_projects.project', 'create', {
#     'name' : 'Naujas projektas',
# })
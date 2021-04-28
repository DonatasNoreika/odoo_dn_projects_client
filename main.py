import functools
import xmlrpc.client
from config import HOST, PORT, DB, USER, PASS
import datetime

ROOT = f'http://{HOST}:{PORT}/xmlrpc/'

uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print(f"Logged in as {USER} (uid:{uid})")

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)


def print_all_projects():
    # Read the projects
    projects = call('dn_projects.project', 'search_read', [],
                    ['name', 'description', 'start_date', 'end_date', 'client_id', 'leader_id'])

    for project in projects:
        print(
            f"Projektas {project['id']} {project['name']}, nuo: {project['start_date']} iki {project['end_date']} klientas: {project['client_id'][1] if project['client_id'] else None}, vadovas: {project['leader_id'][1] if project['leader_id'] else None}")


def print_all_clients():
    clients = call('res.partner', 'search_read', [], ['name'])
    for client in clients:
        print(client['id'], client['name'])


def print_all_leaders():
    leaders = call('hr.employee', 'search_read', [('leader', '=', True)], ['name'])
    for leader in leaders:
        print(leader['id'], leader['name'])


while True:
    pasirinkimas = int(input("""Pasirinkite:
    1 - peržiūrėti projektus
    2 - įrašyti projektą
    3 - išeiti iš programos
    """))
    if pasirinkimas == 1:
        print_all_projects()
    if pasirinkimas == 2:
        name = input("Pavadinimas:\n")
        description = input("Aprašymas:\n")
        start_date = str(datetime.datetime.today())
        trukme = int(input("Trukmė (dienomis)"))
        end_date = str(datetime.date.today() + datetime.timedelta(days=trukme))
        print_all_clients()
        client_id = int(input("Kliento ID:\n"))
        print_all_leaders()
        leader_id = int(input("Vadovo ID:\n"))
        try:
            project_id = call('dn_projects.project', 'create', {
                'name': name,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'client_id': client_id,
                'leader_id': leader_id,
            })
            print(f"Projektas {name} įrašytas")
        except:
            print("Nepavyko įrašyti projekto")
    if pasirinkimas == 3:
        print("Viso gero")
        break

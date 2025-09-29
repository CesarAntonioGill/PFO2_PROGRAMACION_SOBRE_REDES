import requests

BASE_URL = "http://127.0.0.1:5000"

def registrar():
    usuario = input("Ingrese nombre de usuario: ")
    password = input("Ingrese contraseña: ")
    data = {"usuario": usuario, "password": password}
    response = requests.post(f"{BASE_URL}/registro", json=data)
    print(response.json())

def login():
    usuario = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    data = {"usuario": usuario, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    if response.status_code == 200:
        print(response.json()["mensaje"])
        return response.json()["user_id"]
    else:
        print(response.json())
        return None

def crear_tarea(user_id):
    descripcion = input("Ingrese descripción de la tarea: ")
    data = {"descripcion": descripcion, "user_id": user_id}
    response = requests.post(f"{BASE_URL}/tareas", json=data)
    print(response.json())

def listar_tareas(user_id):
    response = requests.get(f"{BASE_URL}/tareas", params={"user_id": user_id})
    if response.status_code == 200:
        tareas = response.json()["tareas"]
        if tareas:
            print("Tareas del usuario:")
            for t in tareas:
                print(f"- [{t['id']}] {t['descripcion']} (Estado: {t['estado']})")
        else:
            print("No hay tareas aún.")
    else:
        print(response.json())

def menu():
    user_id = None
    while True:
        print("\n--- MENU ---")
        print("1. Registrar usuario")
        print("2. Login")
        print("3. Crear tarea")
        print("4. Listar tareas")
        print("5. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            user_id = login()
        elif opcion == "3":
            if user_id:
                crear_tarea(user_id)
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "4":
            if user_id:
                listar_tareas(user_id)
            else:
                print("Debe iniciar sesión primero.")
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()

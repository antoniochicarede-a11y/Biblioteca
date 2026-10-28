"""Punto de unión: crea los componentes y los conecta. Interfaz de consola."""
from datetime import date, timedelta
from catalogo import Catalogo
from socios import Socios
from prestamos import Prestamos

catalogo, socios = Catalogo(), Socios()
prestamos = Prestamos(catalogo, socios)      # inyección de dependencias
for t, a, n in [("Don Quijote", "Cervantes", 3), ("Platero y yo", "J. R. Jiménez", 2),
                ("La sombra del viento", "Ruiz Zafón", 1), ("Rimas y leyendas", "Bécquer", 2)]:
    catalogo.agregar(t, a, n)
hoy = date.today()


def num(msg):
    try:
        return int(input(msg))
    except ValueError:
        raise ValueError("Introduzca un número.")


def menu():
    global hoy
    acciones = {
        "1": lambda: [print(f"  [{l['id']}] {l['titulo']} - {l['autor']} "
                            f"({l['disponibles']}/{l['total']} libres, "
                            f"{len(prestamos.reservas_de(l['id']))} reservas)")
                      for l in catalogo.buscar(input("Título: "))] or print("  Sin resultados"),
        "2": lambda: print("  Alta:", socios.alta(input("Nombre: "))),
        "3": lambda: print("  Préstamo:", prestamos.prestar(num("Id socio: "), num("Id libro: "), hoy)),
        "4": lambda: print("  Retraso (días):", prestamos.devolver(num("Id préstamo: "), hoy)),
        "5": lambda: print("  Posición en cola:", prestamos.reservar(num("Id socio: "), num("Id libro: "), hoy)),
        "6": lambda: [print(" ", p) for p in prestamos.activos()] or print("  Sin préstamos"),
        "7": lambda: [print(" ", s) for s in socios.listar()],
        "8": lambda: globals().__setitem__("hoy", hoy + timedelta(days=num("Avanzar días: "))),
    }
    while True:
        print(f"\n--- Biblioteca (hoy: {hoy}) ---\n1 Buscar  2 Alta socio  3 Prestar  4 Devolver"
              "\n5 Reservar  6 Préstamos  7 Socios  8 Avanzar fecha  0 Salir")
        op = input("> ").strip()
        if op == "0":
            break
        try:
            acciones.get(op, lambda: print("  Opción no válida"))()
        except ValueError as e:
            print("  ✗", e)


if __name__ == "__main__":
    menu()
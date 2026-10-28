"""Componente Socios: altas y sanciones. No conoce a Catalogo ni a Prestamos."""
from datetime import date, timedelta


class Socio:
    """Persona con identidad (id) y estado (sanción)."""

    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre
        self.sancionado_hasta = None


class Socios:
    def __init__(self):
        self._socios = {}
        self._siguiente = 1

    @staticmethod
    def _vista(s):
        return {"id": s.id, "nombre": s.nombre, "sancionado_hasta": s.sancionado_hasta}

    def alta(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        socio = Socio(self._siguiente, nombre)
        self._socios[socio.id] = socio
        self._siguiente += 1
        return self._vista(socio)

    def obtener(self, id_):
        if id_ not in self._socios:
            raise ValueError("Socio inexistente.")
        return self._vista(self._socios[id_])

    def listar(self):
        return [self._vista(s) for s in self._socios.values()]

    def esta_sancionado(self, id_, hoy=None):
        hoy = hoy or date.today()
        hasta = self._socios[self.obtener(id_)["id"]].sancionado_hasta
        return hasta is not None and hoy <= hasta

    def sancionar(self, id_, dias, hoy=None):
        hoy = hoy or date.today()
        self._socios[self.obtener(id_)["id"]].sancionado_hasta = hoy + timedelta(days=dias)
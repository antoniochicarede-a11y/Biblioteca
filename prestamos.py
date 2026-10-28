"""Componente Prestamos: reglas de préstamo y reservas.
Recibe Catalogo y Socios y SOLO usa sus funciones públicas."""
from datetime import date, timedelta

MAX_LIBROS = 2
DIAS_PRESTAMO = 7


class Prestamo:
    """Identidad (id) y estado (devuelto o no)."""

    def __init__(self, id_, socio_id, libro_id, ejemplar_id, inicio):
        self.id = id_
        self.socio_id = socio_id
        self.libro_id = libro_id
        self.ejemplar_id = ejemplar_id
        self.inicio = inicio
        self.vence = inicio + timedelta(days=DIAS_PRESTAMO)
        self.devuelto = None

    def activo(self):
        return self.devuelto is None


class Prestamos:
    def __init__(self, catalogo, socios):
        self._catalogo = catalogo
        self._socios = socios
        self._prestamos = {}
        self._reservas = {}     # libro_id -> [socio_id, ...] por orden de llegada
        self._siguiente = 1

    @staticmethod
    def _vista(p):
        return {"id": p.id, "socio_id": p.socio_id, "libro_id": p.libro_id,
                "ejemplar_id": p.ejemplar_id, "inicio": p.inicio,
                "vence": p.vence, "devuelto": p.devuelto}

    def activos(self, socio_id=None):
        return [self._vista(p) for p in self._prestamos.values()
                if p.activo() and (socio_id is None or p.socio_id == socio_id)]

    def reservas_de(self, libro_id):
        return list(self._reservas.get(libro_id, []))

    def prestar(self, socio_id, libro_id, hoy=None):
        hoy = hoy or date.today()
        self._socios.obtener(socio_id)
        libro = self._catalogo.obtener(libro_id)
        if self._socios.esta_sancionado(socio_id, hoy):
            raise ValueError("Socio sancionado: no puede pedir libros.")
        if len(self.activos(socio_id)) >= MAX_LIBROS:
            raise ValueError(f"Un socio no puede tener más de {MAX_LIBROS} libros a la vez.")
        if libro["disponibles"] == 0:
            raise ValueError("No quedan ejemplares: puede reservarlo.")
        cola = self._reservas.setdefault(libro_id, [])
        if socio_id in cola[:libro["disponibles"]]:
            cola.remove(socio_id)                       # le toca: consume su reserva
        elif len(cola) >= libro["disponibles"]:
            raise ValueError("Los ejemplares libres están reservados por otros socios.")
        ejemplar = self._catalogo.marcar_prestado(libro_id)
        p = Prestamo(self._siguiente, socio_id, libro_id, ejemplar, hoy)
        self._prestamos[p.id] = p
        self._siguiente += 1
        return self._vista(p)

    def reservar(self, socio_id, libro_id, hoy=None):
        hoy = hoy or date.today()
        self._socios.obtener(socio_id)
        libro = self._catalogo.obtener(libro_id)
        if self._socios.esta_sancionado(socio_id, hoy):
            raise ValueError("Socio sancionado: no puede reservar.")
        cola = self._reservas.setdefault(libro_id, [])
        if socio_id in cola:
            raise ValueError("Ya tiene este libro reservado.")
        if libro["disponibles"] > len(cola):
            raise ValueError("Hay ejemplares libres: pídalo directamente.")
        cola.append(socio_id)
        return len(cola)                                # posición en la cola

    def devolver(self, prestamo_id, hoy=None):
        """Devuelve el libro; si hay retraso, sanciona tantos días como de retraso."""
        hoy = hoy or date.today()
        p = self._prestamos.get(prestamo_id)
        if p is None or not p.activo():
            raise ValueError("Préstamo inexistente o ya devuelto.")
        self._catalogo.marcar_devuelto(p.libro_id, p.ejemplar_id)
        p.devuelto = hoy
        retraso = (hoy - p.vence).days
        if retraso > 0:
            self._socios.sancionar(p.socio_id, retraso, hoy)
        return retraso
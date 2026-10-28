"""Componente Catalogo: guarda libros y ejemplares. No conoce a Socios ni a Prestamos."""

DISPONIBLE, PRESTADO = "disponible", "prestado"


class Ejemplar:
    """Copia física de un libro, con identidad y estado propios."""

    def __init__(self, id_):
        self.id = id_
        self.estado = DISPONIBLE


class Libro:
    """Un título con varios ejemplares."""

    def __init__(self, id_, titulo, autor, n_ejemplares):
        self.id = id_
        self.titulo = titulo
        self.autor = autor
        self.ejemplares = [Ejemplar(f"{id_}-{i + 1}") for i in range(n_ejemplares)]

    def libres(self):
        return [e for e in self.ejemplares if e.estado == DISPONIBLE]


class Catalogo:
    def __init__(self):
        self._libros = {}      # privado: nadie fuera de este módulo lo toca
        self._siguiente = 1

    @staticmethod
    def _vista(libro):
        """Copia de solo lectura (dict): así no se filtran los objetos internos."""
        return {"id": libro.id, "titulo": libro.titulo, "autor": libro.autor,
                "total": len(libro.ejemplares), "disponibles": len(libro.libres())}

    def agregar(self, titulo, autor, n_ejemplares=1):
        libro = Libro(self._siguiente, titulo, autor, n_ejemplares)
        self._libros[libro.id] = libro
        self._siguiente += 1
        return self._vista(libro)

    def buscar(self, titulo):
        t = titulo.lower()
        return [self._vista(l) for l in self._libros.values() if t in l.titulo.lower()]

    def obtener(self, id_):
        if id_ not in self._libros:
            raise ValueError("Libro inexistente.")
        return self._vista(self._libros[id_])

    def marcar_prestado(self, id_):
        """Marca un ejemplar libre como prestado y devuelve su id."""
        self.obtener(id_)
        libres = self._libros[id_].libres()
        if not libres:
            raise ValueError("No quedan ejemplares libres.")
        libres[0].estado = PRESTADO
        return libres[0].id

    def marcar_devuelto(self, id_, ejemplar_id):
        self.obtener(id_)
        for e in self._libros[id_].ejemplares:
            if e.id == ejemplar_id:
                e.estado = DISPONIBLE
                return
        raise ValueError("Ejemplar inexistente.")
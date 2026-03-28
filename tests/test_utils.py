import unittest
from app.utils import obtener_id, sanitizar_nombre_archivo, obtener_thumbnail

class TestUtils(unittest.TestCase):
    def test_obtener_id_standard(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(obtener_id(url), "dQw4w9WgXcQ")

    def test_obtener_id_short(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(obtener_id(url), "dQw4w9WgXcQ")

    def test_obtener_id_shorts(self):
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        self.assertEqual(obtener_id(url), "dQw4w9WgXcQ")

    def test_sanitizar_nombre(self):
        nombre = 'Canción / Video? "Genial"'
        esperado = "Canción  Video Genial"
        self.assertEqual(sanitizar_nombre_archivo(nombre), esperado)

    def test_obtener_thumbnail(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        esperado = "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        self.assertEqual(obtener_thumbnail(url), esperado)

if __name__ == "__main__":
    unittest.main()

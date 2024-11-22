import sqlite3
import time
from RPLCD.i2c import CharLCD

class UsuarioClass:
    def __init__(self, db_path, lcd_address=0x27):
        """
        Clase para manejar usuarios y mostrar información en el LCD.
        :param db_path: Ruta a la base de datos SQLite.
        :param lcd_address: Dirección I2C del LCD.
        """
        self.db_path = db_path
        self.lcd = CharLCD('PCF8574', lcd_address)

    def _get_user_data(self, user_name):
        """
        Obtiene datos del usuario desde la base de datos.
        :param user_name: Nombre del usuario reconocido.
        :return: Diccionario con datos del usuario o None si no existe.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT idusuario, nombre, default_azucar FROM usuarios
            WHERE nombre = ?
        """, (user_name,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {"idusuario": user[0], "nombre": user[1], "default_azucar": user[2]}
        return None

    def _get_consumed_sugar(self, user_id):
        """
        Calcula el azúcar consumido por el usuario.
        :param user_id: ID del usuario.
        :return: Cantidad total de azúcar consumida.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(cantidad_servicio) FROM actividad
            WHERE idusuario = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result[0] else 0

    def mostrar_usuario(self, user_name):
        """
        Muestra información del usuario en el LCD.
        :param user_name: Nombre del usuario reconocido.
        """
        user_data = self._get_user_data(user_name)
        if user_data:
            # Usuario reconocido
            consumido = self._get_consumed_sugar(user_data["idusuario"])
            self.lcd.clear()
            self.lcd.write_string(f"Hola, {user_data['nombre']}")
            time.sleep(2)
            self.lcd.clear()
            self.lcd.write_string(f"Azucar: {user_data['default_azucar']}\nConsumido: {consumido}g")
            time.sleep(2)
        else:
            # Usuario desconocido
            self.lcd.clear()
            self.lcd.write_string("USUARIO\nDESCONOCIDO")
            time.sleep(2)
            self.lcd.clear()
            self.lcd.write_string("REGISTRATE")
            time.sleep(2)

    def mostrar_no_rostro(self):
        """
        Muestra mensaje cuando no se detecta un rostro.
        """
        self.lcd.clear()
        self.lcd.write_string("NO SE DETECTO\nROSTRO")
        time.sleep(2)


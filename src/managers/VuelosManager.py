from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from src.tipos import FilaVuelo
from src.managers.DBManager import DBManager
from src.managers.TablaManager import TablaManager
from src.entidades import VueloBase, VueloDesdeDB
from src.querys import OBTENER_VUELO, OBTENER_AVIONES, OBTENER_RUTAS
from src.errores import *

class VuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager):
        super().__init__("vuelos", db_manager)
        self.campos_requeridos = ["fecha_partida_programada", "fecha_arribo_programada", "id_ruta", "id_avion"]
        self.estados_posibles = {
            1: "Programado",
            2: "En vuelo",
            3: "Aterrizado",
            4: "Cancelado"
        }
    
    def registrar_vuelo(self, id_staff: int, vuelo: VueloBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if not self._verificar_fechas(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception(ERROR_FECHAS_INVALIDAS)

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception(ERROR_AVION_Y_RUTA_INVALIDAS)

        costo_operativo_usd: Decimal = self._calcular_costo_operativo_usd(vuelo.id_ruta, vuelo.id_avion)

        precio_venta_usd: Decimal = self._calcular_precio_venta_usd(costo_operativo_usd)

        vuelo.costo_operativo_usd = costo_operativo_usd
        vuelo.precio_venta_usd = precio_venta_usd
        vuelo.id_estado_actual = 1

        super().agregar_fila(id_staff, vuelo)

    def modificar_fechas(self, vuelo: VueloDesdeDB, id_staff: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> None:
        if not super()._verificar_id_a_modificar(vuelo.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)

        if not self._verificar_fechas(fecha_partida_programada, fecha_arribo_programada):
            raise Exception(ERROR_FECHAS_INVALIDAS)
        
        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, fecha_partida_programada, fecha_arribo_programada):
            raise Exception(ERROR_AVION_Y_FECHAS_INVALIDAS)
        
        if vuelo.fecha_partida_programada == fecha_partida_programada and vuelo.fecha_arribo_programada == fecha_arribo_programada:
            return
        
        vuelo.fecha_partida_programada = fecha_partida_programada
        vuelo.fecha_arribo_programada = fecha_arribo_programada

        super().modificar_fila(vuelo, id_staff, "fecha_partida_programada", fecha_partida_programada)
        super().modificar_fila(vuelo, id_staff, "fecha_arribo_programada", fecha_arribo_programada)
    
    def modificar_avion(self, vuelo: VueloDesdeDB, id_staff: int, id_avion: int) -> None:
        if not super()._verificar_id_a_modificar(vuelo.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if not self._verificar_avion(id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception(ERROR_AVION_INVALIDO)
        
        if vuelo.id_avion == id_avion:
            return
        
        vuelo.id_avion = id_avion
        
        super().modificar_fila(vuelo, id_staff, "id_avion", id_avion)

    def modificar_ruta(self, vuelo: VueloDesdeDB, id_staff: int, id_ruta: int) -> None:
        if not super()._verificar_id_a_modificar(vuelo.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if not self._verificar_ruta(vuelo.id_avion, id_ruta):
            raise Exception(ERROR_RUTA_INVALIDA)
        
        if vuelo.id_ruta == id_ruta:
            return
        
        vuelo.id_ruta = id_ruta
        
        super().modificar_fila(vuelo, id_staff, "id_ruta", id_ruta)

    def modificar_estado(self, vuelo: VueloDesdeDB, id_staff: int, id_estado_actual: int) -> None:
        if not super()._verificar_id_a_modificar(vuelo.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if id_estado_actual not in self.estados_posibles:
            raise Exception(ERROR_ESTADO_INVALIDO)
        
        if vuelo.id_estado_actual == id_estado_actual:
            return
        
        if id_estado_actual not in self.estados_posibles:
            raise Exception(ERROR_FORMATO_DATOS)

        if self.estados_posibles[id_estado_actual] == "En vuelo":
            fecha_partida_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(vuelo, id_staff, "fecha_partida_real", fecha_partida_real)
            
        elif self.estados_posibles[id_estado_actual] == "Aterrizado":
            fecha_arribo_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(vuelo, id_staff, "fecha_arribo_real", fecha_arribo_real)
        
        super().modificar_fila(vuelo, id_staff, "id_estado_actual", id_estado_actual)

    def _obtener_aviones_disponibles(self, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> list[int]:
        query = OBTENER_AVIONES

        valores = (fecha_partida_programada, fecha_arribo_programada, id_ruta)

        aviones_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return aviones_disponibles
    
    def _obtener_rutas_disponibles(self, id_avion: int) -> list[int]:
        query = OBTENER_RUTAS

        valores = (id_avion, )

        rutas_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return rutas_disponibles

    def _verificar_fechas(self, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        if fecha_partida_programada < fecha_arribo_programada:
            return True
        
        return False

    def _verificar_avion(self, id_avion: int, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        id_aviones_disponibles: list[int] = self._obtener_aviones_disponibles(id_ruta, fecha_partida_programada, fecha_arribo_programada)

        for id_avion_disponible in id_aviones_disponibles:
            if id_avion_disponible == id_avion:
                return True

        return False
    
    def _verificar_ruta(self, id_avion: int, id_ruta: int) -> bool:
        id_rutas_disponibles: list[int] = self._obtener_rutas_disponibles(id_avion)

        for id_ruta_disponible in id_rutas_disponibles:
            if id_ruta_disponible == id_ruta:
                return True
        
        return False

    def _calcular_costo_operativo_usd(self, id_ruta: int, id_avion: int) -> Decimal:
        query: str = "SELECT duracion_min FROM rutas WHERE id = %s"
        consulta_duracion_min: list[int] = self.db_manager.consultar_columna_unica(query, (id_ruta,))
        
        duracion_min: int = consulta_duracion_min[0]

        query = "SELECT costo_hora_vuelo FROM aviones WHERE id = %s"
        consulta_costo_hora_vuelo: list[int] = self.db_manager.consultar_columna_unica(query, (id_avion,))

        costo_hora_vuelo: int = consulta_costo_hora_vuelo[0]

        costo_operativo_usd: Decimal = ((duracion_min / Decimal("60")) * costo_hora_vuelo).quantize(Decimal("0.01"), ROUND_HALF_UP)

        return costo_operativo_usd
    
    def _calcular_precio_venta_usd(self, costo_operativo_usd: Decimal) -> Decimal:
        precio_venta_usd: Decimal = (costo_operativo_usd * Decimal("1.3")).quantize(Decimal("0.01"), ROUND_HALF_UP)

        return precio_venta_usd

    def _obtener_vuelo(self, id_vuelo: int) -> VueloDesdeDB:
        query = OBTENER_VUELO

        consulta_vuelo: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))
        fila_vuelo: FilaVuelo = consulta_vuelo[0]
        vuelo = VueloDesdeDB(*fila_vuelo)

        return vuelo
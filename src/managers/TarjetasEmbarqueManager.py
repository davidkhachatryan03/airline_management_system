from datetime import datetime
from src.tipos import FilaTarjetaEmbarque
from src.managers.TablaManager import TablaManager
from src.entidades import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.querys import OBTENER_TARJETA_EMBARQUE
from src.errores import *

class TarjetasEmbarqueManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("tarjetas_embarque", db_manager)
        self.campos_requeridos = ["id_venta"]
        self.estados_posibles = {
            1: "Emitida",
            2: "No Show",
            3: "Denegada",
            4: "Embarcado"
        }

    def registrar_tarjeta_embarque(self, id_staff: int, tarjeta_embarque: TarjetaEmbarqueBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        # a futuro este método será eliminado
        if not self._verificar_campos_requeridos(tarjeta_embarque):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")

        super().agregar_fila(id_staff, tarjeta_embarque)
    
    def cambiar_estado(self, tarjeta_embarque: TarjetaEmbarqueDesdeDB, id_staff: int, id_estado_actual: int) -> None:
        if not super()._verificar_id_a_modificar(tarjeta_embarque.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if tarjeta_embarque.id_estado_actual == id_estado_actual:
            return
        
        if id_estado_actual not in self.estados_posibles:
            raise Exception(ERROR_FORMATO_DATOS)
        
        if self.estados_posibles[id_estado_actual] == "Embarcado":
            fecha_embarque: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(tarjeta_embarque, id_staff, "fecha_embarque", fecha_embarque)

        super().modificar_fila(tarjeta_embarque, id_staff, "id_estado_actual", id_estado_actual)

    def _verificar_campos_requeridos(self, tarjeta_embarque: TarjetaEmbarqueBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(tarjeta_embarque, campo) == None:
                return False
        
        return True
    
    def _obtener_tarjeta_embarque(self, id_tarjeta_embarque: int) -> TarjetaEmbarqueDesdeDB:
        query = OBTENER_TARJETA_EMBARQUE
        
        consulta_tarjeta_embarque: list[tuple] = self.db_manager.consultar(query, (id_tarjeta_embarque,))
        fila_tarjeta_embarque: FilaTarjetaEmbarque = consulta_tarjeta_embarque[0]
        tarjeta_embarque = TarjetaEmbarqueDesdeDB(*fila_tarjeta_embarque)

        return tarjeta_embarque
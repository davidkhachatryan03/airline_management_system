from datetime import datetime
from src.tipos import FilaCertificacion
from src.managers.TablaManager import TablaManager
from src.entidades import CertificacionStaffBase, CertificacionStaffDesdeDB
from src.querys import OBTENER_CERTIFICACION
from src.errores import *

class CertificacionesStaffManager(TablaManager):

    def __init__(self, db_manager) -> None:
        super().__init__("certificaciones_staff", db_manager)
        self.campos_requeridos = ["id_staff", "descripcion", "licencia_hasta"]

    def registrar_certificacion(self, id_staff: int, certificacion: CertificacionStaffBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        # a futuro este método será eliminado
        if not self._verificar_campos_requeridos(certificacion):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        super().agregar_fila(id_staff, certificacion)

    def modificar_id_staff(self, certificacion: CertificacionStaffDesdeDB, id_staff_modifica: int, id_staff_nuevo: int) -> None:
        if not super()._verificar_id_a_modificar(certificacion.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff_modifica):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if certificacion.id_staff == id_staff_nuevo:
            return
        
        certificacion.id_staff = id_staff_nuevo
        
        super().modificar_fila(certificacion, id_staff_modifica, "id_staff", id_staff_nuevo)

    def modificar_descripcion(self, certificacion: CertificacionStaffDesdeDB, id_staff: int, descripcion: str) -> None:
        if not super()._verificar_id_a_modificar(certificacion.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if certificacion.id_staff == id_staff:
            return
        
        certificacion.descripcion = descripcion
        
        super().modificar_fila(certificacion, id_staff, "descripcion", descripcion)
        
    def modificar_vencimiento(self, certificacion: CertificacionStaffDesdeDB, id_staff: int, licencia_hasta: datetime) -> None:
        if not super()._verificar_id_a_modificar(certificacion.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if certificacion.licencia_hasta == licencia_hasta:
            return
        
        certificacion.licencia_hasta = licencia_hasta
        
        super().modificar_fila(certificacion, id_staff, "licencia_hasta", licencia_hasta)
    
    def _verificar_campos_requeridos(self, certificacion: CertificacionStaffBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(certificacion, campo) == None:
                return False
        
        return True
    
    def _obtener_certificacion(self, id_certificacion: int) -> CertificacionStaffDesdeDB:
        query = OBTENER_CERTIFICACION
        
        consulta_certificacion: list[FilaCertificacion] = self.db_manager.consultar(query, (id_certificacion,))

        if consulta_certificacion:
            fila_certificacion: FilaCertificacion = consulta_certificacion[0]
            certificacion = CertificacionStaffDesdeDB(*fila_certificacion)
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")
        
        return certificacion
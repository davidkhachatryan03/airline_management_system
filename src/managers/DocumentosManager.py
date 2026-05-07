from datetime import date
from src.tipos import FilaDocumento
from src.managers.TablaManager import TablaManager
from src.entidades import DocumentoBase, DocumentoDesdeDB
from src.querys import OBTENER_DOCUMENTO
from src.errores import *

class DocumentosManager(TablaManager):

    def __init__(self, db_manager) -> None:
        super().__init__("documentos", db_manager)
        self.campos_requeridos = ["num_documento", "fecha_vencimiento", "pais_emision", "id_pasajero", "id_tipo_documento"]

    def registrar_documento(self, id_staff: int, documento: DocumentoBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        # a futuro este método será eliminado
        if not self._verificar_campos_requeridos(documento):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        super().agregar_fila(id_staff, documento)

    def modificar_num_documento(self, documento: DocumentoDesdeDB, id_staff: int, num_documento: str) -> None:
        if not super()._verificar_id_a_modificar(documento.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if documento.num_documento == num_documento:
            return
        
        documento.num_documento = num_documento
        
        super().modificar_fila(documento, id_staff, "num_documento", num_documento)
    
    def modificar_fecha_vencimiento(self, documento: DocumentoDesdeDB, id_staff: int, fecha_vencimiento: date) -> None:
        if not super()._verificar_id_a_modificar(documento.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if documento.fecha_vencimiento == fecha_vencimiento:
            return
        
        documento.fecha_vencimiento = fecha_vencimiento
        
        super().modificar_fila(documento, id_staff, "fecha_vencimiento", fecha_vencimiento)

    def modificar_pais_emision(self, documento: DocumentoDesdeDB, id_staff: int, pais_emision: str) -> None:
        if not super()._verificar_id_a_modificar(documento.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if documento.pais_emision == pais_emision:
            return
        
        documento.pais_emision = pais_emision

        super().modificar_fila(documento, id_staff, "pais_emision", pais_emision) 

    def modificar_pasajero(self, documento: DocumentoDesdeDB, id_staff: int, id_pasajero: int) -> None:
        if not super()._verificar_id_a_modificar(documento.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if documento.id_pasajero == id_pasajero:
            return
        
        documento.id_pasajero = id_pasajero

        super().modificar_fila(documento, id_staff, "id_pasajero", id_pasajero)

    def modificar_tipo_documento(self, documento: DocumentoDesdeDB, id_staff: int, id_tipo_documento: int) -> None:
        if not super()._verificar_id_a_modificar(documento.id):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if documento.id_tipo_documento == id_tipo_documento:
            return
        
        documento.id_tipo_documento = id_tipo_documento

        super().modificar_fila(documento, id_staff, "id_tipo_documento", id_tipo_documento)

    def _obtener_documento(self, id_documento: int) -> DocumentoDesdeDB:
        query = OBTENER_DOCUMENTO

        consulta_documento: list[FilaDocumento] = self.db_manager.consultar(query, (id_documento, ))
        fila_documento: FilaDocumento = consulta_documento[0]
        documento = DocumentoDesdeDB(*fila_documento)

        return documento
    
    def _verificar_campos_requeridos(self, documento: DocumentoBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(documento, campo) == None:
                return False
        
        return True
import pytest
from collections.abc import Callable
from datetime import date
from src.managers import DBManager, DocumentosManager
from src.entidades import DocumentoBase, DocumentoDesdeDB, PasajeroBase, PasajeroDesdeDB
from src.columnas import COLUMNAS_DOCUMENTOS
from src.errores import ERROR_STAFF_INVALIDO, ERROR_FORMATO_DATOS

def test_registrar_documento_correcto(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]]) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    assert ultimo_documento_registrado.num_documento == documento_valido_sin_registrar.num_documento
    assert ultimo_documento_registrado.fecha_vencimiento == documento_valido_sin_registrar.fecha_vencimiento
    assert ultimo_documento_registrado.pais_emision == documento_valido_sin_registrar.pais_emision
    assert ultimo_documento_registrado.id_pasajero == documento_valido_sin_registrar.id_pasajero
    assert ultimo_documento_registrado.id_tipo_documento == documento_valido_sin_registrar.id_tipo_documento

def test_registrar_documento_staff_invalido(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        documentos_manager.registrar_documento(ID_STAFF, ultimo_documento_registrado)

def test_modificar_num_documento_correcto(db_conectada: DBManager, documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_num_documento = "AA1945723"

    documentos_manager.modificar_num_documento(ultimo_documento_registrado, id_staff, nuevo_num_documento)

    ultimo_documento_registrado_modificado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado_modificado.num_documento == nuevo_num_documento
    assert ultimo_documento_registrado_modificado.fecha_vencimiento == ultimo_documento_registrado.fecha_vencimiento
    assert ultimo_documento_registrado_modificado.pais_emision == ultimo_documento_registrado.pais_emision
    assert ultimo_documento_registrado_modificado.id_pasajero == ultimo_documento_registrado.id_pasajero
    assert ultimo_documento_registrado_modificado.id_tipo_documento == ultimo_documento_registrado.id_tipo_documento

def test_modificar_num_documento_invalido(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_num_documento = 1945723

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_num_documento(ultimo_documento_registrado, id_staff, nuevo_num_documento)

def test_modificar_fecha_vencimiento_correcta(db_conectada: DBManager, documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nueva_fecha_vencimiento = date(2060, 1, 1)

    documentos_manager.modificar_fecha_vencimiento(ultimo_documento_registrado, id_staff, nueva_fecha_vencimiento)

    ultimo_documento_registrado_modificado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado_modificado.num_documento == ultimo_documento_registrado.num_documento
    assert ultimo_documento_registrado_modificado.fecha_vencimiento == nueva_fecha_vencimiento
    assert ultimo_documento_registrado_modificado.pais_emision == ultimo_documento_registrado.pais_emision
    assert ultimo_documento_registrado_modificado.id_pasajero == ultimo_documento_registrado.id_pasajero
    assert ultimo_documento_registrado_modificado.id_tipo_documento == ultimo_documento_registrado.id_tipo_documento

def test_modificar_fecha_vencimiento_invalida(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nueva_fecha_vencimiento = None

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_fecha_vencimiento(ultimo_documento_registrado, id_staff, nueva_fecha_vencimiento)

def test_modificar_documento_pais_emision_correcto(db_conectada: DBManager, documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_pais_emision = "FRA" # mi generador de datos no asigna este país a ningún documento, por lo que sé que va a ser distinto siempre.

    documentos_manager.modificar_pais_emision(ultimo_documento_registrado, id_staff, nuevo_pais_emision)

    ultimo_documento_registrado_modificado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado_modificado.num_documento == ultimo_documento_registrado.num_documento
    assert ultimo_documento_registrado_modificado.fecha_vencimiento == ultimo_documento_registrado.fecha_vencimiento
    assert ultimo_documento_registrado_modificado.pais_emision == nuevo_pais_emision
    assert ultimo_documento_registrado_modificado.id_pasajero == ultimo_documento_registrado.id_pasajero
    assert ultimo_documento_registrado_modificado.id_tipo_documento == ultimo_documento_registrado.id_tipo_documento

def test_modificar_documento_pais_emision_invalido(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_pais_emision = None

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_pais_emision(ultimo_documento_registrado, id_staff, nuevo_pais_emision)

def test_modificar_documento_pasajero_correcto(db_conectada: DBManager, documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], pasajero_registrado: Callable[[], tuple[PasajeroBase, PasajeroDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()
    pasajero_valido_sin_registrar, ultimo_pasajero_registrado = pasajero_registrado()

    documentos_manager.modificar_pasajero(ultimo_documento_registrado, id_staff, ultimo_pasajero_registrado.id)

    ultimo_documento_registrado_modificado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado_modificado.num_documento == ultimo_documento_registrado.num_documento
    assert ultimo_documento_registrado_modificado.fecha_vencimiento == ultimo_documento_registrado.fecha_vencimiento
    assert ultimo_documento_registrado_modificado.pais_emision == ultimo_documento_registrado.pais_emision
    assert ultimo_documento_registrado_modificado.id_pasajero == ultimo_pasajero_registrado.id
    assert ultimo_documento_registrado_modificado.id_tipo_documento == ultimo_documento_registrado.id_tipo_documento

def test_modificar_documento_pasajero_invalido(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_pasajero = None

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_pasajero(ultimo_documento_registrado, id_staff, nuevo_pasajero)

def test_modificar_tipo_documento_correcto(db_conectada: DBManager, documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_tipo_documento = 1

    documentos_manager.modificar_tipo_documento(ultimo_documento_registrado, id_staff, nuevo_tipo_documento)

    ultimo_documento_registrado_modificado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado_modificado.num_documento == ultimo_documento_registrado.num_documento
    assert ultimo_documento_registrado_modificado.fecha_vencimiento == ultimo_documento_registrado.fecha_vencimiento
    assert ultimo_documento_registrado_modificado.pais_emision == ultimo_documento_registrado.pais_emision
    assert ultimo_documento_registrado_modificado.id_pasajero == ultimo_documento_registrado.id_pasajero
    assert ultimo_documento_registrado_modificado.id_tipo_documento == nuevo_tipo_documento

def test_modificar_tipo_documento_invalido(documento_registrado: Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]], documentos_manager: DocumentosManager, id_staff: int) -> None:
    documento_valido_sin_registrar, ultimo_documento_registrado = documento_registrado()

    nuevo_tipo_documento = None

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_tipo_documento(ultimo_documento_registrado, id_staff, nuevo_tipo_documento)
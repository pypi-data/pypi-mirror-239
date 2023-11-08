from datetime import datetime
import boto3
import math
import re

TEXTRACT_DATA = None

TEXTRACT_ALL_DATA_FRONT = None
TEXTRACT_DATA_FRONT = None

TEXTRACT_ALL_DATA_BACK = None
TEXTRACT_DATA_BACK = None

TEXTRACT = None
DPI_DATA = {}


def client(region_name='us-east-1', **kwargs):
    # Configuramos las credenciales
    global TEXTRACT
    TEXTRACT = boto3.client('textract', region_name=region_name, **kwargs)


def analyze_dpi(dpi_path_front = None,dpi_path_back= None, json_path=None):
    global TEXTRACT_DATA
    global TEXTRACT_ALL_DATA_FRONT
    global TEXTRACT_DATA_FRONT
    global TEXTRACT_ALL_DATA_BACK
    global TEXTRACT_DATA_BACK
    global TEXTRACT
    global DPI_DATA

    # json_folder_path = 'json/textract'
    # current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_filename = f'{json_folder_path}/ddt_{current_datetime}.json'

    # Guardar la respuesta en un archivo JSON
    # if not os.path.exists(json_folder_path):
    #     os.makedirs(json_folder_path)

    # with open(output_filename, 'w') as jsonfile:
    #     json.dump(response, jsonfile, indent=2)

    if dpi_path_front or dpi_read_data_back:
        TEXTRACT_DATA_FRONT = None
        TEXTRACT_ALL_DATA_FRONT = None
        TEXTRACT_DATA = None
        TEXTRACT_ALL_DATA_BACK = None
        TEXTRACT_DATA_BACK = None
        DPI_DATA = {}
        
        if dpi_path_front:
            # Leemos la imagen local en forma de bytes
            with open(dpi_path_front, 'rb') as document:
                image_bytes = document.read()

            # Llamamos a DetectDocumentText
            TEXTRACT_DATA = TEXTRACT.detect_document_text(Document={'Bytes': image_bytes})

            # Procesamos la respuesta para obtener el texto detectado
            TEXTRACT_ALL_DATA_FRONT = TEXTRACT_DATA
            TEXTRACT_DATA_FRONT = dpi_read_data_front()
            
        if dpi_path_back:
            # Leemos la imagen local en forma de bytes
            with open(dpi_path_back, 'rb') as document:
                image_bytes = document.read()

            # Llamamos a DetectDocumentText
            TEXTRACT_DATA = TEXTRACT.detect_document_text(Document={'Bytes': image_bytes})

            # Procesamos la respuesta para obtener el texto detectado
            TEXTRACT_ALL_DATA_BACK = TEXTRACT_DATA
            TEXTRACT_DATA_BACK = dpi_read_data_back()
            
    return DPI_DATA


def dpi_read_data_front():

    global DPI_DATA,TEXTRACT_DATA

    # Busqueda CUI
    cui_re = r'\d{4} \d{5} \d{4}'
    cui_block = get_block_by_regex(cui_re)
    if not cui_block:
        print('CUI no encontrado')
        return None
    DPI_DATA['CUI'] = cui_block["Text"]

    # Busqueda PAIS DE NACIMIENTO
    birth_country_re = r'^PAIS DE|^LUGAR DE'
    birth_country, block = search_by_reference(birth_country_re, 4)
    DPI_DATA['PAIS DE NACIMIENTO'] = birth_country

    # Busqueda FECHA DE NACIMIENTO
    birth_date_re = r'^FECHA DE'
    birth_date, block = search_by_reference(birth_date_re, 4)
    DPI_DATA['FECHA DE NACIMIENTO'] = birth_date

    # Busqueda SEXO
    sex_re = r'(M[ÁA]SCULINO|FEMENINO)'
    sex_re = r'^SEXO'
    sex, block = search_by_reference(sex_re, 4)
    DPI_DATA['SEXO'] = sex

    # Busqueda NACIONALIDAD
    nationality_re = r'^NACIONALIDAD'
    nationality, block = search_by_reference(nationality_re, 4)
    DPI_DATA['NACIONALIDAD'] = nationality

    # Busqueda APELLIDO
    last_name_re = r'^APELLIDO'
    last_name, block = search_by_reference(last_name_re, 7)
    DPI_DATA['APELLIDOS'] = last_name

    # Busqueda NOMBRE
    name_re = r'^NOMBRE'
    name, block = search_by_reference(name_re, 8)
    DPI_DATA['NOMBRES'] = name

    # Busqueda EMISIÓN
    issuance_re = r'\d{2}[A-Z]{3}\d{4}'
    issuance_block = get_block_by_regex(issuance_re)
    if not issuance_block:
        DPI_DATA['EMISION'] = ""
    else:
        DPI_DATA['EMISION'] = issuance_block["Text"]

    # Busqueda VERSION
    version_re = r'\d{3}'
    version_block = get_block_by_regex(version_re)
    if not version_block:
        DPI_DATA['VERSION'] = ""
    else:
        DPI_DATA['VERSION'] = version_block["Text"]

    return TEXTRACT_DATA

def dpi_read_data_back():

    global DPI_DATA, TEXTRACT_DATA

    # # Busqueda RENAP
    # cui_re = r'\d{4} \d{5} \d{4}'
    # cui_block = get_block_by_regex(cui_re)
    # if not cui_block:
    #     print('CUI no encontrado')
    #     return None
    # DPI_DATA['CUI'] = cui_block["Text"]

    # Busqueda FECHA DE VENCIMIENTO
    exp_re = r'^FECHA DE|^VENCIMIENTO|^EXPI'
    exp, block = search_by_reference(exp_re, 4)
    DPI_DATA['EXPIRACION'] = exp
    

    # Busqueda ESTADO CIVIL
    status_re = r'^ESTADO CIVIL'
    status, block = search_by_reference(status_re, 4)
    DPI_DATA['ESTADO CIVIL'] = status

    # Busqueda NÚMERO DE SERIE
    serie_re = r'^NUMERO DE|NÚMERO DE'
    serie, block = search_by_reference(serie_re, 4)
    DPI_DATA['SERIE'] = serie
    
    # Busqueda COMUNIDAD
    linguistic_community_re = r'^COMUNIDAD'
    linguistic_community, block = search_by_reference(linguistic_community_re, 4)
    DPI_DATA['COMUNIDAD'] = linguistic_community
    
    # Busqueda PUEBLO
    ethnic_group_re = r'^PUEBLO'
    ethnic_group, block = search_by_reference(ethnic_group_re, 4)
    DPI_DATA['PUEBLO'] = ethnic_group

    # Busqueda VECINDAD
    hood_re = r'^VECINDAD'
    hood, block = search_by_reference(hood_re, 6,4)
    DPI_DATA['VECINDAD'] = hood

    # Busqueda LUGAR DE NACIMIENTO
    birthplace_re = r'^LUGAR DE'
    birthplace, block = search_by_reference(birthplace_re, 6,3)
    DPI_DATA['LUGAR DE NACIMIENTO'] = birthplace


    return TEXTRACT_DATA

#
# Por posición
#


def triangle_area(p1, p2, p3):
    # Calcula el área de un triángulo formado por tres puntos (vértices)
    return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2.0)


def is_inside_area(vertices, point_Q):
    # Verifica si el punto Q está dentro del área definida por los vértices
    A = triangle_area(vertices[0], vertices[1], point_Q) + \
        triangle_area(vertices[1], vertices[2], point_Q) + \
        triangle_area(vertices[2], vertices[3], point_Q) + \
        triangle_area(vertices[3], vertices[0], point_Q)

    total_area = triangle_area(
        vertices[0], vertices[1], vertices[2]) + triangle_area(vertices[2], vertices[3], vertices[0])

    # Se utiliza una tolerancia pequeña para evitar errores de punto flotante
    return abs(A - total_area) < 1e-15


def contain_polygon(area, polygon):

    # Convertir los datos del polígono a una lista de vértices
    vertices_area = area

    vertices_polygon = [(point["X"], point["Y"]) for point in polygon]

    # Verificar si todos los puntos de polygon están dentro del área del primer polígono
    all_inside = all(is_inside_area(vertices_area, point)
                     for point in vertices_polygon)

    return all_inside


def get_block_by_regex(reg_ex, BlockType=None):
    global TEXTRACT_DATA
    # Busca el bloque que coincida con la re y lo elimina de la lista
    for i, bloque in enumerate(TEXTRACT_DATA['Blocks']):
        if bloque['BlockType'] == 'LINE':
            texto = bloque['Text']
            coincide = re.search(reg_ex, texto)
            if coincide:
                # Elimina el bloque encontrado de la lista
                del TEXTRACT_DATA['Blocks'][i]
                return bloque
    # Si no encuentra coincidencia
    return None


def search_by_reference(ref_re, target_height, target_len = None):
    
    ref_block = get_block_by_regex(ref_re)

    if not ref_block:
        print(f'Referencia no encontrada: {ref_re}')
        return None, None
    else:
        ref_polygon = ref_block['Geometry']['Polygon']

    # Convertir los datos del polígono a una lista de vértices
    vertices = [(point["X"], point["Y"]) for point in ref_polygon]

    # Calcula el vectores
    vector1 = (ref_polygon[1]["X"] - ref_polygon[0]["X"],
               ref_polygon[1]["Y"] - ref_polygon[0]["Y"])
    vector2 = (ref_polygon[2]["X"] - ref_polygon[1]["X"],
               ref_polygon[2]["Y"] - ref_polygon[1]["Y"])

    # Calcula el ángulo en radianes con respecto al eje x positivo
    angulo_radianes = math.atan2(vector1[1], vector1[0])

    # Calcula el ángulo en radianes con respecto al eje x positivo
    angulo_radianes2 = math.atan2(vector2[1], vector2[0])

    # Calculo de la magnitud de un vector
    magnitud = math.sqrt(
        (ref_polygon[2]["X"] - ref_polygon[1]["X"])**2 + (ref_polygon[2]["Y"] - ref_polygon[1]["Y"])**2)
    magnitud2 = math.sqrt(
        (ref_polygon[1]["X"] - ref_polygon[0]["X"])**2 + (ref_polygon[1]["Y"] - ref_polygon[0]["Y"])**2)
    
    if not target_len:
        target_len = 0.25
    else:
        target_len = magnitud2 * target_len

    # Creación de los vértices del área para buscar dato objetivo
    p1 = final_point(vertices[-1], magnitud, angulo_radianes+math.pi)
    p2 = final_point(p1, target_len, angulo_radianes)
    p3 = final_point(p2, target_height*magnitud, angulo_radianes2)
    p4 = final_point(p3, target_len, angulo_radianes+math.pi)

    name_area = [p1, p2, p3, p4]

    values = []
    TEXTRACT_DATA
    blocks_to_keep = []

    for block in TEXTRACT_DATA['Blocks']:
        if block['BlockType'] == 'LINE':
            text = block['Text']
            actual_polygon = block['Geometry']['Polygon']
            if contain_polygon(name_area, actual_polygon):
                values.append(text)
            else:
                blocks_to_keep.append(block)
        else:
            blocks_to_keep.append(block)

    TEXTRACT_DATA['Blocks'] = blocks_to_keep
    value = " ".join(values)
    return value, ref_block



def final_point(point, p_length, direction):
    # Ecuentra el punto final dado un punto de inicio y una dirección

    # Punto inicial del vector (x0, y0)
    x0 = point[0]
    y0 = point[1]

    # Longitud del vector
    longitud = p_length

    # Calcular el punto final
    x_final = x0 + longitud * math.cos(direction)
    y_final = y0 + longitud * math.sin(direction)

    return (x_final, y_final)

#
#  Valores indivividuales
#


def cui():
    global DPI_DATA
    try:
        return DPI_DATA['CUI']
    except:
        print("An exception occurred")
        return "Algo salió mal"


def birth_country():
    global DPI_DATA
    try:
        return DPI_DATA['PAIS DE NACIMIENTO']
    except:
        print("An exception occurred")
        return "Algo salió mal"


def birth_date():
    global DPI_DATA
    try:
        return DPI_DATA['FECHA DE NACIMIENTO']
    except:
        print("An exception occurred")
        return "Algo salió mal"


def sex():
    global DPI_DATA
    try:
        return DPI_DATA['SEXO']
    except:
        print("An exception occurred")
        return "Algo salió mal"


def nationality():
    global DPI_DATA
    return DPI_DATA['NACIONALIDAD']


def name():
    global DPI_DATA
    return DPI_DATA['NOMBRES']


def last_name():
    global DPI_DATA
    return DPI_DATA['APELLIDOS']


def issue_date():
    global DPI_DATA
    return DPI_DATA['EMISION']


def dpi_version():
    global DPI_DATA
    return DPI_DATA['VERSION']

# Créditos


def pp():
    msj = "dpi-textrac por Luis Manuel"
    print(msj)
    return msj


print("-> Fin de importacion\n")

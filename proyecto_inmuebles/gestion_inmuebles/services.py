from django.db import connection


def listar_inmuebles():

    consulta = """
        SELECT
            inmuebles.nombre,
            inmuebles.descripcion,
            comuna.nombre
        FROM gestion_inmuebles_inmueble AS inmuebles
        INNER JOIN gestion_inmuebles_comuna AS comuna
            ON comuna.id = inmuebles.comuna_id
        ORDER BY comuna.nombre, inmuebles.nombre
    """

    with connection.cursor() as cursor:
        cursor.execute(consulta)
        resultados = cursor.fetchall()

    with open("inmuebles_por_comuna.txt", "w", encoding="utf-8") as archivo:

        comuna_actual = ""

        for nombre, descripcion, comuna in resultados:

            if comuna != comuna_actual:
                archivo.write(f"\nCOMUNA: {comuna}\n")
                archivo.write("-" * 40 + "\n")

                comuna_actual = comuna

            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"Descripción: {descripcion}\n\n")

    return resultados
    

def listar_inmuebles_por_region():

    consulta = """
        SELECT
            inmuebles.nombre,
            inmuebles.descripcion,
            region.nombre
        FROM gestion_inmuebles_inmueble AS inmuebles
        INNER JOIN gestion_inmuebles_comuna AS comuna
            ON comuna.id = inmuebles.comuna_id
        INNER JOIN gestion_inmuebles_region AS region
            ON region.id = comuna.region_id
        ORDER BY region.nombre, inmuebles.nombre
    """

    with connection.cursor() as cursor:
        cursor.execute(consulta)
        resultados = cursor.fetchall()

    with open("inmuebles_por_region.txt", "w", encoding="utf-8") as archivo:

        region_actual = ""

        for nombre, descripcion, region in resultados:

            if region != region_actual:
                archivo.write(f"\nREGIÓN: {region}\n")
                archivo.write("-" * 40 + "\n")

                region_actual = region

            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"Descripción: {descripcion}\n\n")

    return resultados
    

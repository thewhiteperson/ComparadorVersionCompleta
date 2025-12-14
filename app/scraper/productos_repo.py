from app.connection.mongo import productos_collection


def guardar_productos(productos: list):
    for producto in productos:
        filtro = {
            "marca": producto["marca"],
            "linea": producto["linea"],
            "modelo": producto["modelo"],
            "tienda": producto["tienda"]
        }

        update = {
            "$set": producto
        }

        productos_collection.update_one(
            filtro,
            update,
            upsert=True
        )

def buscar_productos(texto: str):
    regex = {"$regex": texto, "$options": "i"}  # i = ignore case

    query = {
        "$or": [
            {"marca": regex},
            {"modelo": regex},
            {"linea": regex},
            {"tienda": regex}
        ]
    }

    resultados = list(productos_collection.find(query))

    return resultados

def buscar_modelos_unicos(texto: str):
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"marca": {"$regex": texto, "$options": "i"}},
                    {"modelo": {"$regex": texto, "$options": "i"}},
                    {"linea": {"$regex": texto, "$options": "i"}}
                ]
            }
        },
        {
            "$group": {
                "_id": "$modelo",
                "modelo": {"$first": "$modelo"},
                "marca": {"$first": "$marca"},
                "linea": {"$first": "$linea"},
                "imagen": {"$first": "$imagen"}
            }
        },
        {
            "$sort": {"modelo": 1}
        }
    ]

    return list(productos_collection.aggregate(pipeline))
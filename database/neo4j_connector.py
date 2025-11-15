"""
Conector Neo4j - Sistema de Recomendación de Viviendas
Implementa la conexión y operaciones con la base de datos Neo4j.
"""

from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from models.frame_models import PropertyFrame, UserFrame, AmenityFrame, Address, AmenityType
from fuzzy.transport_evaluation import TransportType
import logging
import warnings

# Silenciar warnings de Neo4j
warnings.filterwarnings('ignore', category=Warning)
logging.getLogger("neo4j").setLevel(logging.ERROR)

class Neo4jConnector:
    """Conector para base de datos Neo4j"""
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password", database="housing"):
        """
        Inicializa la conexión a Neo4j
        
        Args:
            uri: URI de conexión a Neo4j
            user: Usuario de Neo4j
            password: Contraseña de Neo4j
            database: Nombre de la base de datos (housing)
        """
        self.database = database
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Verificar conexión con la base de datos específica
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            print(f"✅ Conexión a Neo4j establecida exitosamente (base de datos: {self.database})")
        except Exception as e:
            print(f"❌ Error conectando a Neo4j: {e}")
            print(f"💡 Asegúrate de que Neo4j esté ejecutándose en {uri}")
            print(f"💡 Y que la base de datos '{self.database}' esté activa")
            self.driver = None
    
    def close(self):
        """Cierra la conexión a Neo4j"""
        if self.driver:
            self.driver.close()
    
    def is_connected(self):
        """Verifica si hay conexión activa"""
        return self.driver is not None
    
    def get_session(self):
        """Obtiene una sesión de Neo4j para la base de datos específica"""
        return self.driver.session(database=self.database)
    
    def clear_database(self):
        """Limpia toda la base de datos"""
        if not self.is_connected():
            return False
            
        with self.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print(f"🗑️ Base de datos '{self.database}' limpiada")
        return True
    
    def create_property(self, property_frame: PropertyFrame):
        """Crea un nodo Property en Neo4j"""
        if not self.is_connected():
            return False
            
        with self.get_session() as session:
            query = """
            MERGE (p:Property {name: $name})
            SET p.property_type = $property_type,
                p.price = $price,
                p.area = $area,
                p.rooms = $rooms,
                p.bathrooms = $bathrooms
            MERGE (a:Address {
                street: $street,
                number: $number,
                neighborhood: $neighborhood,
                city: $city,
                province: $province
            })
            MERGE (p)-[:HAS_ADDRESS]->(a)
            RETURN p.name as property_name
            """
            result = session.run(query,
                name=property_frame.name,
                property_type=property_frame.property_type,
                price=property_frame.price,
                area=property_frame.area,
                rooms=property_frame.rooms,
                bathrooms=property_frame.bathrooms,
                street=property_frame.address.street,
                number=property_frame.address.number,
                neighborhood=property_frame.address.neighborhood,
                city=property_frame.address.city,
                province=property_frame.address.province
            )
            
            # Crear amenidades cercanas
            for amenity in property_frame.nearby_amenities:
                amenity_query = """
                MATCH (p:Property {name: $property_name})
                MERGE (a:Amenity {
                    name: $amenity_name,
                    type: $amenity_type
                })
                WITH p, a
                WHERE NOT EXISTS((p)-[:NEAR_TO]->(a))
                CREATE (p)-[:NEAR_TO {
                    distance: $distance,
                    amenity_type: $amenity_type,
                    amenity_name: $amenity_name
                }]->(a)
                """
                session.run(amenity_query,
                    property_name=property_frame.name,
                    distance=amenity["distance"],
                    amenity_type=amenity["type"],
                    amenity_name=amenity["name"]
                )
            
            return True
    
    def create_user(self, user_frame: UserFrame):
        """Crea un nodo User en Neo4j"""
        if not self.is_connected():
            return False
            
        with self.get_session() as session:
            query = """
            MERGE (u:User {name: $name})
            SET u.age = $age
            RETURN u.name as user_name
            """
            session.run(query, name=user_frame.name, age=user_frame.age)
            
            # Crear preferencias
            for pref in user_frame.preferences:
                pref_query = """
                MATCH (u:User {name: $user_name})
                MERGE (at:AmenityType {type: $amenity_type})
                WITH u, at
                WHERE NOT EXISTS((u)-[:PREFERS]->(at))
                CREATE (u)-[:PREFERS {
                    priority: $priority,
                    amenity_name: $amenity_name
                }]->(at)
                """
                session.run(pref_query,
                    user_name=user_frame.name,
                    priority=pref["priority"],
                    amenity_type=pref["type"],
                    amenity_name=pref["name"]
                )
            
            # Crear preferencias de transporte
            for transport in user_frame.transport_preferences:
                transport_query = """
                MATCH (u:User {name: $user_name})
                MERGE (t:Transport {type: $transport_type})
                WITH u, t
                WHERE NOT EXISTS((u)-[:MOVES_BY]->(t))
                CREATE (u)-[:MOVES_BY]->(t)
                """
                session.run(transport_query,
                    user_name=user_frame.name,
                    transport_type=transport.value
                )
            
            return True
    
    def create_amenity(self, amenity_frame: AmenityFrame):
        """Crea un nodo Amenity en Neo4j"""
        if not self.is_connected():
            return False
            
        with self.get_session() as session:
            # Determinar el label específico según el tipo
            amenity_labels = {
                AmenityType.PARK: "Park",
                AmenityType.HOSPITAL: "Hospital",
                AmenityType.EDUCATION_CENTRE: "EducationCentre",
                AmenityType.COMMERCIAL_CENTRE: "CommercialCentre",
                AmenityType.BUS_STOP: "BusStop"
            }
            
            label = amenity_labels.get(amenity_frame.amenity_type, "Amenity")
            
            query = f"""
            CREATE (am:{label}:Amenity {{
                name: $name,
                amenity_type: $amenity_type,
                area: $area,
                stores_count: $stores_count,
                education_type: $education_type,
                is_terminal: $is_terminal
            }})
            CREATE (a:Address {{
                street: $street,
                number: $number,
                neighborhood: $neighborhood,
                city: $city,
                province: $province
            }})
            CREATE (am)-[:HAS_ADDRESS]->(a)
            RETURN am.name as amenity_name
            """
            
            session.run(query,
                name=amenity_frame.name,
                amenity_type=amenity_frame.amenity_type.value,
                area=amenity_frame.area,
                stores_count=amenity_frame.stores_count,
                education_type=amenity_frame.education_type,
                is_terminal=amenity_frame.is_terminal,
                street=amenity_frame.address.street,
                number=amenity_frame.address.number,
                neighborhood=amenity_frame.address.neighborhood,
                city=amenity_frame.address.city,
                province=amenity_frame.address.province
            )
            
            return True
    
    def get_database_stats(self):
        """Obtiene estadísticas de la base de datos"""
        if not self.is_connected():
            return {}
            
        with self.get_session() as session:
            queries = {
                "properties": "MATCH (p:Property) RETURN count(p) AS count",
                "users": "MATCH (u:User) RETURN count(u) AS count", 
                "amenities": "MATCH (a:Amenity) RETURN count(a) AS count",
                "relationships": "MATCH ()-[r]-() RETURN count(r) AS count"
            }
            
            stats = {}
            for stat_name, query in queries.items():
                result = session.run(query)
                stats[stat_name] = result.single()["count"]
            
            return stats

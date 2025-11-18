"""
Gestor de Demonios - Sistema de Recomendación de Viviendas
Coordina y ejecuta todos los demonios de IA del sistema.

Los demonios son procesos inteligentes que aprenden y adaptan el sistema automáticamente:
- Aprendizaje de preferencias reales del usuario
- Análisis adaptativo de precios de mercado
- Detección de tendencias temporales
- Descubrimiento de patrones ocultos
- Optimización continua de recomendaciones

INTEGRADO CON: Neo4j + LangChain + LangGraph
"""

import time
import threading
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from database.neo4j_connector import Neo4jConnector

# Importar demonios compatibles con Neo4j
from demons.preference_learning_demon import PreferenceLearningDemon
from demons.compact_demons import (
    AdaptivePricingDemon,
    TemporalTrendsDemon,
    PatternDiscoveryDemon,
    RecommendationOptimizerDemon
)


class DemonsManager:
    """Gestor principal de todos los demonios de IA"""
    
    def __init__(self, connector: Neo4jConnector = None):
        """Inicializa el gestor de demonios"""
        self.connector = connector or Neo4jConnector()
        self.demons = {}
        self.running = False
        self.demon_threads = {}
        
        # Configuración de intervalos de ejecución (en segundos)
        self.execution_intervals = {
            'preference_learning': 60,      # Cada 1 minuto
            'adaptive_pricing': 300,        # Cada 5 minutos
            'temporal_trends': 180,         # Cada 3 minutos
            'pattern_discovery': 240,       # Cada 4 minutos
            'recommendation_optimizer': 120 # Cada 2 minutos
        }
        
        self._initialize_demons()
        
    def _initialize_demons(self):
        """Inicializa todos los demonios"""
        print("🤖 INICIALIZANDO DEMONIOS DE IA...")
        
        # Crear instancias de todos los demonios
        self.demons = {
            'preference_learning': PreferenceLearningDemon(self.connector),
            'adaptive_pricing': AdaptivePricingDemon(self.connector),
            'temporal_trends': TemporalTrendsDemon(self.connector),
            'pattern_discovery': PatternDiscoveryDemon(self.connector),
            'recommendation_optimizer': RecommendationOptimizerDemon(self.connector)
        }
        
        print(f"✅ {len(self.demons)} demonios inicializados")
        
    def start_all_demons(self):
        """Inicia todos los demonios en modo background"""
        if self.running:
            print("⚠️ Los demonios ya están ejecutándose")
            return
            
        print("🚀 INICIANDO TODOS LOS DEMONIOS...")
        self.running = True
        
        # Iniciar cada demonio en su propio hilo
        for demon_name, demon in self.demons.items():
            interval = self.execution_intervals[demon_name]
            thread = threading.Thread(
                target=self._run_demon_loop,
                args=(demon_name, demon, interval),
                daemon=True,
                name=f"Demon_{demon_name}"
            )
            thread.start()
            self.demon_threads[demon_name] = thread
            print(f"   ✅ {demon_name} iniciado (intervalo: {interval}s)")
        
        print("🎯 TODOS LOS DEMONIOS ACTIVOS Y APRENDIENDO")
        
    def _run_demon_loop(self, demon_name: str, demon, interval: int):
        """Ejecuta un demonio en bucle con el intervalo especificado"""
        while self.running:
            try:
                # Ejecutar el demonio
                demon.execute()
                
                # Esperar el intervalo
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Error en demonio {demon_name}: {e}")
                time.sleep(interval)  # Esperar antes de reintentar
                
    def stop_all_demons(self):
        """Detiene todos los demonios"""
        print("\n🛑 DETENIENDO DEMONIOS...")
        self.running = False
        
        # Esperar a que terminen los hilos
        for demon_name, thread in self.demon_threads.items():
            if thread.is_alive():
                print(f"   ⏸️ Deteniendo {demon_name}...")
                thread.join(timeout=2)
        
        print("✅ Todos los demonios detenidos")
    
    def get_status(self) -> Dict:
        """Obtiene el estado actual de todos los demonios"""
        status = {
            'running': self.running,
            'demons_count': len(self.demons),
            'demons': {}
        }
        
        for name, demon in self.demons.items():
            status['demons'][name] = {
                'executions': demon.execution_count,
                'last_execution': demon.last_execution.isoformat() if demon.last_execution else None
            }
        
        return status
    
    def execute_all_once(self):
        """Ejecuta todos los demonios una sola vez (útil para testing)"""
        print("\n🧪 EJECUTANDO TODOS LOS DEMONIOS UNA VEZ...")
        
        for demon_name, demon in self.demons.items():
            print(f"\n{'='*60}")
            demon.execute()
        
        print(f"\n{'='*60}")
        print("✅ Ejecución única completada")


# EJEMPLO DE USO
if __name__ == "__main__":
    from database.neo4j_connector import Neo4jConnector
    
    connector = Neo4jConnector()
    
    if not connector.is_connected():
        print("❌ Neo4j no conectado")
        exit(1)
    
    manager = DemonsManager(connector)
    
    print("\n" + "="*60)
    print("MODO TEST: Ejecutar todos los demonios una vez")
    print("="*60)
    
    manager.execute_all_once()
    
    print("\n💡 Para ejecutar continuamente, usa:")
    print("   manager.start_all_demons()")
    print("   # ... dejar corriendo ...")
    print("   manager.stop_all_demons()")

    def stop_all_demons(self):
        """Detiene todos los demonios en ejecución"""
        print("🛑 DETENIENDO TODOS LOS DEMONIOS...")
        self.running = False
        
        # Esperar que todos los hilos terminen
        for demon_name, thread in self.demon_threads.items():
            if thread.is_alive():
                thread.join(timeout=5)  # Esperar máximo 5 segundos
                print(f"   🛑 {demon_name} detenido")
        
        self.demon_threads.clear()
        print("✅ Todos los demonios detenidos")
        
    def execute_single_demon(self, demon_name: str):
        """Ejecuta un demonio específico una sola vez"""
        if demon_name not in self.demons:
            print(f"❌ Demonio '{demon_name}' no encontrado")
            return
            
        print(f"🔍 EJECUTANDO DEMONIO: {demon_name}")
        try:
            result = self.demons[demon_name].execute()
            print(f"✅ {demon_name} ejecutado exitosamente")
            return result
        except Exception as e:
            print(f"❌ Error ejecutando {demon_name}: {e}")
            return None
            
    def get_demons_status(self) -> Dict[str, Any]:
        """Obtiene el estado de todos los demonios"""
        status = {
            'manager_running': self.running,
            'demons_count': len(self.demons),
            'active_threads': len([t for t in self.demon_threads.values() if t.is_alive()]),
            'demons_status': {}
        }
        
        for demon_name, demon in self.demons.items():
            thread = self.demon_threads.get(demon_name)
            status['demons_status'][demon_name] = {
                'initialized': True,
                'thread_active': thread.is_alive() if thread else False,
                'last_execution': getattr(demon, 'last_execution', None),
                'execution_count': getattr(demon, 'execution_count', 0),
                'interval': self.execution_intervals[demon_name]
            }
            
        return status
        
    def demonstrate_demons(self):
        """Demuestra el funcionamiento de todos los demonios"""
        print("🎬 DEMOSTRACIÓN DE DEMONIOS DE IA")
        print("=" * 60)
        
        # Simular interacciones de usuario para que los demonios tengan datos
        self._simulate_user_interactions()
        
        # Ejecutar cada demonio una vez para demostración
        for demon_name in self.demons.keys():
            print(f"\n🔍 EJECUTANDO: {demon_name.replace('_', ' ').title()}")
            print("-" * 40)
            
            result = self.execute_single_demon(demon_name)
            
            if result:
                print(f"📊 Resultado: {result}")
            
            time.sleep(1)  # Pausa entre demonios para legibilidad
            
        print(f"\n🎯 DEMOSTRACIÓN COMPLETADA")
        print("💡 En modo normal, estos demonios ejecutarían automáticamente en background")
        
    def _simulate_user_interactions(self):
        """Simula interacciones de usuario para que los demonios tengan datos"""
        print("🎬 Simulando interacciones de usuario...")
        
        # Simular clicks y preferencias
        for demon in self.demons.values():
            if hasattr(demon, 'simulate_data'):
                demon.simulate_data()
                
    def get_learning_insights(self) -> Dict[str, Any]:
        """Obtiene insights de aprendizaje de todos los demonios"""
        insights = {}
        
        for demon_name, demon in self.demons.items():
            if hasattr(demon, 'get_insights'):
                insights[demon_name] = demon.get_insights()
                
        return insights
        
    def save_demons_state(self, filepath: str):
        """Guarda el estado de todos los demonios"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'demons_state': {}
        }
        
        for demon_name, demon in self.demons.items():
            if hasattr(demon, 'get_state'):
                state['demons_state'][demon_name] = demon.get_state()
                
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Estado de demonios guardado en: {filepath}")
        
    def load_demons_state(self, filepath: str):
        """Carga el estado de todos los demonios"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
                
            for demon_name, demon_state in state['demons_state'].items():
                if demon_name in self.demons and hasattr(self.demons[demon_name], 'load_state'):
                    self.demons[demon_name].load_state(demon_state)
                    
            print(f"📂 Estado de demonios cargado desde: {filepath}")
            
        except FileNotFoundError:
            print(f"⚠️ Archivo de estado no encontrado: {filepath}")
        except Exception as e:
            print(f"❌ Error cargando estado: {e}")


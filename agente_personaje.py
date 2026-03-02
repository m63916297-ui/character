"""
Agente para creación de personajes
Genera: edad, lore, ropa, historia, poderes y enemigos
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import random
import re


@dataclass
class Personaje:
    nombre: str = ""
    edad: str = ""
    lore: str = ""
    ropa: str = ""
    historia: str = ""
    poderes: List[str] = field(default_factory=list)
    enemigos: List[str] = field(default_factory=list)
    personalidad: str = ""
    debilidades: List[str] = field(default_factory=list)
    aliados: List[str] = field(default_factory=list)


PERSONAJE_TEMPLATES = {
    "heroe": {
        "tipo": "Héroe",
        "edad_base": "25-35",
        "lore_base": "Un protector nato que ha jurado defender a los inocentes",
        "ropa_base": "Armadura ligera con colores brillantes y emblemas de esperanza",
        "historia_base": "Nacido en circunstancias ordinarias, descubrió su verdadero destino al enfrentar una crisis que cambió su vida para siempre",
        "poderes_base": [
            "Fuerza sobrehumana",
            "Velocidad mejorada",
            "Sentidos agudizados",
        ],
        "enemigos_base": [
            "Villano principal",
            "Organización corrupta",
            "Antiguo aliado corrupto",
        ],
        "personalidad_base": "Valiente, noble, determinado",
        "debilidades_base": [
            "Sentido de justicia inflexible",
            "No puede ignorar a quien necesita ayuda",
            "Confía demasiado en otros",
        ],
    },
    "villano": {
        "tipo": "Villano",
        "edad_base": "30-50",
        "lore_base": "Una figura sombría forjada en tragedia y ambición",
        "ropa_base": "Túnicas oscuras o armadura intimidante con elementos distintivos",
        "historia_base": "Una vez tuvo una vida normal, pero eventos traumáticos lo empujaron por el camino de la oscuridad",
        "poderes_base": ["Manipulación", "Poderes mentales", "Control sobre otros"],
        "enemigos_base": ["Héroe local", "Su propio pasado", "Autoridades"],
        "personalidad_base": "Ambicioso, manipulador, carismático",
        "debilidades_base": [
            "Sed de venganza",
            "No puede confiar plenamente en nadie",
            "Su mayor debilidad es su orgullo",
        ],
    },
    "mago": {
        "tipo": "Mago/Hechicero",
        "edad_base": "40-100",
        "lore_base": "Un estudiante de las artes arcanas que ha dedicado su vida al conocimiento místico",
        "ropa_base": "Manto mágico con runas, bastón o libro de hechizos",
        "historia_base": "Pasó años estudiando en academias secretas o encontró conocimiento prohibido",
        "poderes_base": [
            "Manipulación de elementos",
            "Hechizos de protección",
            "Adivinación",
        ],
        "enemigos_base": [
            "Magos rivales",
            "Entidades oscuras",
            "La institución que lo expulsó",
        ],
        "personalidad_base": "Sabio, curioso, a veces distante",
        "debilidades_base": [
            "Dependencia de sus artefactos",
            "Costo para lanzar hechizos",
            "Curiosidad que lo mete en problemas",
        ],
    },
    "guerrero": {
        "tipo": "Guerrero",
        "edad_base": "20-40",
        "lore_base": "Un combatiente formado en el arte de la guerra desde temprana edad",
        "ropa_base": "Armadura completa o equipamiento de combate especializado",
        "historia_base": "Entrenó desde niño en un clan guerrero o fue reclutado por un ejército",
        "poderes_base": [
            "Maestría en armas",
            "Resistencia sobrehumana",
            "Tácticas de combate",
        ],
        "enemigos_base": [
            "Rival de batallas",
            "Señor de la guerra",
            "Su propio pasado como mercenario",
        ],
        "personalidad_base": "Disciplinado, leal, honorable",
        "debilidades_base": [
            "Desconfía de la magia",
            "No sabe negociar",
            "Su código de honor puede ser explotado",
        ],
    },
    "asesino": {
        "tipo": "Asesino",
        "edad_base": "18-35",
        "lore_base": "Un杀手 entrenado en las sombras para cumplir misiones que otros no pueden",
        "ropa_base": "Ropa oscura y práctica, máscara o capucha, armas ocultas",
        "historia_base": "Fue entrenado por una hermandad secreta o criado en las calles aprendiendo a sobrevivir",
        "poderes_base": ["Sigilo", "Venenos", "Combate con armas duales"],
        "enemigos_base": [
            "La organización que lo creó",
            "Cazadores de recompensas",
            "Su objetivo original",
        ],
        "personalidad_base": "Sarcástico, calculador, leal solo a quien paga",
        "debilidades_base": [
            "No puede resistir un contrato lucrativo",
            "Su pasado siempre lo persigue",
            "Lealtad se puede comprar",
        ],
    },
    "hacker": {
        "tipo": "Hacker",
        "edad_base": "18-30",
        "lore_base": "Un genio de la tecnología que opera en las sombras digitales",
        "ropa_base": "Ropa casual tecnológica, gafas, dispositivos wearable",
        "historia_base": "Autodidacta en programación, descubrió los secretos del sistema a temprana edad",
        "poderes_base": ["Hackeo", "Control de sistemas", "Información infinita"],
        "enemigos_base": ["Corporaciones", "Gobiernos", "Otros hackers"],
        "personalidad_base": "Inteligente, paranoico, irreverente",
        "debilidades_base": [
            "Adicción a la tecnología",
            "Desconfía de las personas",
            "No sabe luchar fisicamente",
        ],
    },
    "piloto": {
        "tipo": "Piloto",
        "edad_base": "22-40",
        "lore_base": "Un experto en navegación espacial y combate aéreo",
        "ropa_base": "Traje de piloto con casco y equipamiento de vuelo",
        "historia_base": "Creció fascin por las estrellas y entrenó para convertirse en el mejor piloto",
        "poderes_base": [
            "Reflejos сверхбыстрые",
            "Navegación instintiva",
            "Combate aéreo",
        ],
        "enemigos_base": ["Piratas espaciales", "Competidores", "Su pasado"],
        "personalidad_base": "Valiente, aventurero, testarudo",
        "debilidades_base": [
            "Arriesga demasiado",
            "No sigue reglas",
            "Su nave es su vida",
        ],
    },
    "medico": {
        "tipo": "Médico",
        "edad_base": "30-60",
        "lore_base": "Un sanador dedicado a salvar vidas",
        "ropa_base": "Bata médica o traje de emergencia médica",
        "historia_base": "Estudió medicina para ayudar a otros, ahora es vital en cualquier equipo",
        "poderes_base": [
            "Curación",
            "Primeros auxilios avanzados",
            "Conocimiento médico",
        ],
        "enemigos_base": ["Enfermedades", "La muerte", "Doctores corruptos"],
        "personalidad_base": "Compasivo, calmado, dedicado",
        "debilidades_base": [
            "No puede salvar a todos",
            "Se culpa por las muertes",
            "A veces tooca pacientes",
        ],
    },
}


def detectar_tipo(entrada: str) -> str:
    entrada_lower = entrada.lower()

    indicadores = {
        "heroe": [
            "heroe",
            "protector",
            "salvar",
            "justicia",
            "noble",
            "luchar",
            "malo",
            "bien",
        ],
        "villano": [
            "villano",
            "malvado",
            "oscuridad",
            "venganza",
            "poder",
            "corrupto",
            "conquistar",
        ],
        "mago": [
            "mago",
            "hechicero",
            "magia",
            "arcano",
            "conocimiento",
            "libro",
            "encantar",
        ],
        "guerrero": [
            "guerrero",
            "combatiente",
            "espada",
            "batalla",
            "ejercito",
            "clan",
            "lucha",
        ],
        "asesino": [
            "asesino",
            "sombra",
            "matar",
            "sigilo",
            "misión",
            "contrato",
            "matar",
        ],
        "hacker": [
            "hacker",
            "computadora",
            "codigo",
            "sistema",
            "digital",
            "tecnologia",
            "ciberspacio",
        ],
        "piloto": ["piloto", "nave", "espacio", "volar", "aviador", "estrellas"],
        "medico": ["medico", "doctor", "curar", "sanar", "salud", "hospital"],
    }

    mejor_tipo = "heroe"
    max_puntos = 0

    for tipo, palabras in indicadores.items():
        puntos = sum(1 for p in palabras if p in entrada_lower)
        if puntos > max_puntos:
            max_puntos = puntos
            mejor_tipo = tipo

    return mejor_tipo


def generar_nombre(entrada: str, template: dict) -> str:
    match = re.search(r"llama[ns]?\s+([A-Z][a-zA-Z]+)", entrada, re.IGNORECASE)
    if match:
        return match.group(1)

    prefijos = ["Z", "K", "V", "A", "M", "N", "X", "S", "R", "L"]
    sufijos = ["ax", "ion", "ex", "or", "us", "ar", "en", "ix", "os", "an"]

    return f"{random.choice(prefijos)}{random.choice(sufijos)}{random.randint(1, 99)}"


def generar_edad(entrada: str, template: dict) -> str:
    if "edad" in entrada.lower():
        numeros = re.findall(r"\d+", entrada)
        if numeros:
            return f"{numeros[0]} años"

    edad = template.get("edad_base", "25-35").split("-")
    return f"{random.randint(int(edad[0]), int(edad[1]))} años"


def generar_historia(entrada: str, template: dict) -> str:
    base = template.get("historia_base", "Una historia por descubrir")

    nombres_extraidos = re.findall(r"llama[ns]?\s+([A-Z][a-zA-Z]+)", entrada)
    if nombres_extraidos:
        nombre = nombres_extraidos[0]
        return f"{nombre} es {base.lower()}. Su nombre se ha convertido en leyenda."

    return base


def generar_poderes(entrada: str, template: dict) -> List[str]:
    poderes_base = template.get("poderes_base", ["Poder básico"])
    num_poderes = random.randint(2, 4)
    return random.sample(poderes_base, min(num_poderes, len(poderes_base)))


def generar_enemigos(entrada: str, template: dict) -> List[str]:
    enemigos_base = template.get("enemigos_base", ["Enemigo desconocido"])
    num_enemigos = random.randint(2, 3)
    return random.sample(enemigos_base, min(num_enemigos, len(enemigos_base)))


def generar_personalidad(template: dict) -> str:
    return template.get("personalidad_base", "Por determinar")


def generar_personaje(entrada: str) -> Personaje:
    tipo = detectar_tipo(entrada)
    template = PERSONAJE_TEMPLATES.get(tipo, PERSONAJE_TEMPLATES["heroe"])

    personaje = Personaje()
    personaje.nombre = generar_nombre(entrada, template)
    personaje.edad = generar_edad(entrada, template)
    personaje.lore = template.get("lore_base", "")
    personaje.ropa = template.get("ropa_base", "")
    personaje.historia = generar_historia(entrada, template)
    personaje.poderes = generar_poderes(entrada, template)
    personaje.enemigos = generar_enemigos(entrada, template)
    personaje.personalidad = generar_personalidad(template)
    personaje.debilidades = template.get("debilidades_base", []).copy()
    personaje.aliados = ["Aliados por determinar"]

    return personaje


class AgenteCreadorPersonajes:
    def __init__(self):
        self.pasos = []

    def crear_personaje(self, descripcion: str) -> dict:
        self.pasos = [
            "Analizando descripción",
            "Detectando tipo",
            "Generando atributos",
        ]

        personaje = generar_personaje(descripcion)

        return {
            "personaje": self._formatear(personaje),
            "personaje_obj": personaje,
            "pasos_ejecutados": self.pasos,
            "estado": "completado",
        }

    def _formatear(self, personaje: Personaje) -> str:
        poderes_str = "\n".join([f"  - {p}" for p in personaje.poderes])
        enemigos_str = "\n".join([f"  - {e}" for e in personaje.enemigos])

        return f"""# PERSONAJE CREADO

## Información Básica
- **Nombre:** {personaje.nombre}
- **Edad:** {personaje.edad}

---

## Personalidad
{personaje.personalidad}

---

## Historia
{personaje.historia}

---

## Poderes
{poderes_str}

---

## Enemigos
{enemigos_str}
"""


def crear_agente() -> AgenteCreadorPersonajes:
    return AgenteCreadorPersonajes()


if __name__ == "__main__":
    agente = crear_agente()
    resultado = agente.crear_personaje(
        "Crea un heroe llamado Valerius que lucha contra el mal"
    )
    print(resultado["personaje"])

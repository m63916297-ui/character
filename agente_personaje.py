"""
Agente LangGraph para creación de personajes
Crea: edad, lore, ropa, historia, poderes y enemigos
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import re


class EstadoPersonaje(Enum):
    INICIADO = "iniciado"
    ANALIZANDO_ENTRADA = "analizando_entrada"
    GENERANDO_EDAD = "generando_edad"
    GENERANDO_LORE = "generando_lore"
    GENERANDO_ROPA = "generando_ropa"
    GENERANDO_HISTORIA = "generando_historia"
    GENERANDO_PODERES = "generando_poderes"
    GENERANDO_ENEMIGOS = "generando_enemigos"
    COMPILANDO_PERSONAJE = "compilando_personaje"
    COMPLETADO = "completado"
    ERROR = "error"


@dataclass
class Personaje:
    nombre: str = ""
    edad: str = ""
    lore: str = ""
    ropa: str = ""
    historia: str = ""
    poderes: List[str] = field(default_factory=list)
    enemigos: List[str] = field(default_factory=list)
    genero: str = ""
    ocupacion: str = ""
    raza: str = ""
    personalidad: str = ""
    debilidades: List[str] = field(default_factory=list)
    aliados: List[str] = field(default_factory=list)


@dataclass
class State:
    input_usuario: str
    personaje: Personaje = field(default_factory=Personaje)
    estado_actual: EstadoPersonaje = EstadoPersonaje.INICIADO
    pasos_ejecutados: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class TemplatePersonaje:
    tipo: str
    edad_base: str
    lore_base: str
    ropa_base: str
    historia_base: str
    poderes_base: List[str]
    enemigos_base: List[str]
    personalidad_base: str
    debilidades_base: List[str]


PERSONAJE_TEMPLATES = {
    "heroe": TemplatePersonaje(
        tipo="Héroe",
        edad_base="25-35",
        lore_base="Un protector nato que ha jurados defender a los inocentes",
        ropa_base="Armadura ligera ovestimenta noble con colores brillantes",
        historia_base="Nacido en circunstancias ordinarias, descubrió su verdadero destino al enfrentar una crisis que cambio su vida",
        poderes_base=[
            "Fuerza sobrehumana",
            "Velocidad mejorada",
            "Sentidos agudizados",
        ],
        enemigos_base=[
            "Villano principal",
            "Organización corrupta",
            "Antiguo ally corrupto",
        ],
        personalidad_base="Valiente, noble, determinado",
        debilidades_base=[
            "Sentido de justicia inflexible",
            "No puede ignorar a quien necesita ayuda",
            "Confía demasiado en otros",
        ],
    ),
    "villano": TemplatePersonaje(
        tipo="Villano",
        edad_base="30-50",
        lore_base="Una figura sombría whose path was forged in tragedy and ambition",
        ropa_base="Túnicas oscuras o armadura intimidante con elementos distintivos",
        historia_base="Una vez tuvo una vida normal, pero eventos traumáticos lo empujaron por el camino de la oscuridad",
        poderes_base=["Manipulación", "Poderes mentales", "Control sobre otros"],
        enemigos_base=["Héroe local", "Su propio pasado", "Autoridades"],
        personalidad_base="Ambicioso, manipulador, carismático",
        debilidades_base=[
            "Sed de venganza",
            "No puede confiar plenamente en nadie",
            "Su mayor debilidad es su orgullo",
        ],
    ),
    "mago": TemplatePersonaje(
        tipo="Mago/Hechicero",
        edad_base="40-100",
        lore_base="Un estudiante de las artes arcanas que ha dedicado su vida al conocimiento místico",
        ropa_base="Manto mágico con runas, bastón o libro de hechizos",
        historia_base="Pasó años estudiando en academias secretas o学习了 conocimiento prohibido",
        poderes_base=[
            "Manipulación de elementos",
            "Hechizos de protección",
            "Adivinación",
        ],
        enemigos_base=[
            "Magos rivales",
            "Entidades oscuras",
            "La institución que lo expulsó",
        ],
        personalidad_base="Sabio, curioso, a veces distante",
        debilidades_base=[
            "Dependencia de sus artefactos",
            "Costoso para lanzar hechizos",
            "Curiosidad que lo mete en problemas",
        ],
    ),
    "guerrero": TemplatePersonaje(
        tipo="Guerrero",
        edad_base="20-40",
        lore_base="Un combatiente formado en el arte de la guerra desde temprana edad",
        ropa_base="Armadura completa o equipamiento de combate especializados",
        historia_base="Entrenó desde niño en un clan guerrero o fue reclutado por un ejercito",
        poderes_base=[
            "Maestría en armas",
            "Resistencia sobrehumana",
            "Tácticas de combate",
        ],
        enemigos_base=[
            "Rival de batallas",
            "Señor de la guerra",
            "Su propio pasado como mercenario",
        ],
        personalidad_base="Disciplinado, leal, honorable",
        debilidades_base=[
            "Desconfía de la magia",
            "No sabe negociar",
            "Su código de honor puede ser explotado",
        ],
    ),
    "asassino": TemplatePersonaje(
        tipo="Asesino",
        edad_base="18-35",
        lore_base="Un杀手 entrenado en las sombras para cumplir misiones que otros no pueden",
        ropa_base="Ropa oscura y práctica, máscara o capucha, armas ocultas",
        historia_base="Fue entrenado por una hermandad secreta o criado en las calles aprendiendo a sobrevivir",
        poderes_base=["Sigilo", "Venenos", "Combate con armas duales"],
        enemigos_base=[
            "La organización que lo creó",
            "Cazadores de recompensas",
            "Su objetivo original",
        ],
        personalidad_base="Sarcástico, calculador, leal solo a quien paga",
        debilidades_base=[
            "No puede resistir un contrato lucrativo",
            "Su pasado siempre lo persigue",
            "Lealtad se puede comprar",
        ],
    ),
    "chaman": TemplatePersonaje(
        tipo="Chamán/Espiritualista",
        edad_base="25-50",
        lore_base="Un guía espiritual que conecta con el mundo de los espíritus y la naturaleza",
        ropa_base="Vestimentas tribales o rituales con plumas, huesos y pigments",
        historia_base="Fue marcado por los espíritus desde niño y entrenado por los ancianos de su tribu",
        poderes_base=[
            "Comunicación con espíritus",
            "Curación natural",
            "Visiones proféticas",
        ],
        enemigos_base=[
            "Entidades corruptas",
            "Cazadores de lo paranormal",
            "La industria que destruye la naturaleza",
        ],
        personalidad_base="Sagaz, mystico, conectado con la naturaleza",
        debilidades_base=[
            "Dependencia de rituales",
            "Los espíritus pueden ser traicioneros",
            "Su poder atrae a quienes lo quieren usar",
        ],
    ),
}


def detectar_tipo_personaje(entrada: str) -> str:
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
        "asassino": [
            "asesino",
            "asesino",
            "sombra",
            "matar",
            "sigilo",
            "misión",
            "contrato",
        ],
        "chaman": [
            "chaman",
            "espiritu",
            "naturaleza",
            "tribu",
            "curar",
            "ritual",
            "vision",
        ],
    }

    mejor_tipo = "heroe"
    max_puntos = 0

    for tipo, palabras in indicadores.items():
        puntos = sum(1 for p in palabras if p in entrada_lower)
        if puntos > max_puntos:
            max_puntos = puntos
            mejor_tipo = tipo

    return mejor_tipo


def generar_edad(template: TemplatePersonaje, entrada: str) -> str:
    if "edad" in entrada.lower():
        numeros = re.findall(r"\d+", entrada)
        if numeros:
            return f"{numeros[0]} años"

    edad = template.edad_base
    return f"Aproximadamente {edad}"


def generar_lore(template: TemplatePersonaje, entrada: str) -> str:
    return template.lore_base


def generar_ropa(template: TemplatePersonaje, entrada: str) -> str:
    return template.ropa_base


def generar_historia(template: TemplatePersonaje, entrada: str) -> str:
    return template.historia_base


def generar_poderes(template: TemplatePersonaje, entrada: str) -> List[str]:
    return template.poderes_base.copy()


def generar_enemigos(template: TemplatePersonaje, entrada: str) -> List[str]:
    return template.enemigos_base.copy()


def generar_personalidad(template: TemplatePersonaje) -> str:
    return template.personalidad_base


def generar_debilidades(template: TemplatePersonaje) -> List[str]:
    return template.debilidades_base.copy()


def analizar_entrada(state: State) -> State:
    state.pasos_ejecutados.append("Analizando entrada del usuario")
    state.estado_actual = EstadoPersonaje.ANALIZANDO_ENTRADA

    entrada = state.input_usuario

    match = re.search(
        r"(?:llama|nombre|se llama|personaje)\s+([A-Z][a-zA-Z]+)",
        entrada,
        re.IGNORECASE,
    )
    if match:
        state.personaje.nombre = match.group(1)
    else:
        state.personaje.nombre = "Personaje Sin Nombre"

    return state


def crear_nodo_generar(tipo_atributo: str, funcion_generadora, atributo_destino: str):
    def nodo_generar(state: State) -> State:
        state.pasos_ejecutados.append(f"Generando {tipo_atributo}")
        state.estado_actual = getattr(
            EstadoPersonaje, f"GENERANDO_{tipo_atributo.upper()}"
        )

        entrada = state.input_usuario
        template = PERSONAJE_TEMPLATES.get(
            detectar_tipo_personaje(entrada), PERSONAJE_TEMPLATES["heroe"]
        )

        if callable(funcion_generadora):
            resultado = funcion_generadora(template, entrada)
        else:
            resultado = funcion_generadora

        if isinstance(resultado, list):
            setattr(state.personaje, atributo_destino, resultado)
        else:
            setattr(state.personaje, atributo_destino, str(resultado))

        return state

    return nodo_generar


def compilar_personaje(state: State) -> State:
    state.pasos_ejecutados.append("Compilando personaje final")
    state.estado_actual = EstadoPersonaje.COMPILANDO_PERSONAJE

    template = PERSONAJE_TEMPLATES.get(
        detectar_tipo_personaje(state.input_usuario), PERSONAJE_TEMPLATES["heroe"]
    )

    if not state.personaje.raza:
        state.personaje.raza = "Humano"
    if not state.personaje.personalidad:
        state.personaje.personalidad = generar_personalidad(template)
    if not state.personaje.debilidades:
        state.personaje.debilidades = generar_debilidades(template)
    if not state.personaje.aliados:
        state.personaje.aliados = ["Aliados por determinar"]

    return state


def nodo_completado(state: State) -> State:
    state.estado_actual = EstadoPersonaje.COMPLETADO
    return state


def crear_workflow() -> StateGraph:
    workflow = StateGraph(State)

    workflow.add_node("analizar", analizar_entrada)
    workflow.add_node("edad", crear_nodo_generar("edad", generar_edad, "edad"))
    workflow.add_node("lore", crear_nodo_generar("lore", generar_lore, "lore"))
    workflow.add_node("ropa", crear_nodo_generar("ropa", generar_ropa, "ropa"))
    workflow.add_node(
        "historia", crear_nodo_generar("historia", generar_historia, "historia")
    )
    workflow.add_node(
        "poderes", crear_nodo_generar("poderes", generar_poderes, "poderes")
    )
    workflow.add_node(
        "enemigos", crear_nodo_generar("enemigos", generar_enemigos, "enemigos")
    )
    workflow.add_node("compilar", compilar_personaje)
    workflow.add_node("completado", nodo_completado)

    workflow.set_entry_point("analizar")

    workflow.add_edge("analizar", "edad")
    workflow.add_edge("edad", "lore")
    workflow.add_edge("lore", "ropa")
    workflow.add_edge("ropa", "historia")
    workflow.add_edge("historia", "poderes")
    workflow.add_edge("poderes", "enemigos")
    workflow.add_edge("enemigos", "compilar")
    workflow.add_edge("compilar", "completado")
    workflow.add_edge("completado", END)

    return workflow


def formatear_personaje(personaje: Personaje) -> str:
    poderes_str = "\n".join([f"  - {p}" for p in personaje.poderes])
    enemigos_str = "\n".join([f"  - {e}" for e in personaje.enemigos])
    debilidades_str = "\n".join([f"  - {d}" for d in personaje.debilidades])
    aliados_str = "\n".join([f"  - {a}" for a in personaje.aliados])

    return f"""# PERSONAJE CREADO

## Información Básica
- **Nombre:** {personaje.nombre}
- **Edad:** {personaje.edad}
- **Raza:** {personaje.raza}
- **Género:** {personaje.genero}
- **Ocupación:** {personaje.ocupacion}

---

## Personalidad
{personaje.personalidad}

---

## Lore
{personaje.lore}

---

## Historia
{personaje.historia}

---

## Ropa/Apariencia
{personaje.ropa}

---

## Poderes
{poderes_str}

---

## Enemigos
{enemigos_str}

---

## Debilidades
{debilidades_str}

---

## Aliados
{aliados_str}
"""


class AgenteCreadorPersonajes:
    def __init__(self):
        self.graph = crear_workflow()
        self.compilado = self.graph.compile()

    def crear_personaje(self, descripcion: str) -> Dict[str, Any]:
        estado_inicial = State(input_usuario=descripcion)

        resultado = self.compilado.invoke(estado_inicial)

        return {
            "personaje": formatear_personaje(resultado["personaje"]),
            "personaje_obj": resultado["personaje"],
            "pasos_ejecutados": resultado["pasos_ejecutados"],
            "estado": resultado["estado_actual"].value,
        }


def crear_agente() -> AgenteCreadorPersonajes:
    return AgenteCreadorPersonajes()


if __name__ == "__main__":
    agente = crear_agente()

    descripcion = "Crea un heroe llamado Valerius que lucha contra el mal"
    resultado = agente.crear_personaje(descripcion)

    print(resultado["personaje"])
    print("\n--- Pasos ejecutados ---")
    for paso in resultado["pasos_ejecutados"]:
        print(f"- {paso}")

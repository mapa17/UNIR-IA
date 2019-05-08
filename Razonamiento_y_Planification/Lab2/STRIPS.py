## Students
##
## * Gonzalo Molina
## * Sol Román Mendaña
## * David Garcia Retuerta
## * Manuel Pasieka
##

from typing import List, Dict
from copy import deepcopy
import numpy as np

POSICIONES = [0, 1, 2]


class Propiedad(object):
    nombre: str
    activa: bool

    def __init__(self, nombre):
        self.nombre = nombre
        self.activa = False

    def __eq__(self, other):
        if not isinstance(other,Propiedad):
            return False

        return self.nombre == other.nombre

    def __str__(self):
        return self.nombre


class PropiedadPosicion(Propiedad):
    posicion: int

    def __init__(self, nombre, posicion):
        if not posicion in POSICIONES:
            raise Exception("Posicion no aplicable {}".format(posicion))
        self.posicion = posicion
        Propiedad.__init__(self, "{} {}".format(nombre,posicion))


class MonoPosicion(PropiedadPosicion):
    def __init__(self, posicion):
        PropiedadPosicion.__init__(self, "Mono en", posicion)


class ConPlatano(Propiedad):
    def __init__(self):
        Propiedad.__init__(self, "Con Platano")


class SobreCaja(PropiedadPosicion):
    def __init__(self, pos):
        PropiedadPosicion.__init__(self, "Sobre la Caja", pos)

class EnSuelo(Propiedad):
    def __init__(self):
        Propiedad.__init__(self, "En Suelo")

class CajaPosicion(PropiedadPosicion):
    def __init__(self, posicion):
        PropiedadPosicion.__init__(self, "Caja en", posicion)

class PlatanoPosicion(PropiedadPosicion):
    def __init__(self, posicion):
        PropiedadPosicion.__init__(self, "Platano en", posicion)

class Estado(object):
    propiedades: Dict[str,Propiedad]

    def __init__(self, props: List[Propiedad] = []):
        self.propiedades = dict()
        self.__crear_propiedades()
        self.configurar(props)
    
    def __crear_posiciones(self):
        for i in POSICIONES:
            m = MonoPosicion(i)
            self.propiedades[m.nombre] = m
            c = CajaPosicion(i)
            self.propiedades[c.nombre] = c
            p = PlatanoPosicion(i)
            self.propiedades[p.nombre] = p
            s = SobreCaja(i)
            self.propiedades[s.nombre] = s

    def __crear_propiedades(self):
        self.__crear_posiciones()

        s = EnSuelo()
        self.propiedades[s.nombre] = s
        s = ConPlatano()
        self.propiedades[s.nombre] = s

    def configurar(self, props: List[Propiedad]):
        """Apply the following properties to the state
        
        Arguments:
            props {List[Propiedad]} -- [description]
        """
        for p in props:
            self.propiedades[p.nombre].activa = True


    def pendientes(self, props: List[Propiedad])-> List[Propiedad]:
        """Check which of the given properties is active for this state
        Can be used to compare states?
        
        Arguments:
            props {List[Propiedad]} -- [description]
        
        Returns:
            List[Propiedad] -- Active properties
        """
        result = []
        for p in props:
            if not self.propiedades[p.nombre].activa:
                result.append(p)
        return result
    
    

    #def __str__(self):
    def __repr__(self):
        techo = ""
        for i in POSICIONES:
            platano = PlatanoPosicion(i)
            if self.propiedades[platano.nombre].activa:
                techo+=" P "
            else:
                techo+="   "
        suelo_m = ""
        for i in POSICIONES:
            mono = MonoPosicion(i)
            if self.propiedades[mono.nombre].activa:
                suelo_m+=" M "
            else:
                suelo_m+="   "

        suelo_c = ""
        for i in POSICIONES:
            caja = CajaPosicion(i)
            if self.propiedades[caja.nombre].activa:
                suelo_c += " C "
            else:
                suelo_c += "   "

        if self.propiedades[EnSuelo().nombre].activa:
            ensuelo = "En Suelo"
        else:
            ensuelo = "Sobre Caja"

        conplatano = ""
        if self.propiedades[ConPlatano().nombre].activa:
            conplatano = "Con Platano"
        return "{}\n{}\n{}\n {} {}".format(techo,suelo_m,suelo_c,ensuelo,conplatano)

###################

class Operador(object):
    nombre: str
    PC: List[Propiedad]
    A : List[Propiedad]
    E : List[Propiedad]

    def __init__(self, nombre):
        self.nombre = nombre
        self.PC = []
        self.A = []
        self.E = []

    def aplicar(self, estado: Estado)->Estado:
        result = deepcopy(estado)

        for i in self.A:
            result.propiedades[i.nombre].activa=True

        for i in self.E:
            result.propiedades[i.nombre].activa=False

        return result

    def aplicable(self, estado:Estado)->bool:
        for i in self.PC:
            if not estado.propiedades[i.nombre].activa:
                return False

        return True

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class MoverMono(Operador):
    def __init__(self, origen: int, destino:int):
        Operador.__init__(self,"MoverMono({},{})".format(origen,destino))
        self.PC.append(EnSuelo())
        self.PC.append(MonoPosicion(origen))

        self.A.append(MonoPosicion(destino))

        self.E.append(MonoPosicion(origen))

class MoverCaja(Operador):
    def __init__(self, origen: int, destino: int):
        Operador.__init__(self, "MoverCaja({},{})".format(origen, destino))
        self.PC.append(EnSuelo())
        self.PC.append(MonoPosicion(origen))
        self.PC.append(CajaPosicion(origen))

        self.A.append(CajaPosicion(destino))

        self.E.append(CajaPosicion(origen))


class Subir(Operador):
    def __init__(self, origen: int):
        Operador.__init__(self, "SubirCaja({})".format(origen))
        self.PC.append(EnSuelo())
        self.PC.append(MonoPosicion(origen))
        self.PC.append(CajaPosicion(origen))

        self.A.append(SobreCaja(origen))

        self.E.append(EnSuelo())

class Bajar(Operador):
    def __init__(self, origen):
        Operador.__init__(self, "BajarCaja({})".format(origen))
        self.PC.append(SobreCaja(origen))

        self.A.append(EnSuelo())

        self.E.append(SobreCaja(origen))

class ObtenerPlatano(Operador):
    def __init__(self, origen: int):
        Operador.__init__(self, "ObtenerPlatano({})".format(origen))
        self.PC.append(SobreCaja(origen))
        self.PC.append(PlatanoPosicion(origen))
        self.PC.append(MonoPosicion(origen))

        self.A.append(ConPlatano())

        self.E.append(PlatanoPosicion(origen))

class Acciones(object):
    disponibles: List[Operador]

    def __init__(self):
        self.disponibles = []
        for i in POSICIONES:
            self.disponibles.append(Subir(i))
            self.disponibles.append(ObtenerPlatano(i))
            for j in POSICIONES:
                if i != j:
                    self.disponibles.append((MoverCaja(i, j)))
                    self.disponibles.append((MoverMono(i, j)))

    def aplicables(self, estado:Estado)->List[Operador]:
        result = []
        for a in self.disponibles:
            if a.aplicable(estado):
                result.append(a)
        return result

    def produce(self, prop: Propiedad)-> List[Operador]:
        result = []
        for a in self.disponibles:
            if prop in a.A:
                result.append(a)
        return result

def join_props(a: List[Propiedad], b: List[Propiedad]):
    c = []
    __join_props(c, a)
    __join_props(c, b)
    return c
        
def __join_props(base: List[Propiedad], other: List[Propiedad]):
    bt = [type(b) for b in base]
    for oi in other:
        to = type(oi)
        if (to is SobreCaja) and (EnSuelo in bt):
            continue
        if (to is EnSuelo) and (SobreCaja in bt):
            continue
        if to not in bt:
            base.append(oi)
            bt.append(to)


############################# STUDENT CODE BEGINING ############################

def activos(self):
    """Helper function that returns active properties
    Returns:
        [type] -- [description]
    """
    result = []
    for n, p in self.propiedades.items():
        if p.activa:
            result.append(p)
    return result

# Patch the 'Estado' class, adding the helper function
setattr(Estado, "activos", activos)


# Add dummy definition in order to avoid future reference error
class Plan(object):
    pass

class Plan(object):
    """Helper class that holds the plan in form of a forward linked list.
    
    Arguments:
        object {[type]} -- [description]
    """
    estado: Estado
    accion: Operador
    siguiente: Plan

    def __init__(self, estado: Estado, accion: Operador, siguiente: Plan):
        self.estado = estado
        self.accion = accion
        self.siguiente = siguiente


def STRIPS(active_plans, meta, acciones)->Plan:
    """Search for a Plan modifying 'active_plans' until
    the meta state is reached.

    Perform a breath first exhaustive search.
    
    Arguments:
        active_plans {[type]} -- [description]
        meta {[type]} -- [description]
        acciones {[type]} -- [description]
    
    Returns:
        Plan -- [description]
    """
    while(1):
        try:
            current = active_plans.pop(0)
        except IndexError:
            # No solution!
            return None

        # Check if the current node/plan satisfies all properties of the meta
        if current.estado.pendientes(meta.activos()) == []:
            # Found a solution
            return current
            
        # Generate all possible pre states to this one
        active_props = current.estado.activos()
        for ap in active_props:
            possible_actions = acciones.produce(ap)

            for next_action in possible_actions:

                # Modify the active properties, replacing the active prop with
                # the preconditions of the action that leads to it
                new_props = current.estado.activos()
                new_props.remove(ap)
                new_props = join_props(new_props, next_action.PC)

                # Check if the state is applicable for that action
                prev_state = Estado(new_props)
                if next_action.aplicable(prev_state):
                    # Create a new plan that is the preceding this one
                    new_plan = Plan(prev_state, next_action, current)

                    # Append the new node/plan to the list of active ones
                    active_plans.append(new_plan)


if __name__ == "__main__":
    e = Estado([MonoPosicion(0),CajaPosicion(2),PlatanoPosicion(1), EnSuelo()])
    #e = Estado([MonoPosicion(1),CajaPosicion(1),PlatanoPosicion(1), EnSuelo()])
    #e = Estado([MonoPosicion(0),CajaPosicion(0),PlatanoPosicion(1), EnSuelo()])
    acciones = Acciones()

    # Generate a plan containing the meta state 
    meta = Plan(Estado([ConPlatano()]), None, None)

    # Try to find a sequence of states from the meta to the initial state (regresivo)
    sequencia = STRIPS([meta], e, acciones)

    if sequencia:
        print('Initial state:\n{}\n'.format(e))
        print('Meta:\n{}\n'.format(meta.estado))
        print('=====================')
        # Iterate until we get to a node without next action
        current = sequencia
        nactions = 0
        while(current.accion):
            print('Apply action {}\n'.format(current.accion))
            e = current.accion.aplicar(e)
            print(e)
            nactions+=1
            current = current.siguiente
            print('------------')
        
        print('Final state\n{}'.format(e))

        print('This took %d actions ...' % nactions)
    else:
        print('Found no solution!')

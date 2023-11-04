

class operacion:
    """ 
    Clase operacion 
    """

    def __init__(self, a, b):
        """
        Constructor de la clase operacion
        """
        self.a = a
        self.b = b
    
    def suma(self):
        """
        Metodo que suma dos numeros
        """
        return self.a + self.b

class prueba:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        return self.a + self.b
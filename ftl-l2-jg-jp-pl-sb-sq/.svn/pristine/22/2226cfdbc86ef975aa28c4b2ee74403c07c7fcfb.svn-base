class Door(object):
    """
    Class which allow you to monitor each door.
    """

    def __init__(self, position, link, hasDoor=True):
        """

        @param position: Position de la porte qui fait 0 d'epaisseur et 2 de largeur,
        on veut donc les deux points qui sont les extremitees du segment.
        @type position: Tuple de 2 tuple de 2 entiers.
        @param link: Which rooms are linked by this door.
        @type link: Tuple of 2 integer.
        @param hasDoor: Permet de savoir si il y a une porte, si il y en a pas on dit que la porte est toujours ouverte.
        @type hasDoor: Booleen.
        """
        self.__link = link
        self.__closed = True
        self.__position = position
        self.__hasDoor = hasDoor

    def isClosed(self):
        """
        Renvoie vrai si la porte est fermee.
        @return: Renvoie vrai si la porte est fermee.
        @rtype: Booleen.
        """
        if self.__hasDoor:
            return self.__closed
        return True

    def getPosition(self):
        return self.__position

    def getLink(self):
        """
        Renvoie les salles reliees par la porte.
        @return: Retourne le tuple des salles reliees.
        @rtype: Tuple d'entiers correspondant aux salles dans la liste du vaisseau, donc ca commence a 0.
        """
        return self.__link

    def closeDoor(self):
        """
        Ferme la porte si il y en a une.
        """
        if self.__hasDoor:
            self.__closed = True

    def openDoor(self):
        """
        Ouvre la porte.
        """
        self.__closed = False
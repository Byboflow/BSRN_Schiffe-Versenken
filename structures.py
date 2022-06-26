class Square:
    """
    Klasse für Repraesentation eines Squares im Spielfeld
    """
    def __init__(self, sign):
        """
        :param sign: str -> String Repraesentation eines Squares
        """
        self.sign = sign
        self.final_sign = sign

    def change_sign(self, sign):
        """
        Zeichen eines Square-Objects aendern

        :param sign: str -> String representation eines Squares
        """
        self.sign = sign

    def __repr__(self):
        """
        String Repreaesentation eines Squares returnen
        """
        return self.sign

    def __str__(self):
        """
        String Repraesentation eines Squares returnen
        """
        return self.sign

class OceanSquare(Square):
    """
    Konkrete Klasse, die den spielbaren Ozean repraesentiert
    """
    def __init__(self, ShipReference=None):
        """
        :param ShipReference: str -> String Repraesentation von OceanSquare
        """
        if(ShipReference is None):
            super().__init__("~ ")
        else:
            super().__init__(ShipReference)


class ShipSquare(Square):
    """
    Konkrete Klasse, die das Schiff repraesentiert
    """
    def __init__(self, sign):
        """
        :param sign: str -> String Representation von Square
        """
        super().__init__(sign)

class Ocean():
    """
    Klasse, die das Feld repraesentiert (mit List)
    """
    def __init__(self, height, width):
        self.board = []

        self.board_width = width
        self.board_height = height

        self.create_board(height, width)

    def create_board(self, height, width):
        """
        Spielfeld erstellen mit List, die Square Objekte enthält

        :param height: int -> hoehe des feldes, default: 10
        :param width: int -> weite des feldes, default: 10
        """
        if self.board:
            self.board = []
        for c in range(0, height):
            self.board.append([OceanSquare() for i in range(width)])
            
    def __str__(self):
        """
        Spielfeld/Board ausgeben
        """
        res = "    "
        for i in range(self.board_width):
            if i != self.board_width-1:
                res += chr(i+65) + "  "
            else:
                res += chr(i+65)
        res += " \n"

        for i in range(self.board_height):
            if(len(str(i+1)) == 1):
                temp = str(i+1) + "  "
            else:
                temp = str(i+1) + " "
                
            for x in self.board[i]:
                temp += " " + x.__str__()

            res += temp + "\n"

        return res


class Ship():
    """
    Repraesentiert Schiff-Objekt auf dem Spielfeld
    """
    def __init__(self, space: int, sign: str, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        """
        :param space: int -> Laenge eines Schiffs
        :param sign: str -> String Representation eines Schiffs
        :param ocean: Ocean -> Ocean, wo das Schiff platziert ist
        :param is_horizontal: bool -> True, wenn Schiff horizontal platziert ist, false wenn vertikal
        :param starting_point: int, int -> Tuple mit Startpunkt des Schiffs (Reihe, Spalte)
        :param is_decoy: bool -> True, wenn Schiff am temporaeren Spielfeld platziert wird, default: false
        """
        self.space = space
        self.sign = sign
        self.ocean = ocean
        self.is_horizontal = is_horizontal
        if not is_decoy:
            self.create_ship_by_user(starting_point)
        else:
            self.create_ship_by_decoy(starting_point)

    def create_ship_by_user(self, starting_point):
        """
        Checke, ob Schiff hier platziert werden kann und Schiff dann auf das Brett hinzufügen

        Schiffe können nur vertikal oder horizontal platziert werden
        Schiffe können nicht am Rand des Spielfeldes plaziert werden
        Schiffe dürfen nicht überschneiden oder sich berühren

        :param starting_point: int, int -> Tuple mit Startpunkt eines Schiffs (Reihe, Spalte)
        """

        x = starting_point[0]
        y = starting_point[1]

        if self.is_horizontal:
            if x <= 0 or x + self.space > self.ocean.board_width-1 or y <= 0 or y > self.ocean.board_height-1:
                raise ValueError('Das geht nicht. Dein Schiff ist am Rand!')
        else:
            if y <= 0 or y + self.space > self.ocean.board_height-1 or x <= 0 or x > self.ocean.board_width-1:
                raise ValueError('Das geht nicht. Dein Schiff ist am Rand!')

        if self.is_another_ship_near(x, y):
            raise ValueError('Es dürfen keine Schiffe neben eines anderen Schiffs platziert werden!')

        if self.is_horizontal:
            self.ocean.board[y][x: x + self.space] = [ShipSquare(self.sign) for i in range(self.space)]
        else:
            for i in self.ocean.board[y:y + self.space]:
                i[x] = ShipSquare(self.sign)

    def create_ship_by_decoy(self, position):
        """
        Schiff bewegen, während es platziert wird. Um es hinzubekommen, erstellen wir einen temporären Ozean

        :param position: int, int -> Tuple mit Startpunkt des Schiffs (Reihe, Spalte)
        """
        x = position[0]
        y = position[1]
        if self.is_horizontal:
            self.ocean.board[y][x: x + self.space] = [ShipSquare(self.sign) for i in range(self.space)]
        else:
            for i in self.ocean.board[y:y + self.space]:
                i[x] = ShipSquare(self.sign)

    def is_another_ship_near(self, x, y):
        """
        Check, ob in der gegebenen Position des Schiffs sich ein anderes Schiff befindet

        :param x: int -> Row
        :param y: int -> Line
        """
        BUFFER = 1
        surrounding = []

        if self.is_horizontal:
            surrounding += self.ocean.board[y + BUFFER][x - BUFFER: x + BUFFER + self.space]
            surrounding += self.ocean.board[y][x - BUFFER: x + BUFFER + self.space]
            surrounding += self.ocean.board[y - BUFFER][x - BUFFER: x + BUFFER + self.space]
        else:
            surrounding += [i[x - BUFFER] for i in self.ocean.board[y - BUFFER: y + BUFFER + self.space]]
            surrounding += [i[x] for i in self.ocean.board[y - BUFFER: y + BUFFER + self.space]]
            surrounding += [i[x + BUFFER] for i in self.ocean.board[y - BUFFER: y + BUFFER + self.space]]
        return any(isinstance(i, ShipSquare) for i in surrounding)

    def __str__(self):
        return self.sign


class Carrier(Ship):

    def __init__(self, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        super().__init__(5, "CA", ocean, is_horizontal, starting_point, is_decoy)
        
class Battleship(Ship):
    def __init__(self, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        super().__init__(4, "BS", ocean, is_horizontal, starting_point, is_decoy)


class Cruiser(Ship):

    def __init__(self, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        super().__init__(3, "CR", ocean, is_horizontal, starting_point, is_decoy)


class Submarine(Ship):

    def __init__(self, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        super().__init__(2, "SU", ocean, is_horizontal, starting_point, is_decoy)


class Destroyer(Ship):
    def __init__(self, ocean: Ocean,
                 is_horizontal: bool, starting_point, is_decoy=False):
        super().__init__(1, "DE", ocean, is_horizontal, starting_point, is_decoy)

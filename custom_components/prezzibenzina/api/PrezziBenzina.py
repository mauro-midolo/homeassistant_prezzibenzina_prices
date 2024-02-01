

import string


class PrezziBenzina():
    
    def __init__(self, name: string, street:string, values) -> None:
        self._name = name
        self._street = street
        self._values = values

    def get_name(self) -> string:
        return self._name

    def get_street(self) -> string:
        return self._street

    def get_values(self) -> list:
        return self._values
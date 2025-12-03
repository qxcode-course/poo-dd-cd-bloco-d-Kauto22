class Fone():
    def __init__(self, id: str, number: str):
        self.__id = id
        self.__number = number

    def getId(self):
        return self.__id
    
    def getNumber(self):
        return self.__number
    
    def isValid(self) -> bool:
        validos = "0123456789()- ."
        for v in self.__number:
            if v not in validos:
                return False
        return True

    def __str__(self):
        return f"{self.__id}:{self.__number}"

class Contact():
    def __init__(self, name: str):
        self.__name = name
        self.__fone: list[Fone] = []
        self.__favorited = False

    def getName(self):
        return self.__name
    
    def getFone(self):
        return self.__fone

    def toggleFavorited(self):
        self.__favorited = not self.__favorited
    
    def getFavorited(self):
        return self.__favorited
    
    def isFavorited(self):
        return self.__favorited
    
    def setName(self, name: str):
        self.__name = name

    def addFone(self, id: str, number: str):
        fone = Fone(id, number)
        if fone.isValid():
            self.__fone.append(fone)
        else:
            raise Exception(f"Telefone invalido: {number}")
    
    def rmFone(self, index: int):
        if 0 <= index < len(self.__fone):
            self.__fone.pop(index)

    def __str__(self):
        fones_str = ", ".join([str(f) for f in self.__fone])
        fav = "@" if self.__favorited else "-"
        return f"{fav} {self.__name} [{fones_str}]"
    
class Agenda():
    def __init__(self):
        self.__contacts: list[Contact] = []

    def getContacts(self):
        return self.__contacts
    
    def findPosByName(self, name: str) -> int:
        i = 0
        for contact in self.__contacts:
            if contact.getName() == name:
                return i
            i += 1
        return -1
    
    def addContact(self, name: str, fones: list[Fone]):
        pos = self.findPosByName(name)
        if pos != -1:
            contact = self.__contacts[pos]
            for fone in fones:
                try:
                    contact.addFone(fone.getId(), fone.getNumber())
                except Exception as e:
                    print(f"Erro ao adicionar fone: {e}")
        else:
            contact = Contact(name)
            self.__contacts.append(contact)
            for fone in fones:
                try:
                    contact.addFone(fone.getId(), fone.getNumber())
                except Exception as e:
                    print(f"Erro ao adicionar fone: {e}")
            self.__contacts.sort(key=lambda c: c.getName())
    
    def getContact(self, name: str): 
        pos = self.findPosByName(name)
        return self.__contacts[pos] if pos != -1 else None
    
    def rmContact(self, name: str):
        for i, contact in enumerate(self.__contacts):
            if contact.getName() == name:
                self.__contacts.pop(i)
                return
        print("fail: contato não encontrado")  
    
    def search(self, pattern: str):
        results = []
        for contact in self.__contacts:
            if pattern.lower() in str(contact).lower():
                results.append(contact)
        return results
    
    def getFavorited(self):
        return [c for c in self.__contacts if c.isFavorited()]

    def __str__(self):
        return "\n".join([str(c) for c in self.__contacts])
    
def main():
    agenda = Agenda()

    while True:
        line = input()
        print("$" + line)
        args = line.split(" ")

        try:
            if args[0] == "end":
                break
        
            elif args[0] == "show":
                print(agenda)

            elif args[0] == "add":
                name = args[1]
                fones = []
                for fone_str in args[2:]:
                    if ":" in fone_str:
                        id, number = fone_str.split(":", 1)
                        fones.append(Fone(id, number))
                agenda.addContact(name, fones)

            elif args[0] == "rmFone":
                try:
                    name = args[1]
                    index = int(args[2])
                    contact = agenda.getContact(name)
                    if contact:
                        contact.rmFone(index)
                    else:
                        print("fail: contato não encontrado")
                except IndexError:
                    print("fail: uso: rmFone <nome> <indice>")
            
            elif args[0] == "rm":
                agenda.rmContact(args[1])
        
            elif args[0] == "search":
                results = agenda.search(args[1])
                for r in results:
                    print(r)

            
            elif args[0] == "tfav":
                contact = agenda.getContact(args[1])
                if contact:
                    contact.toggleFavorited()
                else:
                    print("fail: contato não encontrado")

            
            elif args[0] == "favs": 
                favs = agenda.getFavorited()
                for f in favs:
                    print(f)

            else:
                print("fail: comando invalido")

        except Exception as e:
            print(e)

main()

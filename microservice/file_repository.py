class FileRepository:
    fileName = ""

    def __init__(self, fileName) -> None:
        self.fileName = fileName

    def readFile(self):
        with open(self.fileName, mode="r") as f:
            return f.read()

    def writeFile(self, contents):
        with open(self.fileName, mode="w") as f:
            f.write(contents)


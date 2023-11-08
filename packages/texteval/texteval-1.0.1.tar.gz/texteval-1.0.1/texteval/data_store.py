
class Data_Store:
    data_store = ""
    data = ""

    def __init__(self, ) -> None:
        pass 

    @property
    def current_store(self):
        print(f"Current data store :: {self.data_store}")

    # parse pdf documents and extract text as string
    def parse_pdf(self, file_path: str, pdf_byte: bytes, is_scanned: False):
        print(f"PDF parser")
        
    

class Elastic_store(Data_Store):
    def __init__(self) -> None:
        super().__init__()
        self.data_store = 'elasticsearch'

class Weaviate_store(Data_Store):
    def __init__(self) -> None:
        super().__init__()
        self.data_store = 'weaviate'

Elastic_store().parse_pdf()
class CheckBox:
    def __init__(self,fieldName,value="",status=False,corr=[]) -> None:
        self.fieldName = fieldName
        self.value = value
        self.status = status
        self.corr = corr
    
    def get(self,fieldName):
        try:
            return self.fieldName
        except Exception as e:
            print(f'{self} does not have attribute {fieldName}')
    
    def get(self,value):
        try:
            return self.value
        except Exception as e:
            print(f'{self} does not have attribute {value}')

    def get(self,status):
        try:
            return self.status
        except Exception as e:
            print(f'{self} does not have attribute {status}')
    
    def get(self,corr):
        try:
            return self.corr
        except Exception as e:
            print(f'{self} does not have attribute {corr}')
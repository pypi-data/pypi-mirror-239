import re

class Validations:

        def email_validations(self, email):
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$")
            if EMAIL_REGEX.match(email):
                return True
            else:
                return False
            
        def password_validation(Self, password):
            PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
            if PASSWORD_REGEX.match(password):
                return True
            else: False

        def empty_validation(self, obj):
            for key, value in obj:
                if value == "":
                    return False
                
        def login_validation(Self,user):
            if user.is_active == True:
                return True
            else:
                return False
            
        def User_delete_validation(self, user):
            if user.is_deleted == True:
                return True
            else:
                return False
        
        def None_validation(self,*args):
            for i in args:
                if i == None:
                    return True
                
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self, username, password=None, phone_number=None, **extra_fields):
        
        if not phone_number:
            raise ValueError("Phone number is required")
        
        user=self.model(phone_number=phone_number, username=username, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_active' , True)

        return self.create_user(username, password, phone_number, **extra_fields)

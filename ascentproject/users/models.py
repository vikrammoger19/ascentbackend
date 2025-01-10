from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True, unique=True)  # Custom user_id
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    user_type = models.CharField(max_length=50, null=False)
    assigned_entities = models.TextField(null=True, blank=True)  # Assuming it's a JSON or text field
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Phone number field (optional)

    class Meta:
        db_table = "users"
        managed=False

    def _str_(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.user_id:
            # Get the last user record, or set the initial value to 0 if no records exist
            last_user = User.objects.all().order_by('user_id').last()
            if last_user:
                last_id = int(last_user.user_id[1:])  # Remove 'U' and convert to integer
                new_id = last_id + 1
            else:
                new_id = 1
            self.user_id = f'U{new_id:03d}'  # Format the ID like U001, U002, ...
        
        super(User, self).save(*args, **kwargs)


# Organization model
class Organization(models.Model):
    # organization_id = models.AutoField(primary_key=True)
    organization_id = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # Specifying the column name
    products = models.ManyToManyField('Product', related_name='organizations')  # Many-to-Many relationship with Product

    class Meta:
        db_table = "organizations"
        managed=False
        

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a custom organization ID.
        """
        if not self.organization_id:  # Only set custom ID if not already set
            # Get the latest organization ID to increment it
            last_org = Organization.objects.aggregate(Max('organization_id'))['organization_id__max']
            
            if last_org:
                # Extract the number part of the last organization_id (assuming format org_XXXX)
                last_number = int(last_org.split('_')[1])
                new_number = last_number + 1
            else:
                new_number = 1  # If no organizations exist, start from 1

            # Create the new organization_id in the format 'org_XXXX'
            self.organization_id = f"org_{new_number:04d}"  # Zero-padded to 4 digits

        super().save(*args, **kwargs)

    def _str_(self):
        return self.name

    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Explicit primary key
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.name

    class Meta:
        db_table = "products"
        managed=False


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  # Explicit primary key
    role_name = models.CharField(max_length=50, null=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="roles",
        db_column="product_id",
    )

    def _str_(self):
        return self.role_name

    class Meta:
        db_table = "roles"
        managed=False
      



class Entities(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=100)
    entity_desc = models.TextField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='entities')
    formatted_entity_id = models.CharField(max_length=15, unique=True, blank=True)

    class Meta:
        db_table = 'entity'
        managed=False
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.formatted_entity_id:
            self.formatted_entity_id = f"ENTITY{self.entity_id:05d}"
            super().save(update_fields=['formatted_entity_id'])

    def _str_(self):
        return self.entity_name
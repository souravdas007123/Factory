from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# ==========================================
# 1. HR & Employee Module
# ==========================================
class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "01. Department"
            verbose_name_plural = "01. Department"

class Employee(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Production Manager'),
        ('SUPERVISOR', 'Floor Supervisor'),
        ('MACHINE_OPERATOR', 'Worker'),
        ('INVENTORY_CLERK', 'Store Keeper'),
        ('WAREHOUSE_HEAD', 'Store Manager'),
        ('QUALITY_MANAGER', 'Quality Manager'),
        ('QUALITY_INSPECTOR', 'Quality Inspector'),
        ('PROCUREMENT', 'Purchase Manager'),
        ('MAINTENANCE_ENGINEER', 'Technician'),
        ('SALES_EXECUTIVE', 'Sales Executive'),
        ('DISPATCH_COORDINATOR', 'Dispatch Coordinator'),
        ('HR_EXECUTIVE', 'HR Executive'),
        
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
            verbose_name = "02. Employee"
            verbose_name_plural = "02. Employee"

# ==========================================
# 2. Inventory Module (Raw & Finished)
# ==========================================
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "03. Supplier"
            verbose_name_plural = "03. Supplier"

class Item(models.Model):
    ITEM_TYPES = (
        ('RAW', 'Raw Material'),
        ('FINISHED', 'Finished Good'),
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True) # Stock Keeping Unit
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    unit_of_measure = models.CharField(max_length=20) # kg, liters, pieces
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.item_type})"

    class Meta:
            verbose_name = "04. Item"
            verbose_name_plural = "04. Item"

# ==========================================
# 3. Production & Manufacturing Module
# ==========================================
class Machine(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('INACTIVE', 'Inactive'),
    )
    name = models.CharField(max_length=100)
    machine_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "05. Machine"
            verbose_name_plural = "05. Machine"

class ProductionOrder(models.Model):
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('QC_PENDING', 'QC Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    order_number = models.CharField(max_length=50, unique=True)
    product_to_build = models.ForeignKey(Item, on_delete=models.CASCADE, limit_choices_to={'item_type': 'FINISHED'})
    quantity_to_build = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    assigned_machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        # FIX 3: Check agar product_to_build exist hi nahi karta (form incomplete ho)
        if not hasattr(self, 'product_to_build') or self.product_to_build is None:
            return # Django automatically "This field is required" error dega

        # FIX 2: Stock check sirf naye order banate waqt hona chahiye (not self.pk means New Object)
        if not self.pk and self.status == 'PLANNED':
            bom_items = self.product_to_build.bom_items.all()
            
            if not bom_items.exists():
                raise ValidationError(
                    f"{self.product_to_build.name} ka koi Bill of Materials (BOM) nahi mila. Pehle BOM set karein."
                )

            for bom in bom_items:
                total_required_qty = bom.quantity_required * self.quantity_to_build
                
                if bom.raw_material.current_stock < total_required_qty:
                    raise ValidationError(
                        f"Stock Error: {bom.raw_material.name} ka stock kam hai! "
                        f"Required: {total_required_qty} {bom.raw_material.unit_of_measure}, "
                        f"Available: {bom.raw_material.current_stock} {bom.raw_material.unit_of_measure}."
                    )

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.product_to_build.name}"

    class Meta:
        verbose_name = "07. Production Order"
        verbose_name_plural = "07. Production Orders"




class BillOfMaterials(models.Model):
    """Ek finished good banane ke liye kya kya raw material chahiye"""
    # FIX 1: blank=True, null=True hata diya gaya hai.
    finished_good = models.ForeignKey(Item, related_name='bom_items', on_delete=models.CASCADE, limit_choices_to={'item_type': 'FINISHED'})
    raw_material = models.ForeignKey(Item, on_delete=models.CASCADE, limit_choices_to={'item_type': 'RAW'})
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_required} {self.raw_material.unit_of_measure} for {self.finished_good.name}"

    class Meta:
        verbose_name = "06. Bill of Materials"
        verbose_name_plural = "06. Bill of Materials"
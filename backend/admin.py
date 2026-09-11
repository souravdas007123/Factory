from django.contrib import admin
from .models import Department, Employee, Supplier, Item, Machine,ProductionOrder,BillOfMaterials
# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'department', 'role', 'phone')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__email', 'phone')  

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):      
    list_display = ('id', 'name', 'contact_person', 'phone', 'address')
    search_fields = ('name', 'contact_person', 'phone')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):  
    list_display = ('id', 'name', 'sku', 'item_type', 'unit_of_measure', 'current_stock', 'supplier')
    search_fields = ('name', 'sku')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'machine_code', 'status')
    search_fields = ('name', 'machine_code')


@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'product_to_build', 'quantity_to_build', 'status', 'assigned_machine', 'supervisor', 'start_date', 'end_date')
    search_fields = ('order_number', 'product_to_build')


@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'finished_good', 'raw_material', 'quantity_required')
    search_fields = ('finished_good',)       



     

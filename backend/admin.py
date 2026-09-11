from django.contrib import admin
from .models import Department, Employee, Supplier, Item, Machine, ProductionOrder, BillOfMaterials, Bom
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

# 1. Pehle Inline banayein
class BillOfMaterialsInline(admin.TabularInline):
    model = BillOfMaterials
    fk_name = 'finished_good'
    extra = 1  

# 2. Inline ko 'Item' ke andar daalein
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):  
    list_display = ('id', 'name', 'sku', 'item_type', 'unit_of_measure', 'current_stock', 'supplier')
    search_fields = ('name', 'sku')
    list_filter = ('item_type',)
    inlines = [BillOfMaterialsInline] # <--- YAHAN SAHI JAGAH HAI

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'machine_code', 'status')
    search_fields = ('name', 'machine_code')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'product_to_build', 'quantity_to_build', 'status', 'assigned_machine', 'supervisor', 'start_date', 'end_date')
    search_fields = ('order_number', 'product_to_build')
    list_filter = ('status',)

# Bom model ki waise koi zarurat nahi hai, par agar aapne banaya hai toh ise simple register kar dein (bina inline ke)
@admin.register(Bom)
class BomAdmin(admin.ModelAdmin):  
    list_display = ('id', 'name')
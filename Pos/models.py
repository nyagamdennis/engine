from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone


class Material(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Color(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name   
    
class StockProperty(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    num_of_rolls = models.IntegerField()
    size = models.DecimalField(max_digits=1000, decimal_places=2)  # Use DecimalField for precise decimal calculations
    extrasize = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)  # Use DecimalField for precise decimal calculations
    total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)  # Use DecimalField for total
    date_added = models.DateTimeField(auto_now_add=True)
    date_stocked = models.DateField()
    buying_price = models.IntegerField()
    
     
    
    def __str__(self):
        return f'{self.material.name} {self.color.name}'
    
    
    
class ProductSize(models.Model):
    size = models.CharField(max_length=50, null=True, blank=True)
    alphabetic_size = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.size
    
  
class Product(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class ProductPro(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.product.name
    
class Employees(models.Model):
    id_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField()
    gender = models.CharField(max_length=200)
    date_employed = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
    
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductPro, on_delete=models.CASCADE)
    mode_of_payment = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    to_be_delivered_to = models.CharField(max_length=200, null=True, blank=True)
    no_to_be_delivered = models.IntegerField(null=True, blank=True)
    fully_payed = models.BooleanField(default=True)
    deposited = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.customer.name} bought {self.product.product.name}'
   

# class Sales(models.Model)


class Deposits(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    date = models.DateField()

    def __str__(self):
        return f'{self.cart.customer} deposited {self.amount} on {self.date}'

    
class Advances(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='advances')
    amount = models.IntegerField()
    date_issued = models.DateTimeField()
    date_given = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.employee.first_name}'
    
    
class Expenses(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    expence_name = models.CharField(max_length=200)
    amount = models.IntegerField()
    date_issued = models.DateTimeField()
    reset = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.employee.first_name} {self.expence_name}'
    

class ProjectName(models.Model):
    name = models.CharField(max_length=1000)
    product = models.CharField(max_length=200)
    product_size = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name




class Task(models.Model):
    project = models.ForeignKey(ProjectName, on_delete=models.CASCADE, related_name='project')
    task_name = models.TextField()
    estimated_pay = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    task_completed = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    due_date_time = models.DateTimeField()
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')


    def __str__(self):
        return self.project.name
    

class ProjectMaterial(models.Model):
    # task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="materials")
    project = models.ForeignKey(ProjectName, on_delete=models.CASCADE, related_name="materials")
    material_to_use = models.ForeignKey(StockProperty, on_delete=models.CASCADE)
    material_size = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.project.name} - {self.material_to_use.material}"
    

    
class WorkInProgress(models.Model):
    # task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockProperty,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    product_size = models.IntegerField(null=True, blank=True)
    size = models.DecimalField(max_digits=5, decimal_places=2) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    productQuantity = models.IntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.employee.first_name} is making {self.product_name}'




class SalesAnalytics(models.Model):
    month = models.IntegerField() # You can also use DateField to group by month.
    year = models.IntegerField()
    total_sales_amount = models.DecimalField(decimal_places=2, max_digits=115, default=0.00)
    cash_sales = models.DecimalField(decimal_places=2, max_digits=115, default=0.00)
    number_of_orders = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sales for {self.month}/{self.year}: {self.total_sales_amount}'
    

    @staticmethod
    def update_monthly_sales():
        """
        Method to calculate and update sales analytics.
        This can be scheduled to run monthly or whenever needed.
        """
        current_year = timezone.now().year
        current_month = timezone.now().month

        carts = Cart.objects.filter(
            date__year=current_year,
            date__month=current_month
        )

        

        # Calculate the number of orders for the month
        total_sales = 0
        cash_sales = 0
        number_of_orders = carts.count()

        for cart in carts:
            if cart.fully_payed:
                # For fully paid orders, use product price * quantity
                cart_total = cart.product.price * cart.quantity
                total_sales += cart_total
                cash_sales += cart_total
            else:
                # For partially paid orders, use the deposited amount
                total_sales += cart.deposited or 0
                cash_sales += cart.deposited or 0


        # Update or create the record
        sales, created = SalesAnalytics.objects.get_or_create(
            month=current_month,
            year=current_year,
            defaults={
                'total_sales_amount': total_sales,
                'cash_sales': total_sales,  # Set initial cash sales
                'number_of_orders': number_of_orders  # Store the number of orders
            }
        )

        # If the record exists, update it
        if not created:
            sales.total_sales_amount = total_sales
            sales.cash_sales = total_sales  # Update cash sales
            sales.number_of_orders = number_of_orders  # Update the number of orders
            sales.save()




@receiver(post_save, sender=Cart)
def update_sales_analytics(sender, instance, created, **kwargs):
    if instance.fully_payed:  # Only update analytics for fully paid sales (cash sales)
        SalesAnalytics.update_monthly_sales()




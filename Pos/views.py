from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView





from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        # token['first_name'] = user.first_name
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


def get_fast_moving_products():
    # Calculate the date one month ago from today
    one_month_ago = datetime.now() - timedelta(days=30)
    
    # Query fast-moving products based on your criteria
    fast_moving_products = ProductPro.objects.annotate(
        total_quantity_sold=Sum('quantity', filter=models.Q(cart__delivered=True, cart__date__gte=one_month_ago))
    ).order_by('-total_quantity_sold')[:10]  # Get the top 10 fast-moving products

    return fast_moving_products




@api_view(['GET'])
def sales_analysis(request):
    sales = SalesAnalytics.objects.all()
    serializer = SalesAnalysisSerializer(sales, many=True)
    return Response(serializer.data)



@api_view(['POST', 'GET'])
def all_products(request):
    product = ProductPro.objects.order_by('-date_added')
    serialize = ProductPropSerializer(product, many=True)
    return Response(serialize.data)



# @api_view(['POST', 'GET'])
# def all_prods(request):
#     product = Product.objects.order_by('-date_added')
#     serialize = ProductAndDetailsSerializer(product, many=True)
#     return Response(serialize.data)
@api_view(['POST', 'GET'])
def all_prods(request):
    try:
        # Fetching products and ordering them by 'date_added'
        product = Product.objects.order_by('-date_added')
        serialize = ProductAndDetailsSerializer(product, many=True)

        # Return successful response with a status code of 200 (OK)
        return Response(serialize.data, status=status.HTTP_200_OK)
    
    except Product.DoesNotExist:
        # Return a 404 response if no products are found
        return Response({"error": "Products not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        # Catch any other exceptions and return a 500 (Internal Server Error)
        print('eeror is ', str(e))
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def check_product_exists(request):
    product_name = request.query_params.get('name')
    if product_name:
        exists = Product.objects.filter(name__iexact=product_name).exists()
        return Response({'exists': exists})
    return Response({'exists': False})


@api_view(['POST', 'GET'])
def all_productsNames(request):
    product = Product.objects.all()
    serialize = ProductSerializer(product, many=True)
    return Response(serialize.data)


@api_view(['POST', 'GET'])
def all_colors(request):
    color = Color.objects.all()
    serialize = ColorSerializer(color, many=True)
    return Response(serialize.data)



@api_view(['POST', 'GET'])
def all_material(request):
    material = Material.objects.all()
    serialize = MaterialSerializer(material, many=True)
    return Response(serialize.data)

class CreateProjectView(APIView):
    def post(self, request, *args, **kwargs):
        print('This is the data ', request.data)
        serializer = CreateProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()  # This creates the project and saves it
            print('Project created: ', project)

            # Serialize the project instance to include nested materials
            response_serializer = CreateProjectSerializer(project)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        print('This is the error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CreateProjectView(APIView):
#     def post(self, request, *args, **kwargs):
#         print('This is the data ', request.data)
#         serializer = CreateProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # This calls the create method of the serializer
#             print('jj ', serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print('This is the error ', serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllProjects(APIView):
    def get(self, request):
        project = ProjectName.objects.all()
        serialize = ProjectSerializer(project, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
        # ProjectName

class CreateTaskView(APIView):
    def post(self, request, *args, **kwargs):
        print('This is the data ', request.data)
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This calls the create method of the serializer
            print('later data ', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('This is the error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def all_productsize(request):
    pro_size = ProductSize.objects.all()
    serialize = MaterialSizeSerializer(pro_size, many=True)
    return Response(serialize.data)



@api_view(['POST', 'GET'])
def all_emplyees(request):
    employee = Employees.objects.order_by('-date_added')
    serialize = EmployeeSerializer(employee, many=True)
    return Response(serialize.data)


@api_view(['PUT'])
def update_task(request, pk):
    print('Updates ', request.data)
    task = Task.objects.get(pk=pk)
    serializer = updateTaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print('serializer data ', serializer.data)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST', 'GET'])
def single_emplyee(request, pk):
    employee = Employees.objects.get(pk=pk)
    serialize = EmployeeSerializer(employee)
    return Response(serialize.data)



@api_view(['POST', 'GET'])
def all_cart(request):
    cart = Cart.objects.order_by('-date')
    serialize = CartSerializer(cart, many=True)
    return Response(serialize.data)



@api_view(['POST', 'GET'])
def all_customers(request):
    customer = Customer.objects.order_by("-date_added")
    serialize = CustomerSerializer(customer, many=True)
    return Response(serialize.data)



@api_view(['POST', 'GET'])
def all_stock_prop(request):
    stock = StockProperty.objects.order_by('-date_added')
    serialize = StockPropertySerializer(stock, many=True)
    return Response(serialize.data)


@api_view(['POST', 'GET'])
def all_on_work(request):
    works = WorkInProgress.objects.all()
    serialize = WorkInProgressSerializer(works, many=True)
    return Response(serialize.data)



@api_view([ 'GET'])
def all_expenses(request):
    expenses = Expenses.objects.order_by('-date_posted')
    serialize = ExpensesSerializer(expenses, many=True)
    return Response(serialize.data)


@api_view(['POST'])
def create_or_update_expenses(request):
    print('this is the request data ', request.data)
    serializer = AddExpensesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_advances(request):
    serializer = AddAdvancesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print('advance ', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def create_or_update_cart(request):
    cart_data = request.data
    product_id = cart_data['product']
    cart_quantity = int(cart_data['quantity'])
    
    
    product = ProductPro.objects.get(id=product_id)
    product_quantity = int(product.quantity)
    
    if cart_quantity >= 0:
        if cart_quantity <= product_quantity:
            remaining_product_quantity = product_quantity - cart_quantity
            ProductPro.objects.filter(id=product_id).update(quantity=remaining_product_quantity)    
            serializer = CartCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print('response data is ', serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('errors ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Cart quantity exceeds product quantity.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid cart quantity.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def add_deposit(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)

    # Extract the new deposit amount from the request data
    new_deposit = request.data.get('deposit')
    if new_deposit is None or float(new_deposit) <= 0:
        return Response({'error': 'Invalid deposit amount'}, status=400)

    try:
        # Convert the deposit amount to a decimal for precision
        new_deposit = Decimal(new_deposit)
    except InvalidOperation:
        return Response({'error': 'Invalid deposit amount format'}, status=400)

    # Add the new deposit to the already present deposit amount
    if cart.deposited is None:
        cart.deposited = Decimal(0)
    cart.deposited += new_deposit

    # Calculate the total price of the products in the cart
    total_price = cart.product.price * cart.quantity

    # Check if the total deposit equals or exceeds the total price
    if cart.deposited >= total_price:
        cart.fully_payed = True
    else:
        cart.fully_payed = False

    # Save the updated cart information
    cart.save()

    # Return the updated cart data
    serializer = CartDepositSerializer(cart)
    print('Return data ', serializer.data)
    return Response(serializer.data, status=200)


@api_view(['PUT'])
def update_cart(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)

    serializer = CartSerializer(cart, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE']) 
def deleteCart(request ,pk):
    print('Cart id is ', pk)
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)
    
    print('Cart data is ', cart)
    # product_pro = get_object_or_404(ProductPro, product=cart.product)
    product_pro = cart.product

    product_pro.quantity += cart.quantity
    product_pro.save()

    if cart.fully_payed:
        sales_analytics = SalesAnalytics.objects.filter(month=cart.date.month,year=cart.date.year).first()
        if sales_analytics:
            # Subtract the deleted cart's sales from the analytics
            sales_analytics.total_sales_amount -= cart.deposited
            sales_analytics.cash_sales -= cart.deposited
            sales_analytics.number_of_orders -= 1
            
            # If no orders are left for the month, delete the analytics
            if sales_analytics.number_of_orders <= 0:
                sales_analytics.delete()
            else:
                sales_analytics.save()

    # Delete the cart
    cart.delete()

    return Response({"message": "Cart deleted and product quantity updated"}, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
def update_work(request, pk):
    try:
        work = WorkInProgress.objects.get(pk=pk)
    except WorkInProgress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = WorkInProgressSerializer(work, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['PUT'])
def reset_expense(request, pk):
    try:
        expense = Expenses.objects.get(pk=pk)
    except Expenses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExpensesSerializer(expense, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    


@api_view(['POST'])
def create_product(request):
    serializer = CreateProductSerializer(data=request.data)
    print('data is ', request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('this is the error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def add_product(request):
    serializer = AddProductSerializer(data=request.data)
    data=request.data
    print('This is data post ', data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('this is the error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def add_product_pro(request):
    serializer = AddProductProSerializer(data=request.data)
    data=request.data
    print('This is the data ', data)
    if serializer.is_valid():
        serializer.save()
        print('this is the payload ', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('this is the error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def create_progress(request):
    serializer = CreateProgressSerializer(data=request.data)
    if serializer.is_valid():
        try:
            employee = serializer.validated_data['employee']
            stock = serializer.validated_data['stock']
            size = serializer.validated_data['size']

            # Determine the number of rolls based on the size
            if size > 0:
                num_of_rolls = stock.total / size
                stock.num_of_rolls = int(num_of_rolls)  # Round down to the nearest integer
            else:
                stock.num_of_rolls = 0  # If size is 0, set rolls to 0

            # Deduct the used size
            stock.total -= size

            # Update the size based on the remaining rolls
            if stock.num_of_rolls > 0:
                stock.size = stock.total / stock.num_of_rolls
            else:
                stock.size = 0  # If no rolls are left, set size to 0

            # Save the updated StockProperty
            stock.save()

            # Create the WorkInProgress instance after updating the stock
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle any exceptions and return an error response
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Handle serializer validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['POST'])
def create_stock(request):
    
    the_data = request.data
    num_rolls = the_data['num_of_rolls']
    role_size = the_data['size']
    
    
    total = int(num_rolls) * float(role_size)
    request.data['total'] = total
    
    serializer = CreateStockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print('This is data ', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('This is the error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    
@api_view(['POST'])
def create_employee(request):
    serializer = CreateEmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('This is the error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def delete_employee(request, pk):
    print('employee ', request.data)
    try:
        employee = Employees.objects.get(pk=pk)
        print('Employee found ', employee)
    except Employees.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_employee(request, pk):
    try:
        employee = Employees.objects.get(pk=pk)
    except Employees.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def update_product(request, pk):
    print('PK ', pk)
   
    try:
        product = Product.objects.get(pk=pk)
        
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
    serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    print('Error is ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product_pro(request, pk):
    print('data ', request.data)
    try:
        productpro = ProductPro.objects.get(pk=pk)        
    except ProductPro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    serializer = ProductPropUpdateSerializer(productpro, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Re-fetch the updated object to return full material, color, size details
        productpro.refresh_from_db()  # Refresh the instance with the latest data
        updated_serializer = ProductPropUpdateSerializer(productpro)  # Use the serializer to serialize the updated object
        
        return Response(updated_serializer.data, status=status.HTTP_200_OK)
    print('Updated data ', updated_serializer.data)
    print('Error is ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def update_product_pro_quantity(request, pk):
    print('data ', request.data)
    try:
        productpro = ProductPro.objects.get(pk=pk)        
    except ProductPro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    serializer = ProductPropAddQuantitySerializer(productpro, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Re-fetch the updated object to return full material, color, size details
        productpro.refresh_from_db()  # Refresh the instance with the latest data
        updated_serializer = ProductPropAddQuantitySerializer(productpro)  # Use the serializer to serialize the updated object
        
        return Response(updated_serializer.data, status=status.HTTP_200_OK)
    print('Updated data ', updated_serializer.data)
    print('Error is ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def update_stock(request, pk):
    try:
        stock = StockProperty.objects.get(pk=pk)
    except StockProperty.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Perform the arithmetic operation
    num_of_rolls = float(request.data.get('num_of_rolls'))
    size = float(request.data.get('size'))
    extrasize = request.data.get('extrasize')
    
    
    if num_of_rolls is not None and size is not None:
        new_total = num_of_rolls * size
        total = float(new_total) + float(stock.total)  # Add the new total to the current total
        request.data['total'] = total
       
        
        
        new_roll = num_of_rolls + stock.num_of_rolls
        print('New rolls ', new_roll)
        new_size = float(size) + float(stock.size)  # Add the new size to the current size
        print('new size ', new_size)
        request.data['size'] = new_size
        request.data['num_of_rolls'] = new_roll
       

    serializer = StockPropUpdateSerializer(stock, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        print('Returned data ', serializer.data)
        return Response(serializer.data)
    print('Error is ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_all_stock(request, pk):
    try:
        stocks = StockProperty.objects.get(pk=pk)        
    except stocks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    print('new data ', request.data)
    serializer = AllStockSerializer(stocks, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Re-fetch the updated object to return full material, color, size details
        stocks.refresh_from_db()  # Refresh the instance with the latest data
        updated_serializer = AllStockSerializer(stocks)  # Use the serializer to serialize the updated object
        print('updated stock ', updated_serializer.data)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)
    # print('Updated data ', updated_serializer.data)
    print('Error is ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_all_stock(request, pk):
    try:
        stocks = StockProperty.objects.get(pk=pk)        
    except stocks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    stocks.delete()
    # Return a success response with 204 NO CONTENT status
    return Response(status=status.HTTP_204_NO_CONTENT)
  


@api_view(['POST'])
def user_registration(request):
    serializer = UserRegSerializer(data=request.data)
    print('The register data is ', request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('there is an error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_productpro(request, pk):
    print('This is pk ', pk)
    try:
        productpro = ProductPro.objects.get(pk=pk)
    except ProductPro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    productpro.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






class TaskManagement(APIView):
    def get(self, request):
        data = Task.objects.order_by('-date_created')
        serialize = TaskManagementSerializer(data, many=True)

        return Response(serialize.data)
    

class ProjectManagement(APIView):
    def get(self, request):
        data = ProjectName.objects.order_by('-date_created')
        serialize = ProjectNameSerializer(data, many=True)
        return Response(serialize.data)
    


class updateAdvances(APIView):
    def put(self, request, pk):
        try:
            advance = Advances.objects.get(pk=pk)
        except Advances.DoesNotExist:
            return Response({"error": "Advance not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate the incoming data
        serializer = AdvancesUpdatesSerilizer(advance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # Save the updated instance if valid
            print('data ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Return validation errors if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_advance(request, pk):
    try:
        advance = Advances.objects.get(pk=pk)
    except Advances.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    advance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['DELETE'])
# def delete_employee(request, pk):
#     print('employee ', request.data)
#     try:
#         employee = Employees.objects.get(pk=pk)
#         print('Employee found ', employee)
#     except Employees.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     employee.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

class task_completion(APIView):
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Advance not found."}, status=status.HTTP_404_NOT_FOUND)
        task_completed = request.data.get("task_completed")


        task_completed = request.data.get("task_completed")

        # Validate that task_completed is provided and is a valid integer
        if task_completed is None or not isinstance(task_completed, int) or task_completed < 0:
            return Response({"error": "Invalid value for task_completed."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the task fields
        task.task_completed = task_completed
        task.completed = task.task_completed >= task.quantity  # Mark as complete if `task_completed` >= `quantity`
        task.save()

        # Serialize the updated task and return it
        serializer = TaskSerializer(task)
        print('data ', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
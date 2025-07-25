import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from graphql import GraphQLError

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=True)

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        customer = Customer.objects.create(**input)
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []
        for data in input:
            try:
                customer = Customer.objects.create(**data)
                customers.append(customer)
            except Exception as e:
                errors.append(str(e))
        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        product = Product.objects.create(**input)
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
            products = Product.objects.filter(id__in=input.product_ids)

            total = sum(p.price for p in products)
            order = Order.objects.create(customer=customer, total_amount=total)
            order.products.set(products)
            return CreateOrder(order=order)
        except Exception as e:
            raise GraphQLError(str(e))

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        products = Product.objects.filter(stock__lt=10)
        for product in products:
            product.stock += 10
            product.save()
        return UpdateLowStockProducts(updated_products=products, message="Low stock products restocked.")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  

    updated_products = graphene.List(graphene.String)
    success = graphene.Boolean()

    def mutate(self, info):
        updated_products = []

        low_stock_products = Product.objects.filter(stock__lt=10)  # required check line

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(f"{product.name}: {product.stock}")

        return UpdateLowStockProducts(updated_products=updated_products, success=True)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()
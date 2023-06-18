from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.forms import modelform_factory
from .models import Inventory, Orders, Transaction
from django.contrib import messages
# Create your views here.


def home(request):
    products = Inventory.objects.all()

    total_profit = 0
    highest_cost = 0
    highest_profit = 0
    out_of_stock = []
    most_sold = 0
    for i in range(len(products)):

        #total profit
        total_profit += products[i].profit_earned
        # highest cost item
        if highest_cost < products[i].cost_price:
            highest_cost_item = products[i]
            highest_cost = products[i].cost_price
        # out of stock items
        if products[i].quantity == 0:
            out_of_stock.append(products[i])
        # item with highest profit
        if highest_profit < products[i].profit_earned:
            highest_profit = products[i].profit_earned
            highest_profit_item = products[i]
        if most_sold < products[i].quantity_sold:
            most_sold = products[i].quantity_sold
            most_sold_item = products[i]

    print(total_profit)
    print(highest_cost_item)
    print(out_of_stock)
    print(highest_profit_item)
    print(most_sold_item)
    # messages.warning(request, 'Welcome to Shopeo')
    data = {
        'products': products,
        'total_profit': total_profit,
        'out_of_stock': out_of_stock,
        'highest_profit_item': highest_profit_item,
        'most_sold_item': most_sold_item,
        'highest_cost_item': highest_cost_item
    }

    return render(request, 'home.html', data)


def show(request):
    products = Inventory.objects.all()
    print(products)
    return render(request, 'show.html', {'data': products})


def all_items(request):
    products = Inventory.objects.all()
    return render(request, 'items.html', {'data': products})


def view_item(request, id):
    data = get_object_or_404(Inventory, pk=id)
    return render(request, 'viewItem.html', {'dt': data})


def sell_item(request, id):
    if request.method == 'POST':
        qty = int(request.POST['qty'])
        stock_data = Inventory.objects.filter(id=id).values('quantity', 'quantity_sold', 'selling_price')
        print(type(qty), type(stock_data))
        stock_quantity = stock_data[0]['quantity']
        item_sold = stock_data[0]['quantity_sold']
        selling_price = stock_data[0]['selling_price']
        updated_stock = stock_quantity - qty
        item_sold_add = item_sold + qty
        print(item_sold, item_sold_add)
        print(updated_stock)
        if qty <= stock_quantity:
            Inventory.objects.filter(id=id).update(quantity=updated_stock, quantity_sold=item_sold_add)
            Inventory.objects.get(id=id).save()
            Transaction.objects.create(item=Inventory.objects.get(id=id), quantity=qty, selling_price=selling_price*qty)
            messages.success(request, 'Item Sold Successfully')
            return redirect(view_item, id)
        else:
            messages.warning(request, "Your Enter quantity must below stock qty.")
            return redirect(sell_item, id)
    else:
        item = get_object_or_404(Inventory, pk=id)
        return render(request, 'sellForm.html', {'item': item})


def new_item(request):
    ItemForm = modelform_factory(Inventory, exclude=['id', 'revenue', 'profit_earned'])
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Create Successfully")
    else:
        form = ItemForm()
    return render(request, 'new_item.html', {'form': form})


def order_item(request, id):
    OrderItem = modelform_factory(Orders, exclude=['id', 'order_date', 'is_received', 'is_cancel', 'order_cost'])
    if request.method == 'POST':
        form = OrderItem(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created')
    else:
        form = OrderItem()

    return render(request, 'order_item.html', {'form': form})


def edit_item(request, id):
    ItemForm = modelform_factory(Inventory, exclude=['id', 'revenue', 'profit_earned'])
    product = get_object_or_404(Inventory, pk=id)
    if request.method == 'GET':
        data = {'form': ItemForm(instance=product)}
        return render(request, 'edit_form.html', data)
    else:
        form = request.POST
        print(form)

        product.__dict__.update({'name': form['name'], 'iin': form['iin'], 'cost_price': float(form['cost_price']),
                                 'quantity': int(form['quantity']), 'quantity_sold': int(form['quantity_sold']),
                                 'selling_price': float(form['selling_price'])})
        product.save()
        messages.success(request, 'Changes has Saved')
        return redirect(view_item, id)


def show_order(request, id):
    orders = Orders.objects.filter(item=id, is_received=False, is_cancel=False)
    return render(request, 'showOrder.html', {'orders': orders})


def receive_order(request, id):
    o = Orders.objects.get(id=id)
    o.is_received = True
    print(o.item.quantity)
    o.item.quantity = o.item.quantity + o.quantity
    print(o.item.quantity)
    o.item.save()
    o.save()
    return redirect(show_order, o.item.id)


def cancel_order(request, id):
    Orders.objects.filter(id=id).update(is_cancel=True)
    item_id = Orders.objects.get(id=id).item.id
    return redirect(show_order, item_id)


def received_orders(request, id):
    orders = Orders.objects.filter(is_received=True)
    data = []
    for order in orders:
        if order.item.id == id:
            data.append(order)
    print(data)
    return render(request, 'show_received.html', {'data': data})


def cancelled_orders(request, id):
    orders = Orders.objects.filter(is_cancel=True)
    data = []
    for order in orders:
        if order.item.id == id:
            data.append(order)
    print(data)
    return render(request, 'show_cancelled.html', {'data': data})


def sold_items(request, id):
    data = Transaction.objects.all()
    trans = []
    for dt in data:
        if dt.item.id == id:
            trans.append(dt)
    return render(request, 'show_sold.html', {'trans': trans})


from django.shortcuts import redirect, render, get_object_or_404
from cinema.models import Product, Screening, Seat#, Extra
from extras.models import Extra
from .models import Cart, MovieCartItem, ExtraCartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
from order.models import Order, OrderItem
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal
import stripe


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def movie_add_cart(request, screening_id):
    screening = get_object_or_404(Screening, pk=screening_id)
    product = screening.movie
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = MovieCartItem.objects.get(product=product, screening=screening, cart=cart)
        cart_item.save()
    except MovieCartItem.DoesNotExist:
        cart_item = MovieCartItem.objects.create(product=product, screening=screening, cart=cart, numSeats = 0)
        cart_item.save()

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')

        if selected_seats == []:
            return redirect('.')
        else:
            for seat_id in selected_seats:
                seat = Seat.objects.get(number=seat_id, screening=screening)
                seat.is_available = False
                seat.save()
                cart_item.seats.add(seat)
                cart_item.numSeats +=1
            cart_item.save()
            cart.save()
            return redirect('extras:all_extras')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def extra_add_cart(request, extra_id):
    extra = Extra.objects.get(id=extra_id)
    #extra = get_object_or_404(Extra, pk=extra_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = ExtraCartItem.objects.get(extra=extra, cart=cart)
        if cart_item.quantity < cart_item.extra.stock:
            cart_item.quantity += 1
        cart_item.save()
    except ExtraCartItem.DoesNotExist:
        cart_item = ExtraCartItem.objects.create(extra=extra, quantity=1, cart=cart)
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def extra_cart_remove(request, extra_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    extra = get_object_or_404(Extra, id=extra_id)
    cart_item = ExtraCartItem.objects.get(extra=extra, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def extra_full_remove(request, extra_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    extra = get_object_or_404(Extra, id=extra_id)
    cart_item = ExtraCartItem.objects.get(extra=extra, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

def movie_full_remove(request, screening_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    screening = get_object_or_404(Screening, pk=screening_id)
    product = screening.movie
    cart_item = MovieCartItem.objects.get(product=product, screening=screening, cart=cart)
    for seat in cart_item.seats.all():
        seat.is_available = True
        seat.save()
    cart_item.delete()
    return redirect('cart:cart_detail')



def cart_detail(request, total_ori=0, total=0, counter=0, movie_cart_items = None, extra_cart_items = None):

    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None


    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        movie_cart_items = MovieCartItem.objects.filter(cart=cart, active=True)
        extra_cart_items = ExtraCartItem.objects.filter(cart=cart, active=True)
        for cart_item in movie_cart_items:
            total += (cart_item.numSeats * 10)
            counter += 1
        for cart_item in extra_cart_items:
            total += (cart_item.extra.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'Movies@TUD - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    voucher_apply_form = VoucherApplyForm()

    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if Voucher != None:
            discount = (total*(voucher.discount/Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except:
        ObjectDoesNotExist
        pass

    empty = False
    if not movie_cart_items and not extra_cart_items:
        empty = True

    total_ori = total_ori + total

    if voucher != None:
        discount = (total*(voucher.discount/Decimal('100')))
        total = (total - discount)

    context = {'movie_cart_items':movie_cart_items, 'extra_cart_items':extra_cart_items, 'total':total, 'total_ori':total_ori, 'empty':empty, 
                'counter':counter, 'data_key':data_key, 'stripe_total':stripe_total, 'description':description, 'voucher_apply_form': voucher_apply_form, 'new_total':new_total, 'voucher':voucher, 'discount':discount}

    if request.method == 'POST':
        print(request.POST)    
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingcity = request.POST['stripeShippingAddressCity']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            customer = stripe.Customer.create(email=email, source=token)
            stripe.Charge.create(amount=stripe_total, currency="eur", description=description, customer=customer.id)
        except stripe.error.CardError as e:
            return e

        try:
            order_details = Order.objects.create(
                    token = token,
                    total = total,
                    emailAddress = email,
                    billingName = billingName,
                    billingAddress1 = billingAddress1,
                    billingCity = billingcity,
                    billingCountry = billingCountry,
                    shippingName = shippingName,
                    shippingAddress1 = shippingAddress1, 
                    shippingCity = shippingcity,
                    shippingCountry = shippingCountry
                )
            order_details.save()

            if voucher != None:
                order_details.total = new_total
                order_details.voucher = voucher
                order_details.discount = discount
                order_details.save()

            return redirect('order:thanks', order_details.id)

        except ObjectDoesNotExist:
            pass

    return render(request, 'cart.html', context)


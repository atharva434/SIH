from django.shortcuts import render, redirect
from qrcode import *
import razorpay
from .mail import sendMail
from django.views.decorators.csrf import csrf_exempt
from .models import MonumentTicket, MonumentTicket


@csrf_exempt
def book(request):
    global MonumentTicket
    print(request.POST)
    name=request.POST["name"]
    city=request.POST['city']
    monument=request.POST['monument']
    date=request.POST['date']
    phone = request.POST['phone']
    email=request.POST['emailID']

    count_children=request.POST['count_children']
    count_adult=request.POST['count_adult']
    count_abroad=request.POST['count_abroad']
    total_count = int(count_abroad)+int(count_adult)+int(count_children)

    price_adult=request.POST['price_adult']
    price_children=request.POST['price_children']
    price_abroad=request.POST['price_abroad']

    total_cost=int(float(price_abroad))*int(count_abroad)+int(float(price_adult))*int(count_adult)+int(float(price_children))*int(count_children)

    global payment
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5')) # create Razorpay client

    response_payment = client.order.create(dict(amount=total_cost*100, currency='INR'))# create order
    order_id = response_payment['id']
    order_status = response_payment['status']
    if order_status == 'created':
        Ticket=MonumentTicket(name=name, city=city, monument =monument, date=date, email=email, phone=phone, count_abroad=count_abroad,
        count_adult=count_adult,
        count_children=count_children,

        price_abroad=price_abroad,
        price_adult=price_adult,
        price_children=price_children,
         
        total_count=total_count,
        total_cost=total_cost,
        order_id=order_id)
        
        Ticket.save()
        response_payment['name'] = name
        response_payment['number'] = phone

        print(response_payment)
        # return Response(response_payment)
        return render(request,'coffee_payment.html',{ 'payment': response_payment})    

    return redirect("homepage")

def payment_status(request):
    responses = request.POST['razorpay_order_id']
    response=request.POST
    print(responses)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5'))
    status = client.utility.verify_payment_signature(params_dict)
    cold_coffee = MonumentTicket.objects.get(order_id=response['razorpay_order_id'])
    cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
    cold_coffee.paid = True
    cold_coffee.save()
    url=f"https://safar-ticketless.herokuapp.com/customerscanner/?order_id={response['razorpay_order_id']}"
    # delete_unpaid()
    img=make(url)
    img_path = "Frontend/build/static/Generated_QR/test.png"
    img.save(img_path)
    context_dict={
                    'name': cold_coffee.name,
                    'date':cold_coffee.date,
                    'city':cold_coffee.city,
                    'monument': cold_coffee.monument,
                    'count_adult':cold_coffee.count_adult,
                    'count_children':cold_coffee.count_children,
                    'count_abroad':cold_coffee.count_abroad,
                    'total_count':cold_coffee.total_count,
                    'total_cost':cold_coffee.total_cost,
                    'img':img_path,
                    'status': True,
                    'id':response['razorpay_order_id']
                }
    
    
    sendMail(cold_coffee.email, response['razorpay_order_id'],cold_coffee,context_dict)
    
    return render(request, 'payment_status.html', context_dict)
    # except:
    #     return render(request, 'payment_status.html', {'status': False})
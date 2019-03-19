from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from hashlib import md5

'''
Feedback from Ahmed Beder:
Payment MODEL
The ‘state’ field would be useful.
It will be helpful to identify if the payment was cancelled, received or still in process.
I would recommend to add a unique secure payment_id field for security reasons.
This could be used to identify the payment and prevent fraud.
For the state of payment consider using enums.


Make sure you test this properly.
Most projects have security holes that reduce points.
 Make sure that you can't reuse payments, pay for something else you selected etc.
 All-in-all try to break your own product!
'''

# Create your views here.
def index(request):
 return HttpResponse('The payments are confidential')


def payment(request):
    page={}
    if request.user.groups.filter(name="developers").count() != 0:    
        page['developer'] = 'developer'    
    page["title"]="Payment"
    sid = "ontija"
    secret_key = "301afa56fe812670d268dc6e9c200ca9"
    pid = 'ontija' + get_random_string(8,'0123456789') + "something"
    page['sid'] = sid
    page['pid'] = pid
    amount = 5
    #input_password = request.POST['password']
    #md5_hashed_input_password = md5.new(input_password).hexdigest()
    #checksum = md5.new("pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)).hexdigest()
    checksum = md5(("pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)).encode("ascii")).hexdigest()
    page['checksum'] = checksum
    page["success"] = reverse('payment_success')
    page["error"] =reverse('payment_error')
    page["cancel"] = reverse('payment_error')
    return render(request,"payments/request.html", page)

def success(request):
    page={}
    page["title"]="Payment"
    return render(request,"payments/success.html", page)

def confirmation(request):
    page={}
    page["title"]="Payment"
    return render(request,"payments/confirmation.html", page)


def error(request):
    page={}
    page["title"]="Payment"
    return render(request,"payments/error.html", page)

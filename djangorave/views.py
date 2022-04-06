# stdlib imports

# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from school.models import Premium
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import timedelta
# 3rd party imports
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt 
import json
# project imports
from djangorave.models import TransactionModel, PaymentTypeModel
from djangorave.serializers import TransactionSerializer





def jsonfy(ok):
    data = json.loads(ok)
    return(data)


def verifyhash(hashs):
    if not hashs:
        return False
    #headhash = settings.headershash
    if 'olamide' == hashs:
        return True
    return False




@csrf_exempt
@api_view(['POST'])
def TransactionCreateView(request):
    dat = request.headers['verif-hash']
    ola = verifyhash(dat)
    if ola == False:
        return HttpResponse(status=200)
    
    amount = dat.get('amount')
    status = dat.get('status')
    reference = dat.get('tx_ref')
    data = {
        'tx_ref': reference,
        'flw_ref': dat.get('flw_ref'),
        'status': status,
        'amount': amount ,
        'orderRef': dat.get('payment_type'),
        'charged_amount':dat.get('charged_amount')

    } 
    serializer = TransactionSerializer(data=data)
     
    
    if serializer.is_valid():
        
        
        payment_type_id = reference.split("__")[0]
        user_id = reference.split("__")[2]
        ola = get_user_model().objects.get(id=user_id)
        if status.lower() == 'successful':
            premium,_ = Premium.objects.get_or_create(user=ola)
            payment = PaymentTypeModel.objects.get(amount=amount)
            expiry  = payment.expiry
            premium.expiry_date= timezone.now().date()+timedelta(days=expiry)
            premium.premium = True
            premium.save()
            print(premium.expiry_date)
            
        elif status.lower()=='failed':
            premium,_ = Premium.objects.get_or_create(user=ola)
            premium.expiry_date= timezone.now().date()
            premium.premium = False
            premium.save()
            print(premium.expiry_date)
        
        serializer.save(
                user= ola ,
                payment_type=PaymentTypeModel.objects.get(id=payment_type_id),
            )
       
        return HttpResponse(status=200)

    return HttpResponse(status=400)





'''








class TransactionCreateView(CreateAPIView):
    """Provides an api end point to create transactions"""

    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes: list = []
    
    def perform_create(self, serializer: TransactionSerializer()) -> None:
        """Add payment_type and user to Transaction instance, determined
        from the received reference"""
        reference = serializer.validated_data["reference"]
        status = serializer.validated_data["status"]
        payment_type_id = reference.split("__")[0]
        user_id = reference.split("__")[2]
        ola = get_user_model().objects.get(id=user_id)
        if status == 'success':
            premium,_ = Premium.objects.get_or_create(user=ola)
            premium.paystack_id = payment_type_id
            premium.premium = True
            premium.save()
        if status=='expired':
            premium,_ = Premium.objects.get_or_create(user=ola)
            premium.paystack_id = payment_type_id
            premium.premium = False
            premium.save()
        
        serializer.save(
            user= ola ,
            payment_type=PaymentTypeModel.objects.get(id=payment_type_id),
        )
       
'''
from django.db import models
from django.db.models import Count, Q, Sum
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from soft_delete_it.models import SoftDeleteModel
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class BillingOption(object):
    EMAIL = 1
    MAIL_COPY = 2
    MAIL_ORIGINAL = 3
    FAX = 4
    UPLOAD_TO_SITE = 5
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.EMAIL, "Email"),
            (cls.MAIL_COPY, "Mail Copy"),
            (cls.MAIL_ORIGINAL, "Mail Original"),
            (cls.FAX, "Fax"),
            (cls.UPLOAD_TO_SITE, "Upload to site")
        )
        
class DebtorStatus(object):
    PURCHASE = 1
    DO_NOT_PURCHASE = 2
       
    @classmethod
    def as_choices(cls):
        return (
            (cls.PURCHASE, "Good"), 
            (cls.DO_NOT_PURCHASE, "No Load")
        )

class Debtor(SoftDeleteModel):
    debtor_id = models.AutoField(auto_created=True, primary_key=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=DebtorStatus.as_choices(), default=DebtorStatus.PURCHASE)
    docket = models.CharField(max_length=50, default=None, blank=True, null=True)
    dot_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_phone = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_fax = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_email = models.EmailField(default=None, blank=True, null=True)
    fax_noa = models.CharField(max_length=50, default=None, blank=True, null=True)
    fax_statement = models.CharField(max_length=50, default=None, blank=True, null=True)
    fax_invoice = models.CharField(max_length=50, default=None, blank=True, null=True)
    email_noa = models.EmailField(default=None, blank=True, null=True)
    email_invoice = models.EmailField(default=None, blank=True, null=True)
    email_statement = models.EmailField(default=None, blank=True, null=True)
    email_subject = models.CharField(max_length=255, default=None, blank=True, null=True)
    billing_option = models.SmallIntegerField(choices=BillingOption.as_choices(), default=BillingOption.EMAIL)
    originals_required = models.BooleanField(default=False)
    credit_limit = models.DecimalField(decimal_places =2, max_digits = 10)
    credit_score = models.DecimalField(decimal_places =2, max_digits = 10)
    invoice_upload_website = models.CharField(max_length=255, default=None, blank=True, null=True)
    invoice_upload_user = models.CharField(max_length=255, default=None, blank=True, null=True)
    invoice_upload_password = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('debtor_detail', kwargs={'id':self.debtor_id})
    def __str__(self):
        return self.name
    
class DebtorNote(SoftDeleteModel):
    note_id = models.AutoField(auto_created=True, primary_key=True),
    debtor = models.ForeignKey(Debtor, related_name='debtor_memo', on_delete = models.CASCADE)
    debtor_note = models.CharField(max_length = 255)
    is_alert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_client = models.BooleanField(default=False)
    

class DebtorContactRole(object):
    OWNER = 1
    EMPLOYEE = 2
    ACCOUNTS_PAYABLE = 3
    DISPATCH = 4
    OTHER = 5
   
    @classmethod
    def as_choices(cls):
        return (
            (cls.OWNER, "Owner"),
            (cls.EMPLOYEE, "Employee"),
            (cls.ACCOUNTS_PAYABLE, "Accounts Payable"),
            (cls.DISPATCH, "Dispatch"),
            (cls.OTHER, "Other")
        )
    
        
class DebtorContact(SoftDeleteModel):
    contact_id = models.AutoField(auto_created=True, primary_key=True)
    debtor = models.ForeignKey(Debtor, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    middle_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=100, default=None, blank=True, null=True)
    city  = models.CharField(max_length=100, default=None, blank=True, null=True)
    state = models.CharField(max_length=100, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=100, default=None, blank=True, null=True)
    phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    cell_phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    contact_position = models.CharField(max_length=100, default=None, blank=True, null=True)
    contact_role = models.SmallIntegerField(choices = DebtorContactRole.as_choices(), default=DebtorContactRole.OWNER)
    allow_portal_access = models.BooleanField(default=False)
    portal_access_login = models.CharField(max_length=255, default=None, blank=True, null=True)
    portal_access_password = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('debtor_contact_detail', kwargs={'id': self.contact_id})
    


class SalesBroker(SoftDeleteModel):
    sales_broker_id = models.AutoField(primary_key = True, auto_created = True)
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    middle_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=100, default=None, blank=True, null=True)
    city  = models.CharField(max_length=100, default=None, blank=True, null=True)
    state = models.CharField(max_length=100, default=None, blank=True, null=True)
    country = models.CharField(max_length=100, default=None, blank=True, null=True)
    phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    cell_phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    email = models.EmailField()
    is_active = models.BooleanField(default = True)
    company_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_absolute_url(self):
        return reverse('sales_broker_detail', kwargs={'id':self.sales_broker_id})
        

class TransactionFeeRateType(object):
    FLAT = 1
    DAILY = 2
    BUCKET = 3
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.FLAT, "Flat"),
            (cls.DAILY, "Daily"),
            (cls.BUCKET, "Bucket"),
        )
 
class Terms(SoftDeleteModel):
    terms_id = models.AutoField(auto_created=True, primary_key=True)
    description = models.CharField(max_length= 255, default=None, null=True, blank=True)
    advance_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    security_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    invoice_fee = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    transaction_fee_rate_type = models.SmallIntegerField(choices=TransactionFeeRateType.as_choices(), default=TransactionFeeRateType.FLAT) 
    flat_rate = models.DecimalField(default=0, decimal_places=4, max_digits=6)
    daily_rate = models.DecimalField(default=0,decimal_places=4, max_digits=6)
    express_processing_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    priority_processing_fee = models.DecimalField(decimal_places=2, max_digits=4)
    standard_processing_fee = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    fuel_advance_percentage = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    fuel_advance_fee_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    fuel_advance_days = models.IntegerField(default=0)
    over_advance_fee_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    over_advance_days = models.IntegerField(default=0)
    check_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    wire_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    transcheck_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    ach_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    fuel_card_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    carrier_quck_pay_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    paperwork_delivery_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    postage_fee = models.DecimalField(default=0,decimal_places=2, max_digits=4)
    release_days = models.IntegerField(default=0)
    recourse_days = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('terms_detail', kwargs={'id':self.terms_id})
    
    def __str__(self):
        return self.description

    def default_noa(self):
        return self.noa_id

class BucketRate(SoftDeleteModel):
    bucket_rate_id = models.AutoField(auto_created=True, primary_key=True) 
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)  
    level = models.SmallIntegerField()
    min_days = models.SmallIntegerField()
    max_days = models.SmallIntegerField()
    percentage_rate = models.DecimalField(decimal_places=2, max_digits=4)
    
    def get_absolute_url(self):
        return reverse('bucket_rate_detail', kwargs={'id':self.bucket_rate_id})

class Client(SoftDeleteModel):
    client_id = models.AutoField(auto_created=True, primary_key=True)
    debtor = models.ManyToManyField(Debtor, through='NOA')
    client_name = models.CharField(max_length=255)
    dba_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=50, default=None, blank=True, null=True)
    mailing_address_1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    mailing_address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    mailing_city = models.CharField(max_length=50, default=None, blank=True, null=True)
    mailing_state = models.CharField(max_length=50, default=None, blank=True, null=True)
    mailing_zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    mailing_country = models.CharField(max_length=50, default=None, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    docket = models.CharField(max_length=50, default=None, blank=True, null=True)
    dot_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    ein = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_type = models.CharField(max_length=50, default=None, blank=True, null=True)
    is_broker = models.BooleanField(default = False)
    business_start_date = models.DateField(default=None, blank=True, null=True)
    funding_start_date = models.DateField(default=None, blank=True, null=True)
    funding_end_date = models.DateField(default=None, blank=True, null=True)
    business_phone = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_fax = models.CharField(max_length=50, default=None, blank=True, null=True)
    business_email = models.EmailField(default=None, blank=True, null=True)
    number_of_trucks = models.IntegerField(default=None, blank=True, null=True)
    account_manager = models.ForeignKey(User, default=None, blank=True, null=True, on_delete = models.SET_NULL, related_name='am') # Foreign Key 
    assigned_processor = models.ForeignKey(User, default=None, blank=True, null=True, on_delete = models.SET_NULL, related_name='assigned_processr')
    processed_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete = models.SET_NULL, related_name='processed_by')
    primary_salesperson = models.ForeignKey(User, default=None, blank=True, null=True, on_delete = models.SET_NULL, related_name='salesperson_primary') # Foreign Key 
    secondary_salesperson = models.ForeignKey(User, default=None, blank=True, null=True, on_delete = models.SET_NULL, related_name='salesperson_secondary') # Foreign Key 
    sales_broker = models.ForeignKey(SalesBroker, default=None, blank=True, null=True, on_delete = models.SET_NULL) # Foreign Key 
    terms = models.ForeignKey(Terms, default=None, blank=True, null=True, on_delete = models.SET_NULL) # Foreign Key 
    hold_reserves = models.BooleanField(default = False)
    credit_limit = models.DecimalField(decimal_places =2, max_digits = 10)
    estimated_grp = models.DecimalField(decimal_places=2, max_digits = 4)
    estimated_volume = models.DecimalField(decimal_places =2, max_digits = 10)
    authority_status = models.BooleanField(default=True)
    insurance_status = models.BooleanField(default=True)
    insurance_expiration_date = models.DateField()
    ucc_filing_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'id':self.client_id})
    
    def __str__(self):
        return self.client_name
    def default_term(self):
        return self.terms

class ClientNote(SoftDeleteModel):
    client_note_id = models.AutoField(auto_created=True, primary_key=True),
    client = models.ForeignKey(Client, related_name='client_memo', on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    client_note = models.CharField(max_length = 255)
    is_alert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_processing = models.BooleanField(default=False)
    show_account_managers = models.BooleanField(default=False)
    show_collections = models.BooleanField(default=False)
    show_payments = models.BooleanField(default=False)
    show_client = models.BooleanField(default=False)
    

class ClientContactType(object):
    OWNER = 1
    EMPLOYEE = 2
    OTHER = 3
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.OWNER, "Owner"),
            (cls.EMPLOYEE, "Employee"),
            (cls.OTHER, "Other")
        )
    
class ClientContactAccount(SoftDeleteModel):
    contact_account_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ManyToManyField(Client, through="ClientContact")
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    middle_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=100, default=None, blank=True, null=True)
    city  = models.CharField(max_length=100, default=None, blank=True, null=True)
    state = models.CharField(max_length=100, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=100, default=None, blank=True, null=True)
    phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    cell_phone = models.CharField(max_length=100, default=None, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    contact_type = models.SmallIntegerField(choices=ClientContactType.as_choices(),  default=ClientContactType.OWNER)
    login = models.CharField(max_length=50, default=None, blank=True, null=True)
    password = models.CharField(max_length=255, default=None, blank=True, null=True)
    pin = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('contact_account_detail', kwargs={'id':self.contact_account_id})
    
    def __str__(self):
        return self.email
    
class ClientContact(SoftDeleteModel):
    contact_id = models.AutoField(auto_created=True, primary_key = True)
    client = models.ForeignKey(Client,  on_delete=models.CASCADE)
    client_contact_account = models.ForeignKey(ClientContactAccount, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    can_move_money = models.BooleanField(default=False)
    pin = models.CharField(max_length=50,default=None, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'id':self.contact_id})
    
    
class FundingAccount(SoftDeleteModel):
    funding_account_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    vendor_nick_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_routing_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_address_1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_city = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_state = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    bank_country = models.CharField(max_length=50, default=None, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_fuel_card = models.BooleanField(default=False)
    wire_allowed = models.BooleanField(default=0)
    ach_allowed = models.BooleanField(default=False)
    check_allowed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    note = models.CharField(max_length=255, default=None, null=True, blank=True)
    is_fee_customized = models.BooleanField(default=False)
    customized_fee_amount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    max_withdraw = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    
    def get_absolute_url(self):
        return reverse('funding_account_detail', kwargs={'id':self.funding_account_id})
    
class ClientDocumentType(object):
    CONTRACT = 1
    CREDIT_COMPANY = 2
    CREDIT_PERSONAL = 3
    DRIVERS_LICENSE = 4
    GRP = 5
    ENTITY = 6
    INSURANCE = 7
    AUTHORITY = 8
    IRS_8821 = 9
    UCC_SEARCH = 10
    UCC_FILED = 11
    W9 = 12
    BANKRUPTCY = 13
    SIGNATURE = 14
    NOA = 15
    OTHER = 16
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.CONTRACT, "Contract"),
            (cls.CREDIT_COMPANY, "Company Credit"),
            (cls.CREDIT_PERSONAL, "Personal Credit"),
            (cls.DRIVERS_LICENSE, "Drivers License"),
            (cls.GRP, "GRP"),
            (cls.ENTITY, "Entity"),
            (cls.INSURANCE, "Insurance"),
            (cls.AUTHORITY, "Authority"),
            (cls.IRS_8821, "8821"),
            (cls.UCC_SEARCH, "UCC Search"),
            (cls.UCC_FILED, "UCC Filed"),
            (cls.W9, "W9"),
            (cls.BANKRUPTCY, "Bankruptcy"),
            (cls.SIGNATURE, "Signature"),
            (cls.NOA, "NOA"),
            (cls.OTHER, "Other")
        )
                
class ClientDocument(SoftDeleteModel):
    client_document_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    document_type = models.SmallIntegerField(choices=ClientDocumentType.as_choices(), default=ClientDocumentType.OTHER)
    document_description = models.CharField(max_length=255, default=None, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    file_extension = models.CharField(max_length=50, default=None, blank=True, null=True)
    file_size = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    


class NOA(SoftDeleteModel):
    noa_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)
    terms = models.ForeignKey(Terms, on_delete=models.PROTECT, default=Client.default_term, null=True, blank=True)
    is_customized = models.BooleanField(default=False)
    is_debtor_notified = models.BooleanField(default=False)
    debtor_notification_date = models.DateTimeField(default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('noa_detail', kwargs={'id':self.noa_id})

 
 
class Processing(models.QuerySet):
    def total_invoice_count(self, total):
        return self.filter(total_count)

    '''     p_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    client_name = models.CharField(max_length=100)
    inv_cnt = models.IntegerField
    standard = models.DecimalField(max_digits=10,decimal_places=2)
    priority = models.DecimalField(max_digits=10,decimal_places=2)
    express = models.DecimalField(max_digits=10,decimal_places=2)
    account_manager = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
    am = models.CharField(max_length=100,default=None, null=True, blank=True)
    due_at = models.DateTimeField(default=None, null=True, blank=True)
    processing_stage = models.SmallIntegerField()
    related_name='processing' '''


        
    def get_client(self):
        return this.client  
  
class PurchaseOption(object):
    EXPRESS = 1
    PRIORITY = 2
    STANDARD = 3  
    
    @classmethod
    def as_choices(cls):
        return(
            (cls.EXPRESS, "Express"),
            (cls.PRIORITY, "Priority"),
            (cls.STANDARD, "Standard")
        )

class InvoiceStatus(object):
    PENDING = 1
    OPEN = 2
    CLOSED = 3
    
    @classmethod
    def as_choices(cls):
        return(
            (cls.PENDING, "Pending"),
            (cls.OPEN, "Open"),
            (cls.CLOSED, "Closed")
        )
    
        
class ProcessingStage(object):
    NEW = 1
    AWAITING_DOCUMENT = 2
    REDY_TO_PURCHASE = 3
    HELD_FOR_CREDIT = 4
    HELD_FOR_DOCUMENT = 5
    FUEL_ADVANCE_REQUESTED = 6
    FUEL_ADVANCE_FUNDED = 7
    PURCHASED_ZERO_PCT = 8
    PURCHASED = 9
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.NEW, "New"),
            (cls.AWAITING_DOCUMENT, "Awaiting Document"),
            (cls.REDY_TO_PURCHASE, "Ready to Purchase"),
            (cls.HELD_FOR_CREDIT, "Held for Credit"),
            (cls.HELD_FOR_DOCUMENT, "Held for Document"),
            (cls.FUEL_ADVANCE_REQUESTED, "Fuel Advance (Request Pending)"),
            (cls.FUEL_ADVANCE_FUNDED, "Fuel Advance (Advanced)"),
            (cls.PURCHASED_ZERO_PCT, "Purchased at 0 %"),
            (cls.PURCHASED, "Funded"),
        )

class Invoice(SoftDeleteModel):
    invoice_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    debtor = models.ForeignKey(Debtor, on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    load_number = models.CharField(max_length=255, default=None, blank=True, null=True)
    bol_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=11)
    is_fuel_advance = models.BooleanField(default=False)
    terms = models.ForeignKey(Terms, on_delete=models.PROTECT, default=None, null=True, blank=True)
    purchase_option = models.SmallIntegerField(choices=PurchaseOption.as_choices(), default=PurchaseOption.STANDARD)
    processing_stage = models.SmallIntegerField(choices=ProcessingStage.as_choices(), default=ProcessingStage.NEW)
    is_document_ready = models.BooleanField(default=False)
    invoice_status = models.SmallIntegerField(choices=InvoiceStatus.as_choices(), default=InvoiceStatus.PENDING)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by  = models.CharField(max_length=100, default=None, null=True, blank=True)
    date_submitted = models.DateTimeField(default=None, blank=True, null=True)
    date_processed = models.DateTimeField(default=None, blank=True, null=True)
    date_funded = models.DateTimeField(default=None, blank=True, null=True)
    date_due = models.DateTimeField(default=None, blank=True, null=True)
    is_locked = models.BooleanField(default=False) # lock will be set once invoice is purchased to avoid direct editing
    is_on_hold = models.BooleanField(default=False)
    is_charged_back = models.BooleanField(default=False)
    job_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    load_lable = models.CharField(max_length=50, default=None, blank=True, null=True)
    track_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    pickup_date = models.DateTimeField(default=None, blank=True, null=True)
    pickup_address = models.CharField(max_length=255, default=None, blank=True, null=True)
    pickup_city = models.CharField(max_length=50, default=None, blank=True, null=True)
    pickup_state = models.CharField(max_length=50, default=None, blank=True, null=True)
    pickup_zipcode =  models.CharField(max_length=50, default=None, blank=True, null=True)
    delivery_date = models.DateTimeField(default=None, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, default=None, blank=True, null=True)
    delivery_city = models.CharField(max_length=50, default=None, blank=True, null=True)
    delivery_state = models.CharField(max_length=50, default=None, blank=True, null=True)
    delivery_zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    memo = models.CharField(max_length=255, default=None, blank=True, null=True)
    document_path = models.CharField(max_length=255, default=None, blank=True, null=True)
    document_file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    noa = models.ForeignKey(NOA, on_delete=models.PROTECT)
    billing_status = models.BooleanField(default=False)
    basket_items = GenericRelation(
        'ProcessingItem',
        'invoice_object_id',
        'invoice_content_type_id',
        related_query_name='invoices',
    )


    class Meta:
        ordering = ['-date_created']


    def __str__(self):
        return str(self.invoice_number)

class Basket(models.Model):
    user = models.OneToOneField(
    get_user_model(),primary_key=True,on_delete=models.CASCADE,)
    
    def add_item(self, invoice) -> 'ProcessingItem':
        invoice_content_type = ContentType.objects.get_for_model(invoice)
        return CartItem.objects.create(
            cart=self,
            invoice_content_type=product_content_type,
            invoice_object_id=product.pk,
        )

class ProcessingItem(models.Model):
    buscket = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='invoices',
    )
    invoice_object_id = models.IntegerField()
    invoice_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    invoice = GenericForeignKey(
        'invoice_content_type',
        'invoice_object_id',
    )

     

class LineItem(object):
    RATE = 1
    LUMPER_FEE = 2
    DETENTION = 3
    PAID_IN_ADVANCE = 4
    OTHER = 5
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.RATE, "Rate"),
            (cls.LUMPER_FEE, "Lumper Fee"),
            (cls.DETENTION, "Detention"),
            (cls.PAID_IN_ADVANCE, "Less Cash"),
            (cls.OTHER, "Otehr")
        )
      
class InvoiceLineItems(SoftDeleteModel):
    invoice_line_item_id = models.AutoField(auto_created=True, primary_key=True)
    invoice = models.ForeignKey(Invoice, related_name='line_items', on_delete=models.PROTECT)
    line_item = models.SmallIntegerField(choices=LineItem.as_choices(), default=LineItem.RATE)
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    
    def get_absolute_url(self):
        return reverse('invoice_line_item_detail', kwargs={'id':self.invoice_line_item_id})
       

class InvoiceHoldReason(object):
    DOCUMENT = 1
    CLIENT_CREDIT = 2
    DEBTOR_CREDIT = 3
    OTHER = 4
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.DOCUMENT, "Document"),
            (cls.CLIENT_CREDIT, "Client Credit"),
            (cls.DEBTOR_CREDIT, "Debtor Credit"),
            (cls.OTHER, "Other")
        )
    
class ProcessingNote(SoftDeleteModel):
    note_id = models.AutoField(auto_created=True, primary_key=True),
    invoice = models.ForeignKey(Invoice, related_name='processing_note', on_delete = models.CASCADE)
    hold_reason = models.SmallIntegerField(choices=InvoiceHoldReason.as_choices(), default=None, blank=True, null=True)
    note = models.CharField(max_length = 255)
    is_alert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    show_client = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('processing_note_detail', kwargs={'id':self.note_id})
    
class BillingTask(SoftDeleteModel):
    invoice_delivery_task_id = models.AutoField(auto_created=True, primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    billing_option = models.SmallIntegerField(BillingOption, default=BillingOption.EMAIL)
    date_created = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('invoice_delivery_task_detail', kwargs={'id':self.invoice_delivery_task_id})


class DebtorResponse(object):
    EXPECTED_TO_PAY = 1
    PAID = 2
    CLAIM = 3
    DOCUMENT_ISSUE = 4
    DEBTOR_NO_PAYMENET = 5
    OTHER = 6                  
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.EXPECTED_TO_PAY, "Expected to pay"),
            (cls.PAID, "Paid"),
            (cls.CLAIM, "Claim"),
            (cls.DOCUMENT_ISSUE, "Document required"),
            (cls.DEBTOR_NO_PAYMENET, "Debtor will not pay"),
            (cls.OTHER, "Other")                  
        )

class CollectionNote(SoftDeleteModel): 
    collection_note_id = models.AutoField(auto_created=True, primary_key=True)
    invoice = models.ManyToManyField(Invoice)
    debtor_response = models.SmallIntegerField(choices=DebtorResponse.as_choices(), default=DebtorResponse.OTHER)
    note = models.CharField(max_length=255, default=None, blank=True, null=True)
    payment_date = models.DateTimeField()
    

class OverAdvance(SoftDeleteModel):
    over_advance_id = models.AutoField(auto_created=True, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    term = models.ForeignKey(Terms, on_delete=models.PROTECT)
    over_advance_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    due_date = models.DateTimeField(default=None, blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(default=None, blank=True, null=True)
    is_extended = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('over_advance_detail', kwargs={'id': self.over_advance_id})
    

class RequestType(object):
    WIRE = 1
    ACH = 2
    CHECK = 3
    TRANSCHECK = 4
    FUEL_CARD = 5
    INTERNAL_TRANSFER = 6
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.WIRE, "Wire"),
            (cls.ACH, "ACH"),
            (cls.CHECK, "Check"),
            (cls.TRANSCHECK, "Transcheck"),
            (cls.FUEL_CARD, "Fuel card"),
            (cls.INTERNAL_TRANSFER, "Internal transfer")
        )

class DisbursementRequest(SoftDeleteModel):
    request_id = models.AutoField(auto_created=True, primary_key=True)
    request_type = models.SmallIntegerField(choices= RequestType.as_choices(), default=RequestType.CHECK)
    funding_account = models.ForeignKey(FundingAccount, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, default=None, blank=True, null=True, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=2, max_digits=11)   
    date_requested = models.DateTimeField(auto_now_add=True, blank=True)
    reference_number = models.CharField(max_length=255, default=None, blank=True, null=True)
    check_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    check_date = models.DateTimeField(default=None, blank=True, null=True)
    is_granted = models.BooleanField(default=False) # Request granted by Factor
    is_cleared = models.BooleanField(default=False) # Fund withdrown from Factor's bank/other account
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('disbursement_requet_detail', kwargs={'id':self.request_id})
    
    
class Transcheck(SoftDeleteModel):
    transcheck_id = models.AutoField(auto_created=True, primary_key=True)
    disbursement_request = models.ForeignKey(DisbursementRequest, default=None, blank=True, null=True, on_delete=models.PROTECT)
    account_number  = models.CharField(max_length=50, default=None, blank=True, null=True)
    batch_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    transaction_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    book_number = models.CharField(max_length=50, default=None, blank=True, null=True) 
    expiration_date = models.DateTimeField(default=None, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    code_used = models.BooleanField(default=False)
    money_code = models.CharField(max_length=50, default=None, blank=True, null=True)


class ReceiptType(object):
    WIRE = 1
    ACH = 2
    CHECK = 3
    CREDIT_CARD = 4
   
    @classmethod
    def as_choices(cls):
        return (
            (cls.WIRE, "Wire"),
            (cls.ACH, "ACH"),
            (cls.CHECK, "Check"),
            (cls.CREDIT_CARD, "Credit card")
        )
    
class Receipt(SoftDeleteModel):
    receipt_id = models.AutoField(auto_created=True, primary_key=True)
    batch_number = models.CharField(max_length=255, default=None, blank=True, null=True)
    receipt_type = models.SmallIntegerField(choices=ReceiptType.as_choices(), default=ReceiptType.CHECK)
    client = models.ForeignKey(Client, default=None, blank=True, null=True, on_delete=models.PROTECT)
    debtor = models.ForeignKey(Debtor, default=None, blank=True, null=True, on_delete=models.PROTECT)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=11)   
    date_received = models.DateTimeField(auto_now_add=True, blank=True)
    reference_number = models.CharField(max_length=255, default=None, blank=True, null=True)
    check_number = models.CharField(max_length=50, default=None, blank=True, null=True)
    check_date = models.DateTimeField(default=None, blank=True, null=True)
    is_posted = models.BooleanField(default=False)
    receipt_notes = models.CharField(max_length=255, default=None, blank=True, null=True)
    check_image_file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    remittance_file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('receipt_detail', kwargs={'id':self.receipt_id})


class OverAdvanceNote(SoftDeleteModel):
    over_advance_note_id = models.AutoField(auto_created=True, primary_key=True)
    over_advance = models.ForeignKey(OverAdvance, on_delete=models.CASCADE)
    note = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return reverse('over_advance_note_detail', kwargs={'id': self.over_advance_note_id})


class MiscChargeType(object):
    QUICK_PAY_FEE = 1
    PAPERWORK_DELIVERY_FEE = 2
    STOP_CHECK_FEE = 3
    OTHER = 4
    @classmethod
    def as_choices(cls):
        return (
            (cls.QUICK_PAY_FEE, "Quick pay fee"),
            (cls.PAPERWORK_DELIVERY_FEE, "Paperwork delivery fee"),
            (cls.STOP_CHECK_FEE, "Stop check fee"),
            (cls.OTHER, "Other")
        )
    

class MiscCharge(SoftDeleteModel):
    misc_charge_id = models.AutoField(auto_created=True, primary_key=True)
    misc_charge_type = models.SmallIntegerField(choices=MiscChargeType.as_choices(), default=MiscChargeType.OTHER)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    note = models.CharField(max_length=255, default=None, null=True, blank=True)
    charge_date = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('misc_charge_detail', kwargs={'id': self.misc_charge_id})
    

class AccountType(object):
    ASSET = 1
    LIABILITY = 2
    CAPITAL = 3

    @classmethod
    def as_choices(cls):
        return (
            (cls.ASSET, "Asset"),
            (cls.LIABILITY, "Liability"),
            (cls.CAPITAL, "Capital")
        )
 
 
class WriteOff(SoftDeleteModel):
    write_off_id = models.AutoField(primary_key=True, auto_created=True)
    client = models.ForeignKey(Client, default=None, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    reason = models.CharField(max_length = 50, default=None, blank=True, null=True)
    description = models.CharField(max_length = 255, default=None, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.PROTECT)
     

class PassThrough(SoftDeleteModel):
    pass_through_id = models.AutoField(primary_key=True, auto_created=True)
    receipt = models.ForeignKey(Receipt, default=None, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    fee = models.DecimalField(max_digits=11, decimal_places=2)
    reason = models.CharField(max_length = 50, default=None, blank=True, null=True)
    description = models.CharField(max_length = 255, default=None, blank=True, null=True)
    beneficiary = models.CharField(max_length=255, default=None, blank=True, null=True)
    address_1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    address_2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    zipcode = models.CharField(max_length=50, default=None, blank=True, null=True)
    country = models.CharField(max_length=50, default=None, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.PROTECT)     
      
class Account(SoftDeleteModel):
    account_id = models.AutoField(primary_key = True, auto_created = True)
    account_number = models.CharField(max_length=100, default=None, blank=True, null=True) # Mapped account in accounting software
    account_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    account_description = models.CharField(max_length=255, default=None, blank=True, null=True)
    account_type = models.SmallIntegerField(choices=AccountType.as_choices(), default=None, blank=True, null=True)
    
    def __str__(self):
        return self.account_name


class TransactionSource(object):
    INVOICE = 1
    RECEIPT = 2
    PAYMENT_APPLICATION = 3
    DISBURSEMENT = 4
    OVER_ADVANCE = 5
    MISC_CHARGE = 6
    PASS_THROUGH = 7
    WRITE_OFF = 8
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.INVOICE, "Invoice"),
            (cls.RECEIPT, "Receipt"),
            (cls.PAYMENT_APPLICATION, "Payment application"),
            (cls.DISBURSEMENT, "Disbursement"),
            (cls.OVER_ADVANCE, "Over advance"),
            (cls.MISC_CHARGE, "Misc charge"),
            (cls.PASS_THROUGH, "Pass through"),
            (cls.WRITE_OFF, "Write off")
        )
        
        
class TransactionType(object):
    FUNDING = 1
    INVOICE_ADJUSTMENT = 2
    FEE_ADJUSTMENT = 3
    RECOURSE = 4
    CLOSE_OUT = 5
    RESERVE_RELEASE = 6
    RECEIPT = 7
    PAYMENT_APPLICATION = 8
    REVERSAL = 9
    DISBURSEMENT_REQUEST = 10
    MISC_CHARGE = 11
    PASS_THROUGH = 12
    WRITE_OFF = 13
    
    @classmethod
    def as_choices(cls):
        return (
            (cls.FUNDING, "Funding"),
            (cls.INVOICE_ADJUSTMENT, "Invoice adjustment"),
            (cls.FEE_ADJUSTMENT, "Fee adjustment"),
            (cls.RECOURSE, "Recourse"),
            (cls.CLOSE_OUT, "Close out"),
            (cls.RESERVE_RELEASE, "Reserve release"),
            (cls.RECEIPT, "Receipt"),
            (cls.PAYMENT_APPLICATION, "Payment application"),
            (cls.REVERSAL, "Reversal"),
            (cls.DISBURSEMENT_REQUEST, "Dusbursement request"),
            (cls.MISC_CHARGE, "Misc charge"),
            (cls.PASS_THROUGH, "Pass through"),
            (cls.WRITE_OFF, "Write off")
        )
        



class Transaction(SoftDeleteModel):
    transaction_id = models.AutoField(primary_key = True, auto_created = True)
    transaction_source = models.SmallIntegerField(choices=TransactionSource.as_choices())
    date_created = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(Invoice,default=None, blank=True, null=True, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt,default=None, blank=True, null=True, on_delete=models.CASCADE)
    over_advance = models.ForeignKey(OverAdvance,default=None, blank=True, null=True, on_delete=models.CASCADE)
    disbursement = models.ForeignKey(DisbursementRequest,default=None, blank=True, null=True, on_delete=models.CASCADE)
    misc_charges = models.ForeignKey(MiscCharge,default=None, blank=True, null=True, on_delete=models.CASCADE)
    write_off = models.ForeignKey(WriteOff,default=None, blank=True, null=True, on_delete=models.CASCADE)
    pass_through = models.ForeignKey(PassThrough,default=None, blank=True, null=True, on_delete=models.CASCADE)
    transaction_type = models.SmallIntegerField(choices=TransactionType.as_choices())
    transaction_note = models.CharField(max_length=255, default=None, blank=True, null=True)
    
class Ledger(SoftDeleteModel):
    ledger_id = models.AutoField(primary_key = True, auto_created = True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    credit = models.DecimalField(max_digits=11, decimal_places=2)
    debit = models.DecimalField(max_digits=11, decimal_places=2)



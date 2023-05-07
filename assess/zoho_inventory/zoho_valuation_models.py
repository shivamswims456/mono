from django.db import models

# Create your models here.





class zi_documents(models.Model):

    name = models.CharField(max_length=30)



class langs(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(45)
    formatted = models.CharField(105)


class custom_fields(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    value = models.CharField(max_length=10024, default=None)
    value_float = models.FloatField(default=None)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)



class chart_of_accounts(models.Model):

    zid = models.PositiveBigIntegerField()
    account = models.CharField(max_length=45)
    parent_account = models.ForeignKey("self", on_delete=models.CASCADE)




class payment_terms(models.Model):

  zid = models.PositiveBigIntegerField()
  payment_terms_label = models.CharField(max_length=30)
  expected_date = models.DateField()
  zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE) 



class payment_modes(models.Model):

    name = models.CharField(max_length=30)




class comment_type(models.Model):

    name = models.CharField(max_length=45)




class comments(models.Model):

  zid = models.PositiveBigIntegerField()
  description = models.CharField(105)
  commented_by_id = models.PositiveBigIntegerField() 
  comment_type = models.ForeignKey(comment_type, on_delete=models.CASCADE)
  date_with_time = models.DateTimeField()
  date_description = models.CharField(105)
  operation_type = models.CharField(45)



class country(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)


class state(models.Model):

    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)
    parent_country = models.ForeignKey(country, on_delete=models.CASCADE)

class city(models.Model):

    name = models.CharField(max_length=12)
    formatted = models.CharField(max_length=105)
    parent_sate = models.ForeignKey(state, on_delete=models.CASCADE)


class currency(models.Model):

    zid = models.PositiveBigIntegerField()
    currency_code = models.CharField(max_length=12)
    currency_symbol = models.CharField(max_length=12)
    price_precision = models.IntegerField()
    exchange_rate = models.FloatField()


class addresses(models.Model):

    zid = models.PositiveBigIntegerField()
    attention = models.CharField(max_length=105)
    address = models.CharField(max_length=105)
    street2 = models.CharField(max_length=105)
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    state_code = models.ForeignKey(state, on_delete=models.CASCADE)
    country = models.ForeignKey(country, on_delete=models.CASCADE)
    zip = models.CharField(max_length=12)  
    phone = models.CharField(max_length=13)
    


class tags(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=15)
    parent_tag = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)




class base_measuring_units(models.Model):
   
   unit = models.CharField(max_length=15)


class measuring_unit(models.Model):
   
    name = models.CharField(max_length=15)
    base_unit = models.ForeignKey(base_measuring_units,
                                  on_delete=models.SET_NULL,
                                  null=True)
    
    conversion_factor = models.FloatField()
    conversion_precision = models.IntegerField()

    




class dimensions(models.Model):

    zid = models.PositiveBigIntegerField()
    length = models.FloatField()
    width = models.FloatField()
    weight = models.FloatField()
    weight_unit = models.ForeignKey(measuring_unit, on_delete=models.CASCADE)
    demension_unit = models.ForeignKey(measuring_unit, on_delete=models.CASCADE)        



class statues(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(45)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)






class payment_gateway(models.Model):

    zid = models.PositiveBigIntegerField()
    payment_gateway = models.CharField(max_length=45)
    settlement_status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
  





class gst_return_details(models.Model):

    zid = models.PositiveBigIntegerField()
    return_period = models.FloatField()
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)



class default_tax_zones(models.Model):

    name = models.CharField(max_length=45)
    #business_gst, personal_gst



class default_tax_types(models.Model):

    zid = models.PositiveBigIntegerField()
    zone = models.ForeignKey(default_tax_zones, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    formatted = models.CharField(max_length=105)
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)





class default_taxes(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    formatted = models.CharField(max_length=105)
    value = models.FloatField()
    type = models.ForeignKey(default_tax_types, on_delete=models.CASCADE)
    is_source_deducted = models.BooleanField(default=False) #for TDS





class default_tax_exemption(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    reason = models.CharField(max_length=105)


class default_payment_terms(models.Model):

    label = models.CharField(max_length=45)
    description = models.CharField(max_length=105)


class sales_channels(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    z_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class source(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=105)
    format = models.CharField(max_length=45)




class balance_types(models.Model):

    name = models.CharField(max_length=45)
    document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class balance_store(models.Model):

    zid = models.PositiveBigIntegerField()
    balance_type = models.ForeignKey(balance_types, on_delete=models.CASCADE)
    balance = models.FloatField()
    receiveable = models.FloatField()
    precision = models.IntegerField()
    payable = models.FloatField()
    currency = models.ForeignKey(currency, on_delete=models.CASCADE)
    is_base_currency = models.BooleanField(default=False)



class contact_sub_type(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    format = models.CharField(max_length=105)
    parent = models.ForeignKey(zi_documents, on_delete=models.CASCADE)


class contacts(models.Model):

    zid = models.PositiveBigIntegerField()
    contact_name = models.CharField(105)
    company_name = models.CharField(105)
    first_name = models.CharField(45)
    last_name = models.CharField(45)
    designation = models.CharField(105)
    department = models.CharField(105)
    website = models.URLField()
    is_bcy_only_contact = models.BooleanField()
    is_credit_limit_migration_completed = models.BooleanField()
    lang = models.ForeignKey(langs, on_delete=models.SET_NULL, null=True)
    contact_salutation = models.CharField(max_length=5)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    mobile = models.CharField(max_length=13)
    has_transaction = models.BooleanField()
    contact_type = models.ForeignKey(zi_documents, on_delete=models.CASCADE)
    customer_sub_type = models.ForeignKey(contact_sub_type, on_delete=models.CASCADE)
    owner_id = models.ForeignKey() #tobemade
    source = models.ForeignKey(source, on_delete=models.CASCADE)
    twitter = models.URLField()
    facebook = models.URLField()
    payment_terms = models.ManyToManyField(default_payment_terms)
    credit_limit_exceeded_amount = models.FloatField()
    currency = models.ForeignKey(currency, on_delete=models.CASCADE)
    can_show_customer_ob = models.BooleanField()
    can_show_vendor_ob = models.BooleanField()
    opening_balance = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    outstanding_ob = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    unused_credits = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    unused_retainer_payments = models.ForeignKey(balance_store, on_delete=models.SET_NULL)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL)
    payment_reminder_enabled = models.BooleanField()
    is_sms_enabled = models.BooleanField()
    is_portal_enabled = models.BooleanField()
    is_consent_agreed = models.BooleanField()
    consent_date = models.DateField()
    is_client_review_settings_enabled = models.BooleanField()
    default_tax = models.ForeignKey(default_taxes, on_delete=models.SET_NULL)
    tds_tax_id = models.ForeignKey(default_tax, on_delete=models.SET_NULL)
    place_of_contact = models.ForeignKey(state, on_delete=models.CASCADE)
    gst_no  = models.CharField(max_length=16)
    pan_no = models.CharField(max_length=12)
    trader_name = models.CharField(max_length=45)
    legal_name = models.CharField(max_length=105)
    vat_reg_no = models.CharField(max_length=45)
    tax_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL)
    gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL)
    sales_channel = models.ForeignKey(sales_channels, on_delete=models.SET_NULL)
    portal_receipt_count = models.IntegerField(default=0)
    billing_address = models.ForeignKey(addresses, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(addresses, on_delete=models.SET_NULL)
    created_stamp = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    currency_summary = models.ManyToManyField(balance_store)
    comments = models.ManyToManyField(comments)
    custom_fields = models.ManyToManyField(custom_fields)



class users(models.Model):

    zid = models.PositiveBigIntegerField()
    role_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=45)
    email = models.EmailField()
    is_customer_segmented = models.BooleanField()
    is_vendor_segmented = models.BooleanField()
    user_role_formatted = models.CharField(max_length=45)
    user_type_formatted = models.CharField(max_length=45)
    status_id = models.ForeignKey(statues, on_delete=models.CASCADE)
    photo_url = models.URLField()
    is_payroll_admin = models.BooleanField()
    is_employee = models.BooleanField()
    allocated_warehouse_count = models.IntegerField()
    total_warehouse_count = models.IntegerField()
    custom_fields = models.ManyToManyField(custom_fields)




class approvers(models.Model):

    user = models.ForeignKey(users, on_delete=models.CASCADE)  
    zi_document = models.ForeignKey(zi_documents, on_delete=models.CASCADE)
    order = models.IntegerField()
    has_approved = models.BooleanField()
    approval_status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    is_next_approver = models.BooleanField()
    submitted_date = models.DateField()
    approved_date = models.DateField()
    is_final_approver = models.BooleanField()
  




class warehouses(models.Model):

    zid = models.PositiveBigIntegerField()
    warehouse_name  = models.CharField(max_length=105)
    attention = models.CharField(max_length=45)
    address  = models.ForeignKey(addresses, on_delete=models.SET_NULL, null=True)
    email  = models.EmailField()
    is_primary = models.BooleanField()
    status = models.ForeignKey(statues, on_delete=models.CASCADE)
    is_fba_warehouse  = models.BooleanField()
    sales_channels = models.ManyToManyField(sales_channels)
    custom_fields = models.ManyToManyField(custom_fields)



class item_types(models.Model):

    name = models.CharField(max_length=12)


class product_types(models.Model):

    name = models.CharField(max_length=12)



class item_warehouse_stock(models.Model):

    zid = models.PositiveBigIntegerField()
    warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE) 
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    warehouse_stock_on_hand = models.FloatField()
    initial_stock = models.FloatField()
    initial_stock_rate = models.FloatField()
    warehouse_available_stock = models.FloatField()
    warehouse_actual_available_stock = models.FloatField()
    warehouse_committed_stock = models.FloatField()
    warehouse_actual_committed_stock = models.FloatField()
    warehouse_available_for_sale_stock = models.FloatField()
    warehouse_actual_available_for_sale_stock = models.FloatField()
    is_fba_warehouse = models.BooleanField()
    sales_channel = models.ManyToManyField(sales_channels)
    serial_numbers = models.JSONField()
    batches = models.JSONField()



class items(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=105)
    sku = models.CharField(max_length=105)
    brand = models.CharField(max_length=45)
    manufacturer = models.CharField(max_length=45)
    category_id = models.PositiveBigIntegerField() #tobemade
    hsn_or_sac = models.CharField(max_length=45)
    image_name = models.CharField(max_length=45)
    status = models.ForeignKey(statues, on_delete=models.CASCADE)
    source = models.ForeignKey(source, on_delete=models.CASCADE)
    unit = models.ForeignKey(measuring_unit, on_delete=models.SET_NULL, null=True)
    quantity_decimal_place = models.IntegerField()
    description = models.CharField(max_length=105)
    item_tax_preferences = models.ManyToManyField(default_tax_types)
    rate = models.FloatField()
    account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    is_default_tax_applied = models.BooleanField()
    is_taxable = models.BooleanField()
    tax_exemption_id = models.ForeignKey(default_tax_exemption, on_delete=models.SET_NULL, null=True)
    taxability_type = models.CharField(max_length=12)
    purchase_description = models.CharField(max_length=105)
    product_description = models.CharField(max_length=105)
    product_short_description = models.CharField(max_length=45)
    pricebook_rate = models.FloatField()
    pricebook_discount = models.FloatField()
    sales_rate = models.FloatField()
    purchase_rate = models.FloatField()
    purchase_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    inventory_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField()
    offline_created_date_with_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    item_type = models.ForeignKey(item_types, on_delete=models.SET_NULL, null=True)
    product_type = models.ForeignKey(product_types, on_delete=models.CASCADE)
    is_returnable = models.BooleanField()
    reorder_level = models.FloatField()
    minimum_order_quantity = models.FloatField()
    maximum_order_quantity = models.FloatField()
    initial_stock = models.FloatField()
    initial_stock_rate = models.FloatField()
    total_initial_stock = models.FloatField()
    vendor_id = models.ForeignKey(contacts, on_delete = models.SET_NULL, null=True)
    stock_on_hand = models.FloatField()
    asset_value = models.FloatField()
    available_stock = models.FloatField()
    actual_available_stock = models.FloatField()
    committed_stock = models.FloatField()
    actual_committed_stock = models.FloatField()
    available_for_sale_stock = models.FloatField()
    actual_available_for_sale_stock = models.FloatField()
    custom_fields = models.ManyToManyField(custom_fields) 
    image_document_id = models.PositiveBigIntegerField()
    track_serial_number = models.BooleanField()
    track_batch_number = models.BooleanField()
    upc = models.CharField(max_length=30)
    ean = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    part_number = models.CharField(max_length=30)
    is_combo_product = models.BooleanField()
    sales_channels = models.ManyToManyField(sales_channels)
    warehouses = models.ManyToManyField(item_warehouse_stock)  
    preferred_vendors = models.ManyToManyField(contacts)
    comments = models.ManyToManyField(comments)
    package_details = models.ForeignKey(dimensions)
    is_composite = models.BooleanField()
    





class bill_line_items(models.Model):

  zid = models.PositiveBigIntegerField()
  purchaseorder_item_id = models.PositiveBigIntegerField()
  receive_item_id  = models.PositiveBigIntegerField()
  item_id  = models.PositiveBigIntegerField()
  itc_eligibility = models.CharField(max_length=45)
  gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
  is_combo_product = models.BooleanField()
  warehouse_id = models.ForeignKey()
  account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
  description = models.CharField(max_length=105)
  bcy_rate = models.FloatField()
  rate = models.FloatField()
  pricebook_id = models.PositiveBigIntegerField()
  tags = models.ManyToManyField(tags)
  quantity = models.FloatField()
  discount = models.FloatField()
  discounts = models.JSONField()
  markup_percent = models.FloatField()
  tax_id = models.ForeignKey(default_taxes, on_delete=models.CASCADE)
  line_item_taxes = models.JSONField
  item_total = models.FloatField()
  item_total_inclusive_of_tax = models.FloatField()
  item_order = models.IntegerField()
  unit = models.ForeignKey(dimensions, on_delete=models.CASCADE)
  product_type = models.ForeignKey(product_types, on_delete=models.CASCADE)
  item_type = models.ForeignKey(item_types, on_delete=models.CASCADE)
  has_product_type_mismatch = models.BooleanField()
  reverse_charge_tax_id = models.ForeignKey(default_taxes, on_delete=models.SET_NULL, null=True)
  is_billable = models.BooleanField()
  is_landedcost = models.BooleanField()
  customer_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
  project_id = models.PositiveBigIntegerField()
  item_custom_fields = models.ManyToManyField(custom_fields)
  track_serial_for_receive = models.BooleanField()
  track_batch_for_receive = models.BooleanField()
  serial_numbers = models.JSONField()
  batches = models.JSONField()
  purchase_request_items  = models.JSONField()
  


class composite_items(models.Model):

    zid = models.PositiveBigIntegerField()
    name = models.CharField(max_length=105)
    unit = models.ForeignKey(measuring_unit, on_delete=models.SET_NULL, null=True)
    category_id = models.PositiveBigIntegerField()
    offline_created_date_with_time = models.DateTimeField()
    show_in_storefront = models.BooleanField()
    brand = models.CharField(max_length=45)
    manufacturer = models.CharField(max_length=45)
    product_description = models.CharField(max_length=105)
    product_tags = models.ManyToManyField(tags)
    product_short_description = models.CharField(max_length=105)
    hsn_or_sac = models.CharField(max_length=30)
    description = models.CharField(max_length=105)
    tax_id = models.ForeignKey(default_taxes)
    is_taxable = models.BooleanField()
    tax_exemption_id = models.ForeignKey(default_tax_exemption, on_delete=models.SET_NULL, null=True)
    product_type = models.ForeignKey(product_types, on_delete=models.SET_NULL, null=True)
    taxability_type = models.ForeignKey(default_tax_types, on_delete=models.SET_NULL, null=True)
    purchase_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    inventory_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(tags)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(source, on_delete=models.SET_NULL, null=True)
    is_combo_product = models.BooleanField()
    is_boxing_exist = models.BooleanField()
    item_type = models.ForeignKey(item_types, on_delete=models.SET_NULL, null=True)
    rate = models.FloatField()
    label_rate = models.FloatField()
    pricebook_rate = models.FloatField()
    pricebook_discount = models.FloatField()
    purchase_rate = models.FloatField()
    sales_rate = models.FloatField()
    reorder_level = models.FloatField()
    is_returnable = models.BooleanField()
    initial_stock = models.FloatField()
    initial_stock_rate= models.FloatField()
    total_initial_stock = models.FloatField()
    vendor_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    stock_on_hand = models.FloatField()
    asset_value = models.FloatField()
    available_stock = models.FloatField()
    actual_available_stock = models.FloatField()
    committed_stock = models.FloatField() 
    actual_committed_stock = models.FloatField()
    available_for_sale_stock = models.FloatField()
    actual_available_for_sale_stock = models.FloatField()
    track_serial_number = models.FloatField()
    track_batch_number = models.FloatField()
    sku = models.CharField(max_length=45)
    upc = models.CharField(max_length=45)
    ean = models.CharField(max_length=45)
    isbn = models.CharField(max_length=45)
    part_number = models.CharField(max_length=45)
    purchase_description = models.CharField(max_length=105)
    custom_fields 
    last_modified_time = models.DateTimeField()
    package_details = models.ForeignKey(dimensions, on_delete=models.SET_NULL, null=True)
    mapped_items = models.ManyToManyField(items)
    sales_channels = models.ManyToManyField(sales_channels)
    warehouses = models.ManyToManyField(item_warehouse_stock)
    preferred_vendors = models.ManyToManyField(contacts)
    comments = models.ManyToManyField(comments)





class bill_payments(models.Model):

    payment_id = models.PositiveBigIntegerField()
    bill_id = models.PositiveBigIntegerField()
    bill_payment_id = models.PositiveBigIntegerField()
    payment_mode = models.ForeignKey(payment_modes, on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=30)
    description = models.CharField(max_length=105)
    date = models.DateField()
    reference_number = models.CharField(max_length=30)
    exchange_rate = models.FloatField()
    amount = models.FloatField()
    paid_through_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    is_single_bill_payment = models.IntegerField()
    is_paid_via_print_check = models.BooleanField()
    check_number = models.CharField(max_length=30)
    check_status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    is_ach_payment = models.BooleanField()
    ach_payment_status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    gateway = models.ForeignKey(payment_gateway, on_delete=models.SET_NULL, null=True)   
    ach_gw_transaction_id = models.CharField(max_length=45)
    filed_in_vat_return_id = models.CharField(max_length=45)
    filed_in_vat_return_name = models.CharField(max_length=45)
    filed_in_vat_return_type = models.CharField(max_length=45)

class bills(models.Model):

    zid = models.PositiveBigIntegerField()
    purchaseorder_ids = models.JSONField()
    vendor_id = models.ForeignKey(contacts, on_delete=models.CASCADE)
    source = models.ManyToManyField(source)
    destination_of_supply = models.ForeignKey(state, on_delete=models.SET_NULL, null=True)
    gst_no = models.CharField(max_length=20)
    gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
    tax_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
    invoice_conversion_type = models.CharField(max_length=45)
    unused_credits_payable_amount = models.FloatField()
    gst_return_details = models.ForeignKey(gst_return_details, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    color_code = models.CharField(max_length=30)
    current_sub_status_id = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    sub_statuses = models.JSONField()
    bill_number = models.CharField(max_length=30)
    date = models.DateField()
    is_pre_gst = models.BooleanField()
    due_date = models.DateField()
    discount_setting = models.CharField(max_length=30)
    is_tds_amount_in_percent = models.BooleanField()
    tds_percent = models.FloatField()
    tds_amount = models.FloatField()
    tax_account_id = models.ForeignKey()
    payment_terms = models.ManyToManyField(payment_terms)
    reference_number = models.CharField(max_length=30)
    recurring_bill_id = models.PositiveBigIntegerField()
    due_by_days = models.IntegerField()
    due_in_days = models.IntegerField()
    currency_id = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True)
    price_precision = models.IntegerField()
    exchange_rate = models.FloatField()
    custom_fields = models.ManyToManyField(custom_fields)
    is_viewed_by_client = models.BooleanField()
    client_viewed_time = models.DateTimeField()
    is_tds_applied = models.BooleanField()
    is_item_level_tax_calc = models.BooleanField()
    is_inclusive_tax = models.BooleanField()
    tax_rounding = models.CharField(max_length=30)
    filed_in_vat_return_id = models.CharField(max_length=45)
    is_reverse_charge_applied = models.BooleanField()
    is_uber_bill = models.BooleanField()
    is_tally_bill = models.BooleanField()
    mark_as_received_status = models.CharField(max_length=45)
    is_standalone_bill = models.BooleanField()
    track_discount_in_account = models.BooleanField()
    submitted_date = models.DateField()
    submitted_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    approver_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    adjustment = models.FloatField()
    adjustment_description = models.CharField(max_length=105)
    discount_amount = models.FloatField()
    discount = models.FloatField()
    discount_applied_on_amount = models.FloatField()
    is_discount_before_tax = models.BooleanField()
    discount_account_id = models.PositiveBigIntegerField()
    discount_account_name = models.CharField(max_length=105)
    discount_type = models.CharField(max_length=45)
    sub_total = models.FloatField()
    sub_total_inclusive_of_tax = models.FloatField()
    tax_total = models.FloatField()
    total = models.FloatField()
    payment_made = models.FloatField()
    vendor_credits_applied = models.FloatField()
    is_line_item_invoiced = models.BooleanField()
    purchaseorders = models.JSONField()
    taxes = models.JSONField()
    tax_override = models.BooleanField()
    balance = models.JSONField()
    created_time = models.DateTimeField()
    created_by_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    last_modified_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    last_modified_time = models.DateTimeField()
    warn_create_vendor_credits = models.BooleanField()
    reference_id = models.CharField(max_length=30)
    notes = models.CharField(max_length=145)
    terms = models.CharField(max_length=145)
    open_purchaseorders_count = models.IntegerField() 
    un_billed_items = models.ForeignKey(items)
    invoices = models.JSONField()
    is_approval_required = models.BooleanField()
    can_create_bill_of_entry = models.BooleanField()
    allocated_landed_costs = models.JSONField()
    unallocated_landed_costs = models.JSONField()
    entity_type = models.CharField(max_length=45)
    credit_notes = models.JSONField()
    payments = models.ManyToManyField(bill_payments) 
    reference_bill_id = models.PositiveBigIntegerField()
    can_send_in_mail = models.BooleanField()
    approvers_list = models.ManyToManyField(approvers)
    line_items = models.ManyToManyField(bill_line_items) 
    billing_address = models.ForeignKey(addresses, on_delete=models.SET_NULL, null=True)
    comments = models.ManyToManyField(comments)





class invoice_line_items(models.Model):

    line_item_id = models.PositiveBigIntegerField()
    item_id = models.ForeignKey(items, on_delete=models.SET_NULL, null=True)
    item_order = models.FloatField()
    product_type = models.ForeignKey(product_types, on_delete=models.SET_NULL, null=True)
    has_product_type_mismatch = models.BooleanField()
    has_invalid_hsn = models.BooleanField()
    name = models.CharField(max_length=105)
    description = models.CharField(max_length=105)
    unit = models.ForeignKey(measuring_unit)
    quantity = models.FloatField()
    discount_amount = models.FloatField()
    discount = models.FloatField()
    discounts = models.JSONField()
    bcy_rate = models.FloatField()
    rate = models.FloatField()
    account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    pricebook_id = models.PositiveBigIntegerField()
    item_total_inclusive_of_tax = models.FloatField()
    tax_id = models.ForeignKey(default_taxes, on_delete=models.SET_NULL, null=True)
    gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
    item_total = models.FloatField()
    tags = models.ManyToManyField(tags)
    hsn_or_sac = models.CharField(max_length=45)
    reverse_charge_tax_id = models.ForeignKey(default_taxes, on_delete=models.SET_NULL, null=True)
    line_item_taxes = models.ManyToManyField(default_taxes)
    bill_id = models.PositiveBigIntegerField()
    bill_item_id = models.PositiveBigIntegerField()
    warehouse_id = models.ForeignKey(warehouses, on_delete=models.SET_NULL, null=True)
    is_combo_product = models.BooleanField()
    track_serial_for_package = models.BooleanField()
    track_batch_for_package = models.BooleanField()
    serial_numbers = models.JSONField()
    batches = models.JSONField()
    project_id = models.PositiveIntegerField()
    expense_id = models.PositiveBigIntegerField()
    item_type = models.ForeignKey(item_types, on_delete=models.SET_NULL, null=True)
    purchase_rate = models.FloatField()
    salesorder_item_id = models.PositiveBigIntegerField()
    can_show_in_task_table = models.BooleanField()
    cost_amount = models.FloatField()
    package_details = models.ForeignKey(dimensions, on_delete=models.SET_NULL, null=True)







class invoices(models.Model):

    zid = models.PositiveBigIntegerField()
    invoice_number = models.CharField(max_length=45)
    date = models.DateField()
    due_date = models.DateField()
    offline_created_date_with_time = models.DateTimeField()
    customer_id = models.ForeignKey(contacts, on_delete=models.CASCADE)
    currency_id = models.ForeignKey(currency, on_delete=models.SET_NULL, null=True)
    invoice_source = models.ForeignKey(source, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    custom_fields = models.ManyToManyField(custom_fields)
    recurring_invoice_id = models.PositiveBigIntegerField()
    place_of_supply = models.ForeignKey(state, on_delete=models.SET_NULL, null=True)
    payment_terms = models.ForeignKey(payment_terms, on_delete=models.SET_NULL, null=True)
    payment_reminder_enabled = models.BooleanField()
    payment_made = models.FloatField()
    next_retry_date = models.DateField()
    reference_number = models.CharField(max_length=45)
    lock_details = models.JSONField()
    line_items = models.ManyToManyField(invoice_line_items)
    credits = models.JSONField()
    journal_credits = models.JSONField()
    exchange_rate = models.FloatField()
    is_autobill_enabled = models.BooleanField()
    inprocess_transaction_present = models.BooleanField()
    allow_partial_payments = models.BooleanField()
    price_precision = models.IntegerField()
    sub_total = models.FloatField()
    tax_total = models.FloatField()
    discount_total  = models.FloatField()
    discount_percent  = models.FloatField()
    discount  = models.FloatField()
    discount_applied_on_amount  = models.FloatField()
    discount_type = models.CharField(max_length=12)
    is_discount_before_tax = models.BooleanField()
    adjustment = models.FloatField()
    adjustment_description = models.CharField(max_length=105)
    shipping_charge_tax_id = models.ForeignKey(default_taxes, on_delete=models.SET_NULL, null=True)
    shipping_charge_tax_exemption_id = models.ForeignKey(default_tax_exemption, on_delete=models.SET_NULL, null=True)
    shipping_charge_sac_code  = models.FloatField()
    shipping_charge_exclusive_of_tax  = models.FloatField()
    shipping_charge   = models.FloatField()
    bcy_shipping_charge_tax   = models.FloatField()
    bcy_shipping_charge   = models.FloatField()
    bcy_adjustment   = models.FloatField()
    bcy_sub_total   = models.FloatField()
    bcy_discount_total   = models.FloatField()
    bcy_tax_total   = models.FloatField()
    bcy_total   = models.FloatField()
    is_reverse_charge_applied  = models.BooleanField()
    total   = models.FloatField()
    balance    = models.FloatField()
    write_off_amount    = models.FloatField()
    roundoff_value    = models.FloatField()
    transaction_rounding_type    = models.FloatField()
    reference_invoice_type = models.CharField(max_length=30)
    is_inclusive_tax  = models.BooleanField()
    sub_total_inclusive_of_tax = models.FloatField()
    tax_specification = models.CharField(max_length=12) 
    gst_no = models.CharField(max_length=16)
    gst_treatment = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
    tax_reg_no  = models.CharField(max_length=45)
    tax_treatment  = models.ForeignKey(default_tax_zones, on_delete=models.SET_NULL, null=True)
    tax_rounding = models.FloatField()



class transfer_order_warehouses(models.Model):

    warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    attention = models.CharField(max_length=45)
    address = models.ForeignKey(addresses, on_delete=models.CASCADE)
    is_primary = models.BooleanField()
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    is_fba_warehouse = models.BooleanField()
    sales_channels = models.ManyToManyField(sales_channels)



class line_items_to(models.Model):

    line_item_id = models.PositiveBigIntegerField()
    item_id = models.PositiveBigIntegerField()
    item_order = models.IntegerField()
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=105)
    quantity_transfer = models.FloatField()
    price = models.FloatField()
    asset_price = models.FloatField()
    unit = models.ForeignKey(measuring_unit, on_delete=models.CASCADE)
    quantity_decimal_place = models.IntegerField*()
    sku = models.CharField(max_length=45)
    serial_numbers = models.JSONField()
    batches = models.JSONField()



class transfer_orders(models.Model):

    zid = models.PositiveBigIntegerField()
    from_warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    to_warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    date = models.DateField()
    transferred_date = models.DateField()
    description = models.CharField(max_length=45)
    transfer_order_number = models.CharField(max_length=30)
    created_by_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    last_modified_by_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(statues, on_delete=models.SET_NULL, null=True)
    submitter_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    approver_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    submitted_date = models.DateField()
    submitted_by = models.ForeignKey(users, on_delete=models.SET_NULL,null=True)
    line_items = models.ManyToManyField(line_items_to)
    comments = models.ManyToManyField(comments)
    custom_fields = models.ManyToManyField(custom_fields)
    tracking_number = models.CharField(max_length=45)
    tracking_link = models.URLField()
    carrier = models.CharField(max_length=45)
    is_tracking_enabled = models.BooleanField()
    tracking_statuses = models.ForeignKey(statues, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    warehouses = models.ForeignKey(transfer_order_warehouses, on_delete=models.CASCADE)



class line_items_adjustment_qty(models.Model):

    zid = models.PositiveBigIntegerField()
    item_id = models.ForeignKey(items, on_delete=models.CASCADE)
    item_order = models.IntegerField()
    adjustment_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    asset_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    quantity_adjusted = models.ForeignKey(chart_of_accounts, on_delete=models.SET_NULL, null=True)
    serial_numbers = models.JSONField()
    batches = models.JSONField()
    warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    tags = models.ManyToManyField(tags)




class adjustments(models.Model):

    """     
        adjustments by value has not been implemented
    """

    zid = models.PositiveBigIntegerField()
    date = models.DateField()
    adjustment_account_id = models.ForeignKey(chart_of_accounts, on_delete=models.CASCADE)
    reason = models.CharField(max_length=105)
    description = models.CharField(max_length=105)
    status = models.ForeignKey(statues, on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=45)
    adjustment_type = models.CharField(max_length=45)
    line_items = models.ManyToManyField(line_items_adjustment_qty)
    comments = models.ManyToManyField(comments)
    total = models.FloatField()
    warehouse_id = models.ForeignKey(warehouses, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()
    created_by_id = models.DateTimeField()
    last_modified_by_id = models.ForeignKey(users, on_delete=models.SET_NULL, null=True)
    custom_fields = models.ManyToManyField(custom_fields)

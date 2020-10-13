# DATABASE

## User

### phone

### first_name

### last_name

### gender

### email

optional

### image

optional

### is_verified

### is_admin

### is_staff

### is_active

### updated

### timestamp

## Profile

### user

- OTOF: User

### address

- FK: Address

### is_active

### updated

### timestamp

## Address

```
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    name            = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname        = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='United States of America')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line_1)
```

### address_type

### line_1

### line_2

### city

### state

### postal_code

### country

### timestamp

## Store

### title

### user

- FK: User

### category

### parent

- FK: Store

### opening_time

### closing_time

### store_status

### address

- FK: Address

### logo

### total_store_order_trx

### total_vendor_admin_trx

### is_active

### updated

### timestamp

## Product

### store

- FK: Store

### title

### sku

### description

### manufacturer

### margin

### is_hot

### sup_price

### selling_price

### discount

### measuring_type

### unit_in_stock

### unit_on_order

### category

### is_available

### is_discount_available

### image

### more_images

### updated

### timestamp

## OrderItem

### order

- FK: Order

### product

- FK: Product

### quantity

### item_total

### updated

### timestamp

## Order

### customer

- FK: User

### ordered_date

### date_confirmed

### shipping_date

### date_received

### quote

### confirmed_by

- FK: User

### shipper

- FK: User

### shipping_address

- FK: Adress

### billing_address

- FK: Adress

### tracking_address

- FK: Adress

### status

### is_pending

### is_aproved

### is_arrieved

### sub_total

### shipping_total

### total

### updated

### timestamp

## StoreOrderTrx

### store

- FK: Store

### order

- FK: Order

### amount

### timestamp

## VendorAdminTrx

### admin_user

- FK: User

### vendor_user

- FK: User

### store

- FK: Store

### vouchar_amount

### timestamp

## Delivery Service and E-Commerce System  Database Model for Django Framework
Date: 19.09.2020
Md. Belal Hossain & Md. Shariar Kabir
Updated At: 01.10.2020

## Notes
FK => ForeignKey
OTOF => OneToOneField
MTMF => ManyToManyField
GFK => GenericForeignKey

*XMind - Trial Version*
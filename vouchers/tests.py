from django.test import TestCase
from django.utils import timezone
from .models import Voucher
from .forms import VoucherApplyForm

class VoucherTestCase(TestCase):
    def setUp(self):
        self.voucher = Voucher.objects.create(
            code='TESTVOUCHER',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=30),
            discount=10,
            active=True
        )

    def test_voucher_apply(self):
        response = self.client.post('/voucher-apply/', {'code': 'TESTVOUCHER'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
        self.assertEqual(self.client.session['voucher_id'], self.voucher.id)

        response = self.client.post('/voucher-apply/', {'code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
        self.assertIsNone(self.client.session.get('voucher_id'))
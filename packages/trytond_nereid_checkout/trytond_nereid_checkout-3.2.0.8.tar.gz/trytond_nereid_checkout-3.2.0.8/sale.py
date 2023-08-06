# -*- coding: utf-8 -*-
"""
    sale

    Additional Changes to sale

    :copyright: (c) 2011-2014 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
from uuid import uuid4
from datetime import date
from dateutil.relativedelta import relativedelta

from trytond.model import fields
from trytond.config import CONFIG
from trytond.pool import PoolMeta, Pool

from nereid import render_template, request, abort, login_required, \
    route, current_user, flash, redirect, url_for, jsonify
from nereid.contrib.pagination import Pagination
from nereid.templating import render_email
from nereid.ctx import has_request_context
from trytond.transaction import Transaction
from trytond.report import Report

from .i18n import _

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    """Add Render and Render list"""
    __name__ = 'sale.sale'

    #: This access code will be cross checked if the user is guest for a match
    #: to optionally display the order to an user who has not authenticated
    #: as yet
    guest_access_code = fields.Char('Guest Access Code')
    email_sent = fields.Boolean('Email Sent?', readonly="True")

    per_page = 10

    @staticmethod
    def default_guest_access_code():
        """A guest access code must be written to the guest_access_code of the
        sale order so that it could be accessed without a login
        """
        return unicode(uuid4())

    @classmethod
    @route('/orders')
    @route('/orders/<int:page>')
    @login_required
    def render_list(cls, page=1):
        """Render all orders
        """

        filter_by = request.args.get('filter_by', None)

        domain = [
            ('party', '=', request.nereid_user.party.id),
        ]

        if filter_by == 'processing':
            domain.append(('state', 'in', ('processing', 'confirmed')))

        elif filter_by == 'done':
            domain.append(('state', '=', 'done'))

        elif filter_by == 'canceled':
            domain.append(('state', '=', 'cancel'))

        else:
            domain.append(('state', 'not in', ('draft', 'quotation', 'cancel')))

            # Add a sale_date domain for recent orders.
            req_date = (
                date.today() + relativedelta(months=-3)
            )
            domain.append((
                'sale_date', '>=', req_date
            ))

        # Handle order duration
        sales = Pagination(cls, domain, page, cls.per_page)

        return render_template('sales.jinja', sales=sales)

    @route('/order/<int:active_id>')
    @route('/order/<int:active_id>/<confirmation>')
    def render(self, confirmation=None):
        """Render given sale order

        :param sale: ID of the sale Order
        :param confirmation: If any value is provided for this field then this
                             page is considered the confirmation page. This
                             also passes a `True` if such an argument is proved
                             or a `False`
        """
        NereidUser = Pool().get('nereid.user')

        # This Ugly type hack is for a bug in previous versions where some
        # parts of the code passed confirmation as a text
        confirmation = False if confirmation is None else True

        # Try to find if the user can be shown the order
        access_code = request.values.get('access_code', None)

        if current_user.is_anonymous():
            if not access_code:
                # No access code provided, user is not authorized to
                # access order page
                return NereidUser.unauthorized_handler()
            if access_code != self.guest_access_code:
                # Invalid access code
                abort(403)
        else:
            if self.party.id != request.nereid_user.party.id:
                # Order does not belong to the user
                abort(403)

        return render_template(
            'sale.jinja', sale=self, confirmation=confirmation
        )

    def send_confirmation_email(self, silent=True):
        """An email confirming that the order has been confirmed and that we
        are waiting for the payment confirmation if we are really waiting for
        it.

        For setting a convention this email has to be sent by rendering the
        templates

           * Text: `emails/sale-confirmation-text.jinja`
           * HTML: `emails/sale-confirmation-html.jinja`

        """
        EmailQueue = Pool().get('email.queue')
        ModelData = Pool().get('ir.model.data')
        Group = Pool().get('res.group')
        Sale = Pool().get('sale.sale')

        # TODO: Instead of 2 emails, merge them into one
        group_id = ModelData.get_id(
            "nereid_checkout", "order_confirmation_receivers"
        )
        to_emails = map(
            lambda user: user.email,
            filter(lambda user: user.email, Group(group_id).users)
        )

        if to_emails:
            # Send the order confirmation notification email
            subject = "New order has been placed: #%s" % self.reference
            email_message = render_email(
                CONFIG['smtp_from'], to_emails, subject,
                text_template='emails/sale-confirmation-text.jinja',
                html_template='emails/sale-confirmation-html.jinja',
                sale=self,
                formatLang=lambda *args, **kargs: Report.format_lang(
                    *args, **kargs)
            )
            EmailQueue.queue_mail(
                CONFIG['smtp_from'], to_emails, email_message.as_string()
            )

        # Send the standard order confirmation email
        to_emails = set()
        if self.party.email:
            to_emails.add(self.party.email.lower())
        if not current_user.is_anonymous() and current_user.email:
            to_emails.add(current_user.email.lower())
        if to_emails:
            email_message = render_email(
                CONFIG['smtp_from'], list(to_emails), 'Order Confirmed',
                text_template='emails/sale-confirmation-text.jinja',
                html_template='emails/sale-confirmation-html.jinja',
                sale=self,
                formatLang=lambda *args, **kargs: Report.format_lang(
                    *args, **kargs)
            )

            EmailQueue.queue_mail(
                CONFIG['smtp_from'], list(to_emails),
                email_message.as_string()
            )

            Sale.write([self], {
                'email_sent': True,
            })

    @classmethod
    def confirm(cls, sales):
        "Send an email after sale is confirmed"
        super(Sale, cls).confirm(sales)

        if has_request_context():
            for sale in sales:

                # Change party name to invoice address name for guest user
                if current_user.is_anonymous():
                    sale.party.name = sale.invoice_address.name
                    sale.party.save()
                if sale.email_sent:
                    continue
                sale.send_confirmation_email()

    def nereid_pay_using_credit_card(self, credit_card_form, amount):
        '''
        Complete using the given card.

        If the user is registered and the save card option is given, then
        first save the card and delegate to :meth:`_complete_using_profile`
        with the profile thus obtained.

        Otherwise a payment transaction is created with the given card data.
        '''
        AddPaymentProfileWizard = Pool().get(
            'party.party.payment_profile.add', type='wizard'
        )

        gateway = request.nereid_website.credit_card_gateway

        if not current_user.is_anonymous() and \
                credit_card_form.add_card_to_profiles.data and \
                request.nereid_website.save_payment_profile:
            profile_wiz = AddPaymentProfileWizard(
                AddPaymentProfileWizard.create()[0]     # Wizard session
            )

            profile_wiz.card_info.party = self.party
            profile_wiz.card_info.address = self.invoice_address
            profile_wiz.card_info.provider = gateway.provider
            profile_wiz.card_info.gateway = gateway
            profile_wiz.card_info.owner = credit_card_form.owner.data
            profile_wiz.card_info.number = credit_card_form.number.data
            profile_wiz.card_info.expiry_month = \
                credit_card_form.expiry_month.data
            profile_wiz.card_info.expiry_year = \
                unicode(credit_card_form.expiry_year.data)
            profile_wiz.card_info.csc = credit_card_form.cvv.data

            with Transaction().set_context(return_profile=True):
                profile = profile_wiz.transition_add()
                return self.nereid_pay_using_profile(
                    profile.id, amount
                )

        return self._pay_using_credit_card(
            gateway, {
                'owner': credit_card_form.owner.data,
                'number': credit_card_form.number.data,
                'expiry_month': credit_card_form.expiry_month.data,
                'expiry_year': unicode(credit_card_form.expiry_year.data),
                'cvv': credit_card_form.cvv.data,
            },
            amount
        )

    def nereid_pay_using_alternate_payment_method(self, payment_form, amount):
        '''
        :param payment_form: The validated payment_form to extract additional
                             info
        '''
        PaymentTransaction = Pool().get('payment_gateway.transaction')
        PaymentMethod = Pool().get('nereid.website.payment_method')

        payment_method = PaymentMethod(
            payment_form.alternate_payment_method.data
        )

        payment_transaction = PaymentTransaction(
            party=self.party,
            address=self.invoice_address,
            amount=amount,
            currency=self.currency,
            gateway=payment_method.gateway,
            sale=self,
        )
        payment_transaction.save()

        return payment_method.process(payment_transaction)

    def nereid_pay_using_profile(self, payment_profile_id, amount):
        """
        Pay the amount using the given profile. Ensures that the profile
        belongs to the current user.
        """
        PaymentProfile = Pool().get('party.payment_profile')

        payment_profile = PaymentProfile(payment_profile_id)
        if payment_profile.party != current_user.party:
            # verify that the payment profile belongs to the registered
            # user.
            flash(_('The payment profile chosen is invalid'))
            return redirect(
                url_for('nereid.checkout.payment_method')
            )
        return self._pay_using_profile(payment_profile, amount)

    @route('/order/<int:active_id>/add-comment', methods=['POST'])
    def add_comment_to_sale(self):
        """
        Add comment to sale.

        User can add comment or note to sale order.
        """
        comment_is_allowed = False

        if self.state not in ['confirmed', 'processing']:
            abort(403)

        if current_user.is_anonymous():
            access_code = request.values.get('access_code', None)
            if access_code and access_code == self.guest_access_code:
                # No access code provided
                comment_is_allowed = True

        elif current_user.is_authenticated() and \
                current_user.party == self.party:
            comment_is_allowed = True

        if not comment_is_allowed:
            abort(403)

        if request.form.get('comment') and not self.comment \
                and self.state == 'confirmed':
            self.comment = request.form.get('comment')
            self.save()
            if request.is_xhr:
                return jsonify({
                    'message': 'Comment Added',
                    'comment': self.comment,
                })

            flash(_('Comment Added'))
        return redirect(request.referrer)

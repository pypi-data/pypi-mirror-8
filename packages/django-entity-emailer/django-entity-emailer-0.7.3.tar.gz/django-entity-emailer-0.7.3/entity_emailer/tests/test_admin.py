from datetime import datetime

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django_dynamic_fixture import G, F
from entity.models import Entity, EntityRelationship, EntityKind
from entity_event.models import Source

from entity_emailer import admin
from entity_emailer.models import Email, EmailTemplate, GroupEmail, IndividualEmail
from entity_emailer.tests.utils import g_email


class SubentityContentTypeQsTest(TestCase):
    def setUp(self):
        self.sub_entity_kind_1 = G(EntityKind)
        self.sub_entity_kind_2 = G(EntityKind)
        self.super_entity_type = G(EntityKind)
        sub_entity_1 = G(Entity, entity_kind=self.sub_entity_kind_1)
        sub_entity_2 = G(Entity, entity_kind=self.sub_entity_kind_2)
        super_entity = G(Entity, entity_kind=self.super_entity_type)
        G(EntityRelationship, sub_entity=sub_entity_1, super_entity=super_entity)
        G(EntityRelationship, sub_entity=sub_entity_2, super_entity=super_entity)

    def test_returns_sub_entity_kinds(self):
        self.assertIn(self.sub_entity_kind_1, list(EntityKind.objects.all()))
        self.assertIn(self.sub_entity_kind_2, list(EntityKind.objects.all()))


class GetAllSuperEntitiesQsTest(TestCase):
    def setUp(self):
        self.super_entity_1 = G(Entity)
        self.sub_entity_1 = G(Entity)
        G(EntityRelationship, sub_entity=self.sub_entity_1, super_entity=self.super_entity_1)

    def test_filters_out_sub_entities(self):
        qs = admin.get_all_super_entities_qs()
        self.assertNotIn(self.sub_entity_1, list(qs))

    def test_includes_super_entities(self):
        qs = admin.get_all_super_entities_qs()
        self.assertIn(self.super_entity_1, list(qs))


class GetAllEmailableEntitiesTest(TestCase):
    def setUp(self):
        self.email_entity = G(Entity, entity_meta={'email': 'test@example.com'})
        self.no_email_entity = G(Entity, entity_meta={'name': 'Mr. T'})
        self.no_meta_entity = G(Entity)

    def test_filters_out_no_email(self):
        qs = admin.get_all_emailable_entities_qs()
        self.assertNotIn(self.no_email_entity, list(qs))

    def test_filters_out_no_meta(self):
        qs = admin.get_all_emailable_entities_qs()
        self.assertNotIn(self.no_meta_entity, list(qs))

    def test_includes_email_entities(self):
        qs = admin.get_all_emailable_entities_qs()
        self.assertIn(self.email_entity, list(qs))


class CreateGroupEmailFormTest(TestCase):
    def setUp(self):
        test_entity = G(Entity)
        test_entity_sub = G(Entity)
        G(EntityRelationship, sub_entity=test_entity_sub, super_entity=test_entity)
        G(Source, name='admin')
        G(EmailTemplate, template_name='html_safe', html_template='{{ html|safe }}')
        self.email_form_data = {
            'subject': 'A Test Email Subject',
            'from_email': 'test@example.com',
            'to_entity': test_entity.id,
            'body': '<html><body><p>This is the email body</p></body></html>',
        }

    def test_save_creates_email(self):
        form = admin.CreateGroupEmailForm(self.email_form_data)
        form.is_valid()
        form.save()
        self.assertTrue(Email.objects.exists())

    def test_save_with_scheduled_date_time(self):
        self.email_form_data.update({
            'scheduled_date_year': '2014',
            'scheduled_date_month': '8',
            'scheduled_date_day': '15',
            'scheduled_time': '13:31',
        })
        form = admin.CreateGroupEmailForm(self.email_form_data)
        form.is_valid()
        form.save()
        self.assertTrue(Email.objects.exists())

    def test_save_m2m_exists(self):
        form = admin.CreateGroupEmailForm(self.email_form_data)
        form.save_m2m()


class CreateIndividualEmailFormTest(TestCase):
    def setUp(self):
        test_entity_sub_1 = G(Entity, entity_meta={'email': 'one@example.com'})
        test_entity_sub_2 = G(Entity, entity_meta={'email': 'two@example.com'})
        G(Source, name='admin')
        G(EmailTemplate, template_name='html_safe', html_template='{{ html|safe }}')
        self.email_form_data = {
            'subject': 'A Test Email Subject',
            'from_email': 'test@example.com',
            'to_entities': [test_entity_sub_1.id, test_entity_sub_2.id],
            'body': '<html><body><p>This is the email body</p></body></html>',
        }

    def test_save_creates_email(self):
        form = admin.CreateIndividualEmailForm(self.email_form_data)
        form.fields['to_entities'].queryset = admin.get_all_emailable_entities_qs()
        form.is_valid()
        form.save()
        self.assertTrue(Email.objects.exists())

    def test_save_with_scheduled_date_time(self):
        self.email_form_data.update({
            'scheduled_date_year': '2014',
            'scheduled_date_month': '8',
            'scheduled_date_day': '15',
            'scheduled_time': '13:31',
        })
        form = admin.CreateIndividualEmailForm(self.email_form_data)
        form.fields['to_entities'].queryset = admin.get_all_emailable_entities_qs()
        form.is_valid()
        form.save()
        self.assertTrue(Email.objects.exists())

    def test_save_m2m_exists(self):
        form = admin.CreateIndividualEmailForm(self.email_form_data)
        form.save_m2m()


class GroupEmailAdminTest(TestCase):
    def setUp(self):
        self.ek = G(EntityKind)
        self.site = AdminSite()
        self.entity = G(Entity, entity_meta={'name': 'entity_name'}, display_name='entity_name')
        self.email = g_email(
            sent=datetime(2014, 1, 1, 12, 34), recipients=[self.entity], context={},
            template=F(text_template_path='hi'))

    def test_get_queryset_filters_non_admin(self):
        admin_template = G(EmailTemplate, template_name='html_safe', text_template="...")
        other_template = G(EmailTemplate, template_name='other', text_template="...")
        g_email(template=admin_template, context={}, sub_entity_kind=self.ek)
        g_email(template=other_template, context={}, sub_entity_kind=self.ek)
        email_admin = admin.GroupEmailAdmin(GroupEmail, self.site)
        qs = email_admin.get_queryset(None)
        self.assertEqual(qs.count(), 1)

    def test_has_been_sent(self):
        email_admin = admin.GroupEmailAdmin(GroupEmail, self.site)
        sent = email_admin.has_been_sent(self.email)
        self.assertTrue(sent)

    def test_has_not_been_sent(self):
        email_admin = admin.GroupEmailAdmin(GroupEmail, self.site)
        not_sent = email_admin.has_been_sent(Email())
        self.assertFalse(not_sent)

    def test_to(self):
        email_admin = admin.GroupEmailAdmin(GroupEmail, self.site)
        to = email_admin.to(self.email)
        self.assertEqual(to, 'entity_name')


class IndividualEmailAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.entity = G(Entity, entity_meta={'name': 'entity_name'}, display_name='entity_name')
        self.email = g_email(
            sent=datetime(2014, 1, 1, 12, 34), recipients=[self.entity], context={},
            template=F(text_template_path='hi'))

    def test_get_queryset_filters_non_admin(self):
        admin_template = G(EmailTemplate, template_name='html_safe', text_template="...")
        other_template = G(EmailTemplate, template_name='other', text_template="...")
        g_email(template=admin_template, context={})
        g_email(template=other_template, context={})
        email_admin = admin.IndividualEmailAdmin(Email, self.site)
        qs = email_admin.get_queryset(None)
        self.assertEqual(qs.count(), 1)

    def test_has_been_sent(self):
        email_admin = admin.IndividualEmailAdmin(IndividualEmail, self.site)
        sent = email_admin.has_been_sent(self.email)
        self.assertTrue(sent)

    def test_has_not_been_sent(self):
        email_admin = admin.IndividualEmailAdmin(IndividualEmail, self.site)
        not_sent = email_admin.has_been_sent(Email())
        self.assertFalse(not_sent)

    def test_to(self):
        email_admin = admin.IndividualEmailAdmin(IndividualEmail, self.site)
        to = email_admin.to(self.email)
        self.assertEqual(to, 'entity_name')


class EmailAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.entity = G(Entity, entity_meta={'name': 'entity_name'}, display_name='entity_name')
        self.email = g_email(
            sent=datetime(2014, 1, 1, 12, 34), recipients=[self.entity], context={},
            template=F(text_template_path='hi'))

    def test_has_not_been_sent(self):
        email_admin = admin.EmailAdmin(Email, self.site)
        not_sent = email_admin.has_been_sent(Email())
        self.assertFalse(not_sent)

    def test_to(self):
        email_admin = admin.EmailAdmin(Email, self.site)
        to = email_admin.to(self.email)
        self.assertEqual(to, 'entity_name')

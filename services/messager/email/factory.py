from services.messager.email import SUBJECT_BOSS, SUBJECT_CUSTOMER
from services.messager.email.models import EmailMessager, Template
from services.messager.email.models import Customer,Type,Book

TEMPLATES = {
    Type.PREVENT: lambda customer: TemplateFactory.build_customer_template(customer),
    Type.IMPORTANT: lambda customer: TemplateFactory.build_boss_template(customer)
}
def build_email_message(customer: Customer,type:Type):
    template: Template
    template = TEMPLATES[type](customer)
    return EmailMessager(\
        customer.email,\
        template.template,\
        template.subject,\
        template.data).get_email_message()


class TemplateFactory:
    @staticmethod
    def build_customer_template(customer)->Template:
        template='customer_mail.html'
        subject=SUBJECT_CUSTOMER
        data={
            'name': customer.name,
            'books': [Book(title='a', code='1', due_date='2025-07-01'), Book(title='b', code='2', due_date='2025-07-02'), Book(title='c', code='3', due_date='2025-07-03')] if customer.books == [] else customer.books
        }
        return Template(template,subject,data)
    
    @staticmethod
    def build_boss_template(customer)->Template:
        template='customer_mail.html'
        subject=SUBJECT_BOSS
        data={
            'name': customer.name,
            'books': ['a','c']
        }
        return Template(template,subject,data)



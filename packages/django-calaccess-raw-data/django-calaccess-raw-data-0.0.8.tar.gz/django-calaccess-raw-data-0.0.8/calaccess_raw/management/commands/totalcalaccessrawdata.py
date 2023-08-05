from calaccess_raw import get_model_list
from django.core.management.base import BaseCommand
from django.contrib.humanize.templatetags.humanize import intcomma


class Command(BaseCommand):
    help = "Print out the total of CAL-ACCESS tables and rows in the database"

    def handle(self, *args, **kwargs):
        model_list = get_model_list()
        print "%s total database tables" % len(model_list)
        record_count = 0
        for m in model_list:
            record_count += m.objects.count()
        print "%s total database records" % intcomma(record_count)

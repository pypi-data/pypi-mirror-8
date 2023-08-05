# This script is to be run as a one-off to fix up some of the changes to
# Torfaen wards/communities in the May 2014 edition of Boundary-Line that
# should not have been present.
#
# http://www.legislation.gov.uk/wsi/2013/2156/contents/made is the source for
# all of this. Specifically, section 2 saying that articles 5, 6 and 10 don't
# come into operation until before the next election, which is 2017.
#
# This script will revoke the changes made for the purposes of articles 5 and
# 6, but the changes for article 10 overlap with changes for (active) articles
# 8 and 9, so we will live with those being incorrect until Ordnance Survey
# release hopefully fixed boundaries in October.

from optparse import make_option
from django.core.management.base import NoArgsCommand
from mapit.models import Area

def disp(areas):
    if isinstance(areas, Area):
        areas = [ areas ]
    return ', '.join( a.all_codes['gss'] for a in areas )

class Command(NoArgsCommand):
    help = 'Fix some of the Torfaen wards in the May 2014 UK Boundary-Line import'
    option_list = NoArgsCommand.option_list + (
        make_option('--commit', action='store_true', dest='commit', help='Actually update the database'),
    )

    def move(self, name, code, starts=False):
        areas = Area.objects.filter(parent_area=self.torfaen, type__code=code)
        if starts:
            areas = areas.filter(name__startswith=name)
        else:
            areas = areas.filter(name=name)
        old = areas.filter(generation_high_id=21)
        new = areas.filter(generation_low_id=22)
        if self.commit:
            old.update(generation_high_id=22)
            new.delete()
        else:
            print 'Would delete %s and reinstate %s' % (disp(new), disp(old))

    def handle_noargs(self, **options):
        self.commit = options['commit']
        self.torfaen = Area.objects.get(name='Torfaen Council', type__code='UTA')

        # Article 5 moved some of New Inn to Croesyceiliog
        self.move('Croesyceiliog North', 'UTE')
        self.move('Croesyceiliog Community', 'CPC')
        self.move('New Inn', 'UTE')
        self.move('New Inn Community', 'CPC')

        # Article 6 split up Llanyrafon into West/East rather than North/South
        self.move('Llanyrafon', 'UTE', True)

        # Article 7 moved some of Abersychan to Pen Tranch (Snatchwood UTE)
        # Article 8 moved some of Upper Cwmbran to Pontnewydd
        # Article 9 moved some of Fairwater to Cwmbran Central (Greenmeadow to St Dials UTEs)
        #    These three have come into operation.

        # Article 10 moved some of Fairwater to Upper Cwmbran (Greenmeadow to Upper Cwmbran UTEs)
        #    Not reverting article 10 changes, see above

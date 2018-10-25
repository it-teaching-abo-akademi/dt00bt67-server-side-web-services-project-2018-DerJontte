import traceback

from django.db.models.functions import datetime
from django_cron import CronJobBase, Schedule

from auctionApp.models import Auction


class ResolveAuctions(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'auctionApp.resolve_auctions'    # a unique code

    def do(self):
        print("Resolving auctions...")

        tf='%Y%m%d%H%M%S'
        current_time = datetime.datetime.now().strftime(tf)

        resolvable = []

        for auction in Auction.objects.all():
            if auction.time_closing.strftime(tf) < current_time and \
                    auction.active and \
                    not auction.banned:
                resolvable.append(auction)
        print (resolvable)

        for auction in resolvable:
            body1 = ''
            body2 = ''
            # auction.active = False
            # auction.resolved = True

            subject = 'Auction "%s" has finished' % auction.title
            print(subject)
            if auction.bidders_set.count() == 0:
                body1 = 'Auction number %d: "%s" has finished. Unfortunately no bids were made.' % (auction.id, auction.title)
            else:
                body1 = 'Auction number %d: "%s" has finished. The highest bid was %d EUR by %s.' % (auction.id, auction.title, auction.current_price, auction.current_winner_name)
                body2 = 'Please contact each other to finalise the deal. User %s`s email is %s and %s`s is.' % (auction.seller_name, auction.seller_email, auction.current_winner_name)
            print(body1, body2)
            try:
                print(auction.bidders_set.get(user_id=auction.current_winner_id).email)
            except:
                traceback.print_exc()



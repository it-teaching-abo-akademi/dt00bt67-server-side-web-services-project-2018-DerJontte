import traceback

from django.core.mail import send_mail
from django.db import transaction
from django.db.models.functions import datetime
from django_cron import CronJobBase, Schedule

from auctionApp.models import Auction

class ResolveAuctions(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'auctionApp.resolve_auctions'

    def do(self):
        print("Resolving auctions...")

        tf='%Y%m%d%H%M%S'
        current_time = datetime.datetime.now().strftime(tf)
        resolvable = []
        for auction in Auction.objects.all():
            add_to_resolvable = auction.time_closing.strftime(tf) < current_time and auction.active and not auction.banned
            # Debugging output:
            # print(auction.time_closing.strftime(tf), 'Deadline passed: ', auction.time_closing.strftime(tf) < current_time, ' Banned: ', auction.banned, ' Active: ' , auction.active, ' Resolved: ', auction.resolved, ' Add to resolvable: ' , add_to_resolvable,  ' Title: ', auction.title)

            if add_to_resolvable:
                resolvable.append(auction)

        if resolvable is None:
            print ('No active unresolved auctions found.')
            return

        for auction in resolvable:
            recipients = [auction.seller_email]
            if auction.bid_set.count() > 0:
                winner_email = auction.bid_set.get(user_id=auction.current_winner_id).email
                recipients.append(winner_email)
                body = 'Auction number %d: "%s" has finished. The highest bid was %d EUR by %s.\n\n' % (auction.id, auction.title, auction.current_price, auction.current_winner_name)
                body = body + 'Please contact each other to finalize the deal. User %s`s email is %s and %s`s is %s.' % (auction.seller_name, auction.seller_email, auction.current_winner_name, winner_email)
            else:
                body = 'Auction number %d: "%s" has finished. Unfortunately no bids were made.' % (auction.id, auction.title)

            subject = 'Auction "%s" has finished' % auction.title

            send_mail(subject, body, 'resolver@yaas', recipients)

            auction.active = False
            auction.resolved = True
            auction.save()

            print ('Auction id %d: "%s" resolved.' % (auction.id, auction.title))


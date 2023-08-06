#
# Adlib API migration
# Extension

from datetime import datetime, timedelta
from plone.registry.record import Record
from plone.registry import field
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

def migrate(self):
    from collective.adlibsyncmanager.sync_mechanism import SyncMechanism
    
    folder = "nl/collectie/schilderijen"

    #
    # Create or GET registry record
    #
    registry = getUtility(IRegistry)
    try:
        last_request_successful = registry.records['last_request_successful'].value
        last_successful_date = registry.records['last_successful_date'].value
        request_period = registry.records['request_period'].value
        print "Last request successfull %s" % (last_request_successful)
        print "last successfull date %s" % (last_successful_date)
        print "request period %smin" % (str(request_period))
    except:
        print "Create new records!"
        ten_days_ago = datetime.today() - timedelta(days = 10)
        last_date = ten_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        unicode_date = u"%s" % (last_date)
        registry.records['last_request_successful'] = Record(field.Bool(title=u"last_request_successful"), False)
        registry.records['last_successful_date'] = Record(field.Text(title=u"last_successful_date"), unicode_date)
        registry.records['request_period'] = Record(field.Int(title=u"request_period"), 1)

    #
    #Define date based on last request
    #

    if last_request_successful:
        one_minute_ago = datetime.today() - timedelta(minutes = request_period)
        date = one_minute_ago.strftime('%Y-%m-%d %H:%M:%S')
    else:
        date = last_successful_date
    
    #
    # Define request type
    #
    request_type = "sync_date"
    
    #Create the migrator
    sync = SyncMechanism(self, date, request_type, folder)
    
    print("=== Starting Sync. ===")

    # # # # # # # # #

    sync.start_sync()
    
    # # # # # # # # #
    
    if sync.success:
        # Update last_successful_request
        sync_date_unicode = u"%s" % (sync.date)
        registry.records['last_request_successful'] = Record(field.Bool(title=u"last_request_successful"), True)
        registry.records['last_successful_date'] = Record(field.Text(title=u"last_successful_date"), sync_date_unicode)
        registry.records['request_period'] = Record(field.Int(title=u"request_period"), request_period)

        #
        # Store last successful request
        #
        return "=== Sync Successfull ===\nObjects updated: %s\nObjects skipped: %s\nErrors: %s" % (sync.updated, sync.skipped, sync.errors)
    else:
        sync_date_unicode = u"%s" % (sync.date)
        registry.records['last_request_successful'] = Record(field.Bool(title=u"last_request_successful"), False)
        registry.records['last_successful_date'] = Record(field.Text(title=u"last_successful_date"), sync_date_unicode)
        registry.records['request_period'] = Record(field.Int(title=u"request_period"), request_period)

        return "=== Sync Unsuccessfull ===\nObjects updated: %s\nObjects skipped: %s\nErrors: %s" % (sync.updated, sync.skipped, sync.errors)

        
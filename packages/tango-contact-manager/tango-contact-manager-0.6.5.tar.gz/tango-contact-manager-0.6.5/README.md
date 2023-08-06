Tango Contact Manager
=====

Provides contact forms and any other sort of user submission form you might want. You can create new forms on the fly, straight from the admin.

## Key features
* Simple contact forms or complex user-submission forms -- it's your call
* Create new forms on the fly through the Django admin
* Email addresses are never exposed to spammers
* Submissions can be emailed or stored in your database
* Submissions can be displayed on site
* Submissions can include a photo.

##Installation:

    pip install tango-contact-manager
or 
    pip install git+https://github.com/tBaxter/tango-contact-manager.git


## Usage:
Add 'contact_manager' and 'tango_shared' to your installed apps, then run syncdb or migrate.

tango_shared is a dependency. It will be installed for you.

Site emails will be sent to superusers or anyone specified in a DEFAULT_CONTACTS setting. That setting should be a list of emails.
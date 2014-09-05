django-condenser
==========

Condenses duplicate or similar model entries in installed apps.

Sometimes your team doesn't realize that they have put in two entries into the database that should have really been just one. This allows you to pick the canonical entry and collapse all others into that one. All related objects that pointed to the objects that were deleted will now point to the canonical object left over.

An example is in order:

Say you have a model called School, when in use, the client puts in several schools as such:

- Smalltown High
- Smalltown High School
- Smalltown High Bears

Even if you did your due diligence and made the name field unique, you can run into this scenario.

The idea is then to pick the right entry and have all others deleted. Any related models will then have their relationships changed to the one that's left over.
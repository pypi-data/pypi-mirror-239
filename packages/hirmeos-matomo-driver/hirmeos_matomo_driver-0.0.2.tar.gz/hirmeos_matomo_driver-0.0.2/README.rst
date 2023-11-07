=============
MATOMO Driver
=============

This driver allows programmatic retrieval and normalisation of Matomo usage
data, obtained via the Matomo API.

The driver code covers the following scenarios:
  * Number of visits to pages on the target website.
  * Number of downloads from different pages on the target website.
  * Number of events, by category, if these have been set up in matomo.

Documentation about querying the matomo api can be found here:
https://developer.matomo.org/api-reference/reporting-api


Release Notes:
==============

[0.0.2] - 2013-11-03
---------------------

Added:
    * Serializers were added to ingest the response JSON.
    * Specific requests methods to support the functionality provided by
      the `Actions.getPageUrls`, `Actions.getDownloads` and
      `Events.getNameFromCategoryId` methods.
    * Optional Regex processing, to filter URL results by expected patterns.

Changed:
    * Response returns serialized data rather than raw JSON response.


[0.0.1] - 2013-10-09
---------------------

Added:
    * Make a request to the matomo API, and return the JSON response.

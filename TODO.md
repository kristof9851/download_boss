## TODO

- DelayWrapper should not use fixed delays, but calculate the time between now and the last request, and just make sure the calculated delay has taken place in between the two requests

* Add more Clients to support:
  * file
  * aws
  * ssh
  * git

* Add more wrappers
  * ExtractWrapper  // zip, tar, tgz

* Add higher-level client libraries to help with URL templating and parsing responses into objects
  * JiraHttpClient
  * Gitlab...
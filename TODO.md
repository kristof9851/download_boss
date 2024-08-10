## TODO

```
    multi protocol download support
        // implements Download interface #download(request);
        http/s      OK
        file
        aws
        ssh
        git

    wrappers
        // implements same Download interface
        // execute something before and after, invokes main logic
        RetryWrapper        OK  
        FileCacheWrapper    OK
        DelayWrapper        OK
        ExtractWrapper  // zip, tar, tgz

    client libraries
        JiraHttpClient
        Gitlab...
        Canvas...
        Spr...
```
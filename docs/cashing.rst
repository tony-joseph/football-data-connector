***************************
Caching and Lazy Evaluation
***************************

Values in a **DataSet** object are cached during the creation of DataSet.
Subsequent calls to methods which returns a **DataSet** will be returning the
cached values. These methods will accept an optional parameter,
*force_update*, which if set to **True**, will force an API call again and
fetch new values. You should force update only on situations where it is
absolutely necessary. Otherwise you may hit the API rate limit.

A **DataSet** will not perform any API calls during its creation. There will
not be any values in a **DataSet** after its creation. API call is executed
only when an action which uses the data is executed such as using in a for
loop, checking the length of **DataSet** etc.

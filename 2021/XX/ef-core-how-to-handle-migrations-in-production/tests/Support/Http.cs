using System;
using System.Collections.Generic;
using System.Web;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Primitives;

namespace Tests.Support
{
    public static class Http
    {
        public static IQueryCollection RetrieveQueryCollectionFromQueryString(string queryString)
        {
            var queryParamsDictionary = new Dictionary<String, StringValues>();
            var queryStringCollection = HttpUtility.ParseQueryString(queryString);

            foreach (string key in queryStringCollection)
            {
                var value = queryStringCollection[key];
                queryParamsDictionary.Add(key, new[] {value});
            }

            return new QueryCollection(queryParamsDictionary);
        }
    }
}

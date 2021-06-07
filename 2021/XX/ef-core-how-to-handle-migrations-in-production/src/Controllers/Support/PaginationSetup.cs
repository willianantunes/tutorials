using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Web;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Primitives;

namespace EFCoreHandlingMigrations.Controllers.Support
{
    public record Paginated<T>(int Count, string? Next, string? Previous, IEnumerable<T> Results);

    public interface IPagination
    {
        public Task<Paginated<T>> CreateAsync<T>(IQueryable<T> source, string url, IQueryCollection queryParams);
    }

    public class Pagination : IPagination
    {
        private readonly int _defaultLimit;
        private readonly int _maxPageSize;
        private readonly string _limitQueryParam = "limit";
        private readonly string _offsetQueryParam = "offset";

        public Pagination(int defaultPageSize, int maxPageSize=25)
        {
            _defaultLimit = defaultPageSize;
            _maxPageSize = maxPageSize;
        }

        public async Task<Paginated<T>> CreateAsync<T>(IQueryable<T> source, string url, IQueryCollection queryParams)
        {
            // Extracting query strings
            var limitQueryParam = queryParams.FirstOrDefault(pair => pair.Key == _limitQueryParam);
            var offsetQueryParam = queryParams.FirstOrDefault(pair => pair.Key == _offsetQueryParam);
            // Setting basic data
            var numberOfRowsToSkip = RetrieveConfiguredOffset(offsetQueryParam.Value);
            var numberOfRowsToTake = RetrieveConfiguredLimit(limitQueryParam.Value);
            var count = await source.CountAsync();
            var nextLink = RetrieveNextLink(url, numberOfRowsToSkip, numberOfRowsToTake, count);
            var previousLink = RetrievePreviousLink(url, numberOfRowsToSkip, numberOfRowsToTake);
            // Building list
            var items = await source.Skip(numberOfRowsToSkip).Take(numberOfRowsToTake).ToListAsync();

            return new Paginated<T>(count, nextLink, previousLink, items);
        }

        private string? RetrievePreviousLink(string url, int numberOfRowsToSkip, int numberOfRowsToTake)
        {
            if (numberOfRowsToSkip == 0)
                return null;
            
            var uriBuilder = new UriBuilder(url);
            var query = HttpUtility.ParseQueryString(uriBuilder.Query);
            query[_limitQueryParam] = numberOfRowsToTake.ToString();

            var shouldNotProvideOffset = numberOfRowsToSkip - numberOfRowsToTake <= 0;
            if (shouldNotProvideOffset)
            {
                uriBuilder.Query = query.ToString();
                return uriBuilder.Uri.AbsoluteUri;
            }

            var newOffSetValue = numberOfRowsToSkip - numberOfRowsToTake;

            query[_offsetQueryParam] = newOffSetValue.ToString();
            uriBuilder.Query = query.ToString();

            return uriBuilder.Uri.AbsoluteUri;
        }

        private string? RetrieveNextLink(string url, int numberOfRowsToSkip, int numberOfRowsToTake, int count)
        {
            var greaterThanTheAmountOfRowsAvailable = numberOfRowsToSkip + numberOfRowsToTake >= count;
            if (greaterThanTheAmountOfRowsAvailable) return null;

            var newOffSetValue = numberOfRowsToSkip + numberOfRowsToTake;

            var uriBuilder = new UriBuilder(url);
            var query = HttpUtility.ParseQueryString(uriBuilder.Query);
            query[_offsetQueryParam] = newOffSetValue.ToString();
            query[_limitQueryParam] = numberOfRowsToTake.ToString();
            uriBuilder.Query = query.ToString();

            return uriBuilder.Uri.AbsoluteUri;
        }

        private int RetrieveConfiguredOffset(StringValues values)
        {
            int defaultOffSetValue = 0;
            var value = values.FirstOrDefault();

            if (value is not null)
            {
                int requestedOffsetValue;
                var couldBeParsed = int.TryParse(value, out requestedOffsetValue);

                if (couldBeParsed && requestedOffsetValue > 0)
                    return requestedOffsetValue;
            }

            return defaultOffSetValue;
        }

        private int RetrieveConfiguredLimit(StringValues values)
        {
            var value = values.FirstOrDefault();

            if (value is not null)
            {
                int requestedLimitValue;
                var couldBeParsed = int.TryParse(value, out requestedLimitValue);

                if (couldBeParsed && requestedLimitValue > 0) {
                    var valueToBeReturned = requestedLimitValue > _maxPageSize ? _maxPageSize : requestedLimitValue;
                    return valueToBeReturned;
                }
            }

            return _defaultLimit;
        }
    }
}

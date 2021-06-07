using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Controllers.Support;
using FluentAssertions;
using Tests.Support;
using Xunit;

namespace Tests.EFCoreHandlingMigrations.Controllers.Support
{
    public record Person(int Id, string Name);

    public class PaginationSetupITests
    {
        public class Options
        {
            private readonly int _defaultPageLimit;
            private readonly Pagination _pagination;
            private readonly InMemoryDbContextBuilder.TestDbContext<Person> _dbContext;
            private readonly string _url;
            private readonly int _defaultMaxPageLimit;

            public Options()
            {
                _dbContext = InMemoryDbContextBuilder.CreateDbContext<Person>();
                _defaultPageLimit = 10;
                _defaultMaxPageLimit = 25;
                _pagination = new Pagination(_defaultPageLimit, _defaultMaxPageLimit);
                _url = "https://www.willianantunes.com";
            }

            [Fact(DisplayName = "When no options such as limit or offset are provided")]
            public async Task ShouldCreatePaginatedScenarioOptions1()
            {
                // Arrange
                var query = await CreateScenarioWith50Persons(_dbContext);
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(String.Empty);
                // Act
                var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                // Assert
                paginated.Count.Should().Be(50);
                paginated.Results.Should().HaveCount(_defaultPageLimit);
                paginated.Previous.Should().BeNull();
                paginated.Next.Should().Be($"{_url}/?offset=10&limit=10");
            }

            [Fact(DisplayName = "When either limit or offset receive values different than int")]
            public async Task ShouldCreatePaginatedScenarioOptions2()
            {
                // Arrange
                var query = await CreateScenarioWith50Persons(_dbContext);
                var queryString = "offset=jafar&limit=aladdin";
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(queryString);
                // Act
                var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                // Assert
                paginated.Count.Should().Be(50);
                paginated.Results.Should().HaveCount(_defaultPageLimit);
                paginated.Previous.Should().BeNull();
                paginated.Next.Should().Be($"{_url}/?offset=10&limit=10");
            }

            [Fact(DisplayName = "When only offset is configured")]
            public async Task ShouldCreatePaginatedScenarioOptions3()
            {
                // Arrange
                var query = await CreateScenarioWith50Persons(_dbContext);
                var offsetValue = 23;
                var queryString = $"offset={offsetValue}";
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(queryString);
                // Act
                var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                // Assert
                paginated.Count.Should().Be(50);
                paginated.Results.Should().HaveCount(_defaultPageLimit);
                paginated.Previous.Should().Be($"{_url}/?limit=10&offset={offsetValue - _defaultPageLimit}");
                paginated.Next.Should().Be($"{_url}/?offset={offsetValue + _defaultPageLimit}&limit=10");
            }

            [Fact(DisplayName = "When provided limit is higher than what is allowed")]
            public async Task ShouldCreatePaginatedScenarioOptions4()
            {
                // Arrange
                var query = await CreateScenarioWith50Persons(_dbContext);
                var queryString = "limit=1000";
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(queryString);
                // Act
                var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                // Assert
                paginated.Count.Should().Be(50);
                paginated.Results.Should().HaveCount(_defaultMaxPageLimit);
                paginated.Previous.Should().BeNull();
                paginated.Next.Should().Be($"{_url}/?offset={_defaultMaxPageLimit}&limit={_defaultMaxPageLimit}");
            }
        }

        public class Navigations
        {
            private readonly int _defaultPageLimit;
            private readonly Pagination _pagination;
            private readonly InMemoryDbContextBuilder.TestDbContext<Person> _dbContext;
            private readonly string _url;
            private readonly int _defaultMaxPageLimit;

            public Navigations()
            {
                _dbContext = InMemoryDbContextBuilder.CreateDbContext<Person>();
                _defaultPageLimit = 10;
                _defaultMaxPageLimit = 25;
                _pagination = new Pagination(_defaultPageLimit, _defaultMaxPageLimit);
                _url = "https://www.willianantunes.com";
            }

            [Fact(DisplayName =
                "When the navigation goes from the beginning to end with no provided options at the start")]
            public async Task ShouldCreatePaginatedScenarioNavigation1()
            {
                // First arrangement
                var query = await CreateScenarioWith50Persons(_dbContext);
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(String.Empty);
                var shouldGetNextPagination = true;
                var listOfPrevious = new List<string>();
                var listOfNext = new List<string>();
                // Act
                while (shouldGetNextPagination)
                {
                    var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                    paginated.Count.Should().Be(50);
                    paginated.Results.Should().HaveCount(_defaultPageLimit);
                    listOfPrevious.Add(paginated.Previous);
                    listOfNext.Add(paginated.Next);
                    if (paginated.Next is null)
                        shouldGetNextPagination = false;
                    else
                    {
                        var queryStrings = paginated.Next.Split("?")[1];
                        queryParams = Http.RetrieveQueryCollectionFromQueryString(queryStrings);
                    }
                }

                // Assert
                var expectedListOfPrevious = new List<string>
                {
                    null,
                    $"{_url}/?limit=10",
                    $"{_url}/?limit=10&offset=10",
                    $"{_url}/?limit=10&offset=20",
                    $"{_url}/?limit=10&offset=30",
                };
                var expectedListOfNext = new List<string>
                {
                    $"{_url}/?offset=10&limit=10",
                    $"{_url}/?offset=20&limit=10",
                    $"{_url}/?offset=30&limit=10",
                    $"{_url}/?offset=40&limit=10",
                    null
                };
                listOfPrevious.Should().Equal(expectedListOfPrevious);
                listOfNext.Should().Equal(expectedListOfNext);
            }

            [Fact(DisplayName = "When the navigation goes from the end to beginning")]
            public async Task ShouldCreatePaginatedScenarioNavigation2()
            {
                // First arrangement
                var query = await CreateScenarioWith50Persons(_dbContext);
                var queryString = "offset=40&limit=10";
                var queryParams = Http.RetrieveQueryCollectionFromQueryString(queryString);
                var shouldGetPreviousPagination = true;
                var listOfPrevious = new List<string>();
                var listOfNext = new List<string>();
                // Act
                while (shouldGetPreviousPagination)
                {
                    var paginated = await _pagination.CreateAsync(query, _url, queryParams);
                    paginated.Count.Should().Be(50);
                    paginated.Results.Should().HaveCount(_defaultPageLimit);
                    listOfPrevious.Add(paginated.Previous);
                    listOfNext.Add(paginated.Next);
                    if (paginated.Previous is null)
                        shouldGetPreviousPagination = false;
                    else
                    {
                        var queryStrings = paginated.Previous.Split("?")[1];
                        queryParams = Http.RetrieveQueryCollectionFromQueryString(queryStrings);
                    }
                }

                // Assert
                var expectedListOfPrevious = new List<string>
                {
                    $"{_url}/?limit=10&offset=30",
                    $"{_url}/?limit=10&offset=20",
                    $"{_url}/?limit=10&offset=10",
                    $"{_url}/?limit=10",
                    null,
                };
                var expectedListOfNext = new List<string>
                {
                    null,
                    $"{_url}/?offset=40&limit=10",
                    $"{_url}/?offset=30&limit=10",
                    $"{_url}/?offset=20&limit=10",
                    $"{_url}/?offset=10&limit=10",
                };
                listOfPrevious.Should().Equal(expectedListOfPrevious);
                listOfNext.Should().Equal(expectedListOfNext);
            }
        }

        private static async Task<IQueryable<Person>> CreateScenarioWith50Persons(InMemoryDbContextBuilder.TestDbContext<Person> dbContext)
        {
            var persons = new List<Person>();

            foreach (int index in Enumerable.Range(1, 50))
            {
                var person = new Person(index, $"Person {index}");
                persons.Add(person);
            }

            await dbContext.AddRangeAsync(persons);
            await dbContext.SaveChangesAsync();

            return dbContext.Entities.AsQueryable();
        }
    }
}

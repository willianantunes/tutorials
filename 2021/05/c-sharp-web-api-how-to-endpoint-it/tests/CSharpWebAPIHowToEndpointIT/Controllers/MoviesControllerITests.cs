using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using CSharpWebAPIHowToEndpointIT;
using CSharpWebAPIHowToEndpointIT.Models;
using CSharpWebAPIHowToEndpointIT.Services;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Moq;
using Xunit;

namespace Tests.CSharpWebAPIHowToEndpointIT.Controllers
{
    public class MoviesControllerITests : IClassFixture<WebApplicationFactory<Startup>>
    {
        private readonly IFilmSpecialist _filmSpecialist;
        private HttpClient _httpClient;

        public MoviesControllerITests(WebApplicationFactory<Startup> factory)
        {
            _filmSpecialist = Mock.Of<IFilmSpecialist>();
            _httpClient = factory.WithWebHostBuilder(builder =>
            {
                // https://docs.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-5.0#inject-mock-services
                builder.ConfigureTestServices(services =>
                {
                    services.RemoveAll<IFilmSpecialist>();
                    services.TryAddTransient(_ => _filmSpecialist);
                });
            }).CreateClient();
        }

        [Fact]
        public async Task ShouldCreateGameGivenFirstMovementIsBeingExecuted()
        {
            // Arrange
            var requestPath = "/api/v1/movies";
            var movieToBeSuggested = new Movie("Schindler's List", "12/31/1993", new[] {"Drama", "History", "War"}, "3h 15m");
            Mock.Get(_filmSpecialist)
                .Setup(f => f.SuggestSomeMovie())
                .Returns(movieToBeSuggested)
                .Verifiable();
            // Act
            var response = await _httpClient.GetAsync(requestPath);
            response.StatusCode.Should().Be(HttpStatusCode.OK);
            var movie = await response.Content.ReadFromJsonAsync<Movie>();
            // Assert
            movie.Should().BeEquivalentTo(movieToBeSuggested);
            Mock.Get(_filmSpecialist).Verify();
        }
    }
}

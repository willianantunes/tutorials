using CSharpWebAPIHowToEndpointIT.Services;
using FluentAssertions;
using Xunit;

namespace Tests.CSharpWebAPIHowToEndpointIT.Services
{
    public class FilmSpecialistTests
    {
        private readonly IFilmSpecialist _filmSpecialist = new FilmSpecialist();

        [Fact]
        public void ShouldReturnRandomMovieWhenAsked()
        {
            // Act
            var suggestedMovie = _filmSpecialist.SuggestSomeMovie();
            // Assert
            var expectedTiles = new[]
            {
                "RoboCop", "The Matrix", "Soul", "Space Jam", "Aladdin", "The World of Dragon Ball Z"
            };
            suggestedMovie.Title.Should().BeOneOf(expectedTiles);
        }
    }
}

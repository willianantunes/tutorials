using System;
using CSharpWebAPIHowToEndpointIT.Models;
using Serilog;

namespace CSharpWebAPIHowToEndpointIT.Services
{
    public interface IFilmSpecialist
    {
        Movie SuggestSomeMovie();
    }

    public class FilmSpecialist : IFilmSpecialist
    {
        private static readonly Movie[] Films =
        {
            new("RoboCop", "10/08/1987", new[] {"Action", "Thriller", "Science Fiction"}, "1h 42m"),
            new("The Matrix", "05/21/1999", new[] {"Action", "Science Fiction"}, "2h 16m"),
            new("Soul", "12/25/2020", new[] {"Family", "Animation", "Comedy", "Drama", "Music", "Fantasy"}, "1h 41m"),
            new("Space Jam", "12/25/1996", new[] {"Adventure", "Animation", "Comedy", "Family"}, "1h 28m"),
            new("Aladdin", "07/03/1993", new[] {"Animation", "Family", "Adventure", "Fantasy", "Romance"}, "1h 28m"),
            new("The World of Dragon Ball Z", "01/21/2000", new[] {"Action"}, "20m"),
        };

        public Movie SuggestSomeMovie()
        {
            Log.Debug("OKAY! Which film will I suggest 🤔");
            Random random = new();
            var filmIndexThatIWillSuggest = random.Next(0, Films.Length);
            Log.Information("Will suggest the film with index {FilmIndex}!", filmIndexThatIWillSuggest);

            return Films[filmIndexThatIWillSuggest];
        }
    }
}

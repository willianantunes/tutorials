namespace CSharpWebAPIHowToEndpointIT.Models
{
    public class Movie
    {
        public string Title { get; }
        public string Release { get; }
        public string[] Genres { get; }
        public string Duration { get; }

        public Movie(string title, string release, string[] genres, string duration)
        {
            Title = title;
            Release = release;
            Genres = genres;
            Duration = duration;
        }
    }
}

using CSharpWebAPIHowToEndpointIT.Models;
using CSharpWebAPIHowToEndpointIT.Services;
using Microsoft.AspNetCore.Mvc;
using Serilog;

namespace CSharpWebAPIHowToEndpointIT.Controllers.V1
{
    [ApiController]
    [Route("api/v1/[controller]")]
    public class MoviesController : ControllerBase
    {
        private readonly IFilmSpecialist _filmSpecialist;

        public MoviesController(IFilmSpecialist filmSpecialist)
        {
            _filmSpecialist = filmSpecialist;
        }

        [HttpGet]
        public Movie Get()
        {
            Log.Information("Let me ask the film specialist...");
            var movie = _filmSpecialist.SuggestSomeMovie();
            Log.Information("Suggested movie: {Movie}", movie);
            return movie;
        }
    }
}

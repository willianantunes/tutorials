using FlaggyApi;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Unleash;

namespace Flaggy.Controllers;

[ApiController]
[Route("[controller]")]
public class PostsController : ControllerBase
{
    private readonly ApplicationContext _context;
    private readonly IUnleash _featureManagementClient;

    public PostsController(ApplicationContext context, IUnleash featureManagementClient)
    {
        _context = context;
        _featureManagementClient = featureManagementClient;
    }

    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var contextAboutTheUser = (HttpContext.Items["ContextAboutTheUser"] as UnleashContext)!;
        var showTags = _featureManagementClient.IsEnabled(FeatureFlags.ShowTags, contextAboutTheUser);
        var posts = await _context.Posts.AsNoTracking().ToListAsync();

        if (showTags is false)
            foreach (var post in posts)
                post.Tags = new List<Tag>();


        return Ok(posts);
    }

    [FeatureGate(FeatureFlags.AddPost)]
    [HttpPost("{blogId}:int")]
    public async Task<IActionResult> AddPost([FromRoute] int blogId, PostRequest newPost)
    {
        var post = new Post
        {
            Title = newPost.Title,
            Content = newPost.Content,
            Tags = newPost.Tags.Select(x => new Tag {Value = x}).ToList(),
            BlogId = blogId
        };
        _context.Add(post);
        await _context.SaveChangesAsync();
        return Ok();
    }

    public record PostRequest(string Title, string Content, string[] Tags);
}

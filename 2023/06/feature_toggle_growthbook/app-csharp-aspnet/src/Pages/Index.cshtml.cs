using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace Flaggy.Pages;

public class IndexModel : PageModel
{
    private readonly ApplicationContext _context;

    public IndexModel(ApplicationContext context)
    {
        _context = context;
    }

    public IList<Post> Post { get; set; } = default!;
    public string ButtonSchemeValue { get; set; }

    public async Task OnGetAsync()
    {
        Post = await _context.Posts.Include(p => p.Blog).ToListAsync();
        var gb = (HttpContext.Items["ContextFeatureToggle"] as GrowthBook.GrowthBook)!;
        var value = gb.GetFeatureValue(FeatureFlags.ButtonSchemeValue, "btn-dark")!;
        ButtonSchemeValue = value;
    }
}

using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using Unleash;
using Unleash.Internal;
using Unleash.Variants;

namespace Flaggy.Pages;

public class IndexModel : PageModel
{
    private readonly ApplicationContext _context;
    private readonly IUnleash _featureManagementClient;

    public IndexModel(ApplicationContext context, IUnleash featureManagementClient)
    {
        _context = context;
        _featureManagementClient = featureManagementClient;
    }

    public IList<Post> Post { get; set; } = default!;
    public string ButtonSchemeValue { get; set; }

    public async Task OnGetAsync()
    {
        Post = await _context.Posts.Include(p => p.Blog).ToListAsync();
        var contextAboutTheUser = (HttpContext.Items["ContextAboutTheUser"] as UnleashContext)!;
        var variantDefault = new Variant(FeatureFlags.ButtonSchemeValue, new Payload("BTN-DARK", "btn-dark"), true);
        // We could add an overload of the method `GetVariant` so it can support only the toggle name and the context, without the default value
        var variant = _featureManagementClient.GetVariant(FeatureFlags.ButtonSchemeValue, contextAboutTheUser, variantDefault);
        ButtonSchemeValue = variant.Payload.Value;
    }
}

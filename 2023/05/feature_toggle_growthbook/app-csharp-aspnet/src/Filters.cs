using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace FlaggyApi;

public class FeatureGateAttribute : ActionFilterAttribute
{
    private readonly string _featureFlagKey;

    public FeatureGateAttribute(string featureFlagKey) => _featureFlagKey = featureFlagKey;

    public override async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var gb = (context.HttpContext.Items["ContextFeatureToggle"] as GrowthBook.GrowthBook)!;    
        var enabled = gb.IsOn(_featureFlagKey);

        if (enabled)
            await next();
        else
            context.Result = new StatusCodeResult(StatusCodes.Status404NotFound);
    }
}

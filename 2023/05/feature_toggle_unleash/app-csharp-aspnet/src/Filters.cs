using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Unleash;

namespace FlaggyApi;

public class FeatureGateAttribute : ActionFilterAttribute
{
    private readonly string _featureFlagKey;

    public FeatureGateAttribute(string featureFlagKey) => _featureFlagKey = featureFlagKey;

    public override async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var featureManagementClient = context.HttpContext.RequestServices.GetRequiredService<IUnleash>();
        var contextAboutTheUser = context.HttpContext.Items["ContextAboutTheUser"] as UnleashContext;
        var enabled = featureManagementClient.IsEnabled(_featureFlagKey, contextAboutTheUser);

        if (enabled)
            await next();
        else
            context.Result = new StatusCodeResult(StatusCodes.Status404NotFound);
    }
}

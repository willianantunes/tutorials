using Flaggy;
using Microsoft.EntityFrameworkCore;
using Unleash;
using Unleash.ClientFactory;
using Wangkanai.Detection.Models;
using Wangkanai.Detection.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddRazorPages();

// https://github.com/wangkanai/wangkanai/tree/9f7a9bdc9277a91608b06a1d8e9f3e1040067f47/Detection
builder.Services.AddDetection();

builder.Services.AddDbContext<ApplicationContext>(
    options => options.UseSqlServer(
        builder.Configuration.GetConnectionString("ApplicationContext")));

var featureFlagManagementClient = await AddUnLeashClient(builder);

var app = builder.Build();

app.Lifetime.ApplicationStopping.Register(() =>
{
    app.Logger.LogInformation("Disposing LaunchDarkly Client");
    featureFlagManagementClient.Dispose();
});

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

// Add feature flag context before proceeding any request
app.Use(async (context, next) =>
{
    var detectionService = context.RequestServices.GetRequiredService<IDetectionService>();
    const string userIdDesktop = "40956364-e486-4d8e-b35e-60660721f467";
    const string userIdMobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec";
    var finalUserId = detectionService.Device.Type == Device.Mobile ? userIdMobile : userIdDesktop;
    
    // https://docs.getunleash.io/reference/unleash-context
    // https://github.com/Unleash/unleash-client-dotnet/tree/dcc144883af898267a6d416c058db4b598d97815#providing-context
    context.Items["ContextAboutTheUser"] = new UnleashContext
    {
        UserId = finalUserId,
        Properties = new Dictionary<string, string>
        {
            {"UserAgent", detectionService.UserAgent.ToString()},
            {"Browser", detectionService.Browser.Name.ToString()},
            {"DeviceType", detectionService.Device.Type.ToString()},
            {"PlatformName", detectionService.Platform.Name.ToString()}
        }
    };
    await next.Invoke();
});

app.UseSwagger();
app.UseSwaggerUI();

app.UseStaticFiles();

// https://github.com/wangkanai/wangkanai/tree/9f7a9bdc9277a91608b06a1d8e9f3e1040067f47/Detection
// Make sure that you have app.UseDetection() before app.UseRouting 👀
app.UseDetection();

app.UseRouting();

app.UseAuthorization();

app.MapRazorPages();
app.MapControllers();

app.Run();

async Task<IUnleash> AddUnLeashClient(WebApplicationBuilder webApplicationBuilder)
{
    const string apiEndpointPlaceholder = "FeatureFlagManagement:ApiEndpoint";
    const string appNamePlaceholder = "FeatureFlagManagement:AppName";
    const string apiTokenPlaceholder = "FeatureFlagManagement:ApiToken";
    var apiEndpoint = webApplicationBuilder.Configuration.GetValue<string>(apiEndpointPlaceholder) ??
                      throw new ArgumentNullException(apiEndpointPlaceholder, "Property required");
    var appName = webApplicationBuilder.Configuration.GetValue<string>(appNamePlaceholder) ??
                  throw new ArgumentNullException(appNamePlaceholder, "Property required");
    var apiToken = webApplicationBuilder.Configuration.GetValue<string>(apiTokenPlaceholder) ??
                   throw new ArgumentNullException(apiTokenPlaceholder, "Property required");

    var settings = new UnleashSettings
    {
        AppName = appName,
        UnleashApi = new Uri(apiEndpoint),
        CustomHttpHeaders = new Dictionary<string, string> {{"Authorization", apiToken}}
    };
    var unleashFactory = new UnleashClientFactory();
    // https://github.com/Unleash/unleash-client-dotnet/tree/dcc144883af898267a6d416c058db4b598d97815#synchronous-startup
    var unleash = await unleashFactory.CreateClientAsync(settings, synchronousInitialization: true);
    webApplicationBuilder.Services.AddSingleton(_ => unleash);
    return unleash;
}

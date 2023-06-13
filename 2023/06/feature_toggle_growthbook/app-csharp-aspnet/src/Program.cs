using System.Net;
using Flaggy;
using GrowthBook;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Wangkanai.Detection.Models;
using Wangkanai.Detection.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();

builder.Services.AddRazorPages();

// https://github.com/wangkanai/wangkanai/tree/9f7a9bdc9277a91608b06a1d8e9f3e1040067f47/Detection
builder.Services.AddDetection();

builder.Services.AddDbContext<ApplicationContext>(
    options => options.UseSqlServer(
        builder.Configuration.GetConnectionString("ApplicationContext")));

var app = builder.Build();

app.Lifetime.ApplicationStopping.Register(() =>
{
    app.Logger.LogInformation("Stopping application...");
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
    // Retrieve required data from configuration
    var configuration = context.RequestServices.GetRequiredService<IConfiguration>();
    const string apiEndpointPlaceholder = "FeatureFlagManagement:ApiEndpoint";
    const string apiTokenPlaceholder = "FeatureFlagManagement:ApiToken";
    var apiEndpoint = configuration.GetValue<string>(apiEndpointPlaceholder) ??
                      throw new ArgumentNullException(apiEndpointPlaceholder, "Property required");
    var apiToken = configuration.GetValue<string>(apiTokenPlaceholder) ??
                   throw new ArgumentNullException(apiTokenPlaceholder, "Property required");
    // Retrieve features
    var httpClientFactory = context.RequestServices.GetRequiredService<IHttpClientFactory>();
    var httpClient = httpClientFactory.CreateClient();
    var url = $"{apiEndpoint}/api/features/{apiToken}";
    var response = await httpClient.GetAsync(url);
    if (response.IsSuccessStatusCode)
    {
        var content = await response.Content.ReadAsStringAsync();
        var featuresResult = JsonConvert.DeserializeObject<FeaturesResult>(content);
        var features = featuresResult!.Features;
        var gbContext = new Context
        {
            Enabled = true,
            Features = features
        };
        // Adding attributes
        var detectionService = context.RequestServices.GetRequiredService<IDetectionService>();
        const string userIdDesktop = "40956364-e486-4d8e-b35e-60660721f467";
        const string userIdMobile = "d821cbc0-2e4d-49fc-a5b4-990eb991beec";
        var browser = detectionService.Browser.Name.ToString().ToLower();
        var userId = detectionService.Device.Type == Device.Mobile ? userIdMobile : userIdDesktop;
        var finalUserId = browser == "firefox" ? Guid.NewGuid().ToString() : null;
        gbContext.Attributes["userId"] = finalUserId ?? userId;
        gbContext.Attributes["browser"] = browser;
        // Instantiating GrowthBook and adding to the context
        var gb = new GrowthBook.GrowthBook(gbContext);
        context.Items["ContextFeatureToggle"] = gb;
    }
    else
    {
        context.Response.Clear();
        context.Response.StatusCode = StatusCodes.Status503ServiceUnavailable;
        await context.Response.WriteAsync("Couldn't retrieve feature toggles");
        return;
    }
    await next.Invoke();
    (context.Items["ContextFeatureToggle"] as GrowthBook.GrowthBook)!.Dispose();
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

internal record FeaturesResult(HttpStatusCode Status, IDictionary<string, Feature>? Features,
    DateTimeOffset? DateUpdated);

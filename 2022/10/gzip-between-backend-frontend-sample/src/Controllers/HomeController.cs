using GZipBackendFrontendSample.Helpers;
using Microsoft.AspNetCore.Mvc;

namespace GZipBackendFrontendSample.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index()
    {
        return View();
    }

    [HttpGet]
    public async Task<ActionResult<string>> RetrieveGZippedContent(string text)
    {
        _logger.LogInformation("Received text: {text}", text);
        var compressedTextAsBase64 = await GZipNegotiator.CompressAndRetrieveItAsBase64StringAsync(text);
        _logger.LogInformation("Gzipped text as base64: {compressedTextAsBase64}", compressedTextAsBase64);
        return RedirectToAction("Index", new { compressedTextAsBase64 = compressedTextAsBase64 });
    }
}

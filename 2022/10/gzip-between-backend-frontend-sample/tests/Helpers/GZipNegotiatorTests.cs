using System.Net;
using System.Web;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.WebUtilities;
using Xunit;

namespace Tests.Helpers;

public class GZipNegotiatorTests
{
    [Fact]
    public async Task ShouldCompressTextAndRedirect()
    {
        // Arrange
        var application = new WebApplicationFactory<Program>();
        var client = application.CreateClient();
        var sampleText = "cockatiel";
        var param = new Dictionary<string, string?>
        {
            ["text"] = sampleText,
        };
        var requestUri = QueryHelpers.AddQueryString("/Home/RetrieveGZippedContent", param);
        // Act
        var response = await client.GetAsync(requestUri);
        // Assert
        var queryFromRequestUri = response.RequestMessage!.RequestUri!.Query;
        var compressedStringAsBase64 = HttpUtility.ParseQueryString(queryFromRequestUri)["compressedTextAsBase64"];
        Assert.True(Utils.IsBase64String(compressedStringAsBase64!));
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}

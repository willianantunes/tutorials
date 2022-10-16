using System.IO.Compression;
using System.Text;

namespace GZipBackendFrontendSample.Helpers;

public static class GZipNegotiator
{
    public static async Task<string> CompressAndRetrieveItAsBase64StringAsync(string input,
        CompressionLevel level = CompressionLevel.Optimal)
    {
        var inputAsBytes = Encoding.UTF8.GetBytes(input);

        using var memoryStream = new MemoryStream();
        await using (var gzipStream = new GZipStream(memoryStream, level))
            await gzipStream.WriteAsync(inputAsBytes);
        return Convert.ToBase64String(memoryStream.ToArray());
    }
}

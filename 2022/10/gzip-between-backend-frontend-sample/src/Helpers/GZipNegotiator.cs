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

    public static async Task<string> DecompressBase64StringAsync(string input)
    {
        var compressedValue = Convert.FromBase64String(input);
        using var memoryStream = new MemoryStream(compressedValue);
        using var outputStream = new MemoryStream();
        await using var decompressStream = new GZipStream(memoryStream, CompressionMode.Decompress);
        await decompressStream.CopyToAsync(outputStream);
        var rawValueAsBytes = outputStream.ToArray();
        return Encoding.UTF8.GetString(rawValueAsBytes);
    }
}

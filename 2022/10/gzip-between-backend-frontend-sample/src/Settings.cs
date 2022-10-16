namespace GZipBackendFrontendSample;

public interface ISettings
{
    string SiteName { get; }
}

public class Settings : ISettings
{
    public Settings()
    {
        SiteName = "GZipBackendFrontendSample";
    }

    public string SiteName { get; set; }
}

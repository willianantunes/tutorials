using EFCoreHandlingMigrations.EntryCommands;

namespace Tests.Support
{
    public class ApiIntegrationTests : IntegrationTestsFixture<ApiCommand.Startup>
    {
        // Just to avoid configuring ApiCommand.Startup as the generic type many times 😁
    }
}

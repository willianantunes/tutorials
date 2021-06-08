using System.Threading.Tasks;
using CliFx;
using CliFx.Attributes;
using CliFx.Infrastructure;
using EFCoreHandlingMigrations.Configs;
using Microsoft.Extensions.Configuration;

namespace EFCoreHandlingMigrations.EntryCommands
{
    [Command("task")]
    public class TaskCommand : ICommand
    {
        [CommandOption("seed", IsRequired = false, Description = "Fill database with fake data")]
        public bool SeedDatabase { get; init; } = false;

        public async ValueTask ExecuteAsync(IConsole console)
        {
            if (SeedDatabase is true)
            {
                var connectionStringName = "AppDbContext";
                var connectionString = Program.Configuration.GetConnectionString(connectionStringName);

                if (connectionString is not null)
                {
                    var dbContext = AppDbContext.CreateContext(connectionString);
                    await Seeder.CreateScenarioWith100TodoItems(dbContext);
                    await console.Output.WriteLineAsync("Seed has been executed!");
                }
                else
                {
                    await console.Error.WriteLineAsync($"You should add connection string for: {connectionStringName}");
                }
            }
        }
    }
}

using System;
using System.Linq;
using System.Net.Http;
using EFCoreHandlingMigrations;
using EFCoreHandlingMigrations.Configs;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Serilog;

namespace Tests.Support
{
    public abstract class IntegrationTestsFixture<TStartup> : IDisposable where TStartup : class
    {
        protected readonly HttpClient Client;
        protected readonly AppDbContext AppDbContext;
        private readonly IDbContextTransaction _transaction;

        public IntegrationTestsFixture()
        {
            // Basic setup
            var configuration = Program.BuildConfiguration();
            var builder = WebHost.CreateDefaultBuilder()
                .UseStartup<TStartup>()
                .UseSerilog();
            // You can create new clients with mocked services if required (see ConfigureTestServices)
            builder.ConfigureTestServices(ConfigureDabaseAsSingleton(configuration));
            var server = new TestServer(builder);
            var services = server.Host.Services;
            // It allows you to call API endpoints
            Client = server.CreateClient();
            // It allows you to consult the database
            AppDbContext = services.GetRequiredService<AppDbContext>();
            ExecuteMissingMigrations(AppDbContext);
            // The transaction will be created by each test method, if you inherit it without an IClassFixture
            _transaction = AppDbContext.Database.BeginTransaction();
        }

        private void ExecuteMissingMigrations(DbContext dbContext)
        {
            if (dbContext.Database.GetPendingMigrations().ToList().Any() is true)
                dbContext.Database.Migrate();
        }

        private Action<IServiceCollection> ConfigureDabaseAsSingleton(IConfiguration configuration)
        {
            return services =>
            {
                services.RemoveAll<AppDbContext>();
                services.AddHttpContextAccessor()
                    .AddDbContext<AppDbContext>(options =>
                            options.UseNpgsql(configuration.GetConnectionString("AppDbContext")),
                        ServiceLifetime.Singleton);
            };
        }

        public void Dispose()
        {
            if (_transaction is not null)
            {
                _transaction.Rollback();
                _transaction.Dispose();
            }
        }
    }
}

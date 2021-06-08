using System;
using System.Threading.Tasks;
using CliFx;
using CliFx.Attributes;
using CliFx.Infrastructure;
using DrfLikePaginations;
using EFCoreHandlingMigrations.Configs;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using Serilog;

namespace EFCoreHandlingMigrations.EntryCommands
{
    [Command("api")]
    public class ApiCommand : ICommand
    {
        public async ValueTask ExecuteAsync(IConsole console)
        {
            // We create our host and run our web api!
            await Program.CreateHostBuilder(Array.Empty<string>()).Build().RunAsync();
        }

        public class Startup
        {
            public IConfiguration Configuration { get; }

            public Startup(IConfiguration configuration)
            {
                Configuration = configuration;
            }

            public void ConfigureServices(IServiceCollection services)
            {
                // APIs
                services.AddControllers();
                services.AddSwaggerGen(c =>
                {
                    c.SwaggerDoc("v1", new OpenApiInfo {Title = "EFCoreHandlingMigrations", Version = "v1"});
                });
                // Database
                services.AddHttpContextAccessor().AddDbContext<AppDbContext>(optionsBuilder =>
                {
                    var connectionString = Configuration.GetConnectionString("AppDbContext");
                    optionsBuilder.UseNpgsql(connectionString);
                });
                // Custom services
                var paginationSize = int.Parse(Configuration["Pagination:Size"]);
                services.AddSingleton<IPagination>(new Pagination(paginationSize));
            }

            public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
            {
                if (env.IsDevelopment())
                {
                    app.UseDeveloperExceptionPage();
                    app.UseSwagger();
                    app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "EFCoreHandlingMigrations v1"));
                }

                app.UseSerilogRequestLogging();

                app.UseRouting();

                app.UseAuthorization();

                app.UseEndpoints(endpoints => { endpoints.MapControllers(); });
            }
        }
    }
}

using Bogus;
using CliFx;
using CliFx.Attributes;
using CliFx.Infrastructure;
using Flaggy;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace Commands;

[Command("seed")]
public class SeedCommand : ICommand
{
    public ValueTask ExecuteAsync(IConsole console)
    {
        var configuration = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .AddEnvironmentVariables().Build();
        var options = new DbContextOptionsBuilder<ApplicationContext>()
            .UseSqlServer(configuration.GetConnectionString("ApplicationContext"))
            .Options;
        using (var context = new ApplicationContext(options))
        {
            console.Output.WriteLine("Getting migrations...");
            if (context.Database.GetMigrations().Any())
                context.Database.Migrate();
            var blogFaker = CreateFakeBlogs();

            var blogs = blogFaker.Generate(10);

            context.Blogs.AddRange(blogs);
            console.Output.WriteLine("Seeding db...");
            context.SaveChanges();
        }

        console.Output.WriteLine("Done!");
        return new ValueTask();
    }

    private static Faker<Blog> CreateFakeBlogs()
    {
        var random = new Randomizer();

        var postFaker = new Faker<Post>()
            .RuleFor(x => x.Content, (f, _) => f.Lorem.Paragraph())
            .RuleFor(x => x.Title, (f, _) => f.Lorem.Sentence())
            .RuleFor(x => x.Tags, (f, _) => f.Lorem
                .Words(random.Number(1, 3))
                .Select(word => new Tag { Value = word }).ToList());

        var blogFaker = new Faker<Blog>()
            .RuleFor(x => x.Url, (f, b) => f.Internet.Url())
            .RuleFor(x => x.Posts,
                (f, b) => postFaker.Generate(random.Number(3, 10)));
        return blogFaker;
    }
}

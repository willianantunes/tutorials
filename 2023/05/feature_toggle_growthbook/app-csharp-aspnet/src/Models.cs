using Microsoft.EntityFrameworkCore;

namespace Flaggy;

public class ApplicationContext : DbContext
{
    public DbSet<Blog> Blogs => Set<Blog>();
    public DbSet<Post> Posts => Set<Post>();

    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder) =>
        modelBuilder
            .Entity<Post>()
            .OwnsMany(p => p.Tags, builder => builder.ToJson());
}

public class Blog
{
    public int BlogId { get; set; }
    public string Url { get; set; }

    public List<Post> Posts { get; set; } = new();
}

public class Post
{
    public int PostId { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }

    public int BlogId { get; set; }
    public Blog? Blog { get; set; }
    public List<Tag> Tags { get; set; } = new();
}


public class Tag
{
    public string Value { get; set; }
    public static implicit operator string(Tag tag) => tag.Value;
    public static implicit operator Tag(string tag) => new() { Value = tag };
}

using System;
using Microsoft.EntityFrameworkCore;

namespace Tests.Support
{
    public static class InMemoryDbContextBuilder
    {
        public class TestDbContext<TEntity> : DbContext where TEntity : class
        {
            public DbSet<TEntity> Entities { get; set; }

            public TestDbContext(DbContextOptions<TestDbContext<TEntity>> options) : base(options)
            {
            }
        }

        public static TestDbContext<T> CreateDbContext<T>() where T : class
        {
            var databaseName = Guid.NewGuid().ToString();
            var dbContextOptions = new DbContextOptionsBuilder<TestDbContext<T>>().UseInMemoryDatabase(databaseName).Options;
            var context = new TestDbContext<T>(dbContextOptions);

            return context;
        }
    }
}

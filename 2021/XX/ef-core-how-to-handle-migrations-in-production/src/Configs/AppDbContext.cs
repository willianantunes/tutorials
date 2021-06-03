using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Models;
using Microsoft.EntityFrameworkCore;

namespace EFCoreHandlingMigrations.Configs
{
    public class AppDbContext : DbContext
    {
        // Your models come here
        public DbSet<TodoItem> TodoItems { get; set; }
        
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
            
        }
        

        public override int SaveChanges()
        {
            AutomaticallyAddCreatedAndUpdatedAt();
            return base.SaveChanges();
        }

        public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
        {
            AutomaticallyAddCreatedAndUpdatedAt();
            return base.SaveChangesAsync(cancellationToken);
        }

        private void AutomaticallyAddCreatedAndUpdatedAt()
        {
            var entitiesOnDbContext = ChangeTracker.Entries<StandardEntity>();

            if (entitiesOnDbContext is null)
                return;

            foreach (var item in entitiesOnDbContext.Where(t => t.State == EntityState.Added))
            {
                item.Entity.CreatedAt = DateTime.Now;
                item.Entity.UpdatedAt = DateTime.Now;
            }

            foreach (var item in entitiesOnDbContext.Where(t => t.State == EntityState.Modified))
            {
                item.Entity.UpdatedAt = DateTime.Now;
            }
        }
    }
}

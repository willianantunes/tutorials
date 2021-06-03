namespace EFCoreHandlingMigrations.Models
{
    public class TodoItem  : StandardEntity
    {
        public string Name { get; set; }
        public bool IsComplete { get; set; }
    }
}

using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Models;
using Microsoft.EntityFrameworkCore;

namespace EFCoreHandlingMigrations.Configs
{
    public class Seeder
    {
        public static async Task CreateScenarioWith100TodoItems(AppDbContext dbContext)
        {
            var isThereAnyTodoItem = await dbContext.TodoItems.AnyAsync();
            if (isThereAnyTodoItem is not true)
            {
                var todoItems = new List<TodoItem>();

                foreach (int index in Enumerable.Range(1, 100))
                {
                    var isTodoItemComplete = index % 2 == 0;
                    var todoItem = new TodoItem {Name = $"TD {index}", IsComplete = isTodoItemComplete};
                    todoItems.Add(todoItem);
                }

                await dbContext.AddRangeAsync(todoItems);
                await dbContext.SaveChangesAsync();
            }
        }
    }
}

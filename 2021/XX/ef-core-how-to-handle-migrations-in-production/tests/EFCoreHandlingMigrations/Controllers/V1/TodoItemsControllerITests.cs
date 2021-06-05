using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http.Json;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Models;
using FluentAssertions;
using Tests.Support;
using Xunit;

namespace Tests.EFCoreHandlingMigrations.Controllers.V1
{
    public class TodoItemsControllerITests : ApiIntegrationTests
    {
        [Fact(DisplayName = "Should return todo items")]
        public async Task ShouldReturnTodoItems()
        {
            // Arrange
            await createScenarioWith25TodoItems();
            var requestUri = "/api/v1/TodoItems";
            // Act
            var response = await Client.GetAsync(requestUri);
            var todoItems = await response.Content.ReadFromJsonAsync<List<TodoItem>>();
            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);
            todoItems.Count.Should().Be(25);
        }

        private async Task createScenarioWith25TodoItems()
        {
            var gameRooms = new List<TodoItem>();
            
            foreach (int index in Enumerable.Range(1, 25))
            {
                var isTodoItemComplete = index % 2 == 0;
                var todoItem = new TodoItem {Name = $"TD {index}", IsComplete = isTodoItemComplete};
                gameRooms.Add(todoItem);
            }
            
            await AppDbContext.AddRangeAsync(gameRooms);
            await AppDbContext.SaveChangesAsync();
        }
    }
}

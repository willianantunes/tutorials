using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Models;
using FluentAssertions;
using Newtonsoft.Json.Linq;
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
            var valueAsString = await response.Content.ReadAsStringAsync();
            var responseJson = JObject.Parse(valueAsString);
            var count = responseJson["count"].ToObject<int>();
            var nextPage = responseJson["next"].ToObject<string>();
            var previousPage = responseJson["previous"].ToObject<string>();
            var todoItems = responseJson["results"].ToObject<List<TodoItem>>();
            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.OK);
            count.Should().Be(25);
            nextPage.Should().Be("http://localhost/api/v1/TodoItems?offset=5&limit=5");
            previousPage.Should().BeNull();
            todoItems.Count.Should().Be(5);
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

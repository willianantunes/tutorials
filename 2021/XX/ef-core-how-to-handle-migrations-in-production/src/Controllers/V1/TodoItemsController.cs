using System;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Configs;
using EFCoreHandlingMigrations.Controllers.Support;
using EFCoreHandlingMigrations.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.Extensions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace EFCoreHandlingMigrations.Controllers.V1
{
    [ApiController]
    [Route("api/v1/[controller]")]
    public class TodoItemsController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly DbSet<TodoItem> _databaseSet;
        private readonly IPagination _pagination;

        public TodoItemsController(AppDbContext context, IPagination pagination)
        {
            _context = context;
            _databaseSet = context.TodoItems;
            _pagination = pagination;
        }

        [HttpGet]
        public async Task<Paginated<TodoItem>> GetTodoItems()
        {
            var query = _databaseSet.AsQueryable();
            var displayUrl = Request.GetDisplayUrl();
            var queryParams = Request.Query;

            return await _pagination.CreateAsync(query, displayUrl, queryParams);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<TodoItem>> GetTodoItem(Guid id)
        {
            var todoItem = await _databaseSet.FindAsync(id);

            if (todoItem is null)
                return NotFound();

            return todoItem;
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> PutTodoItem(long id, TodoItem todoItem)
        {
            if (id != todoItem.Id)
                return BadRequest();

            _context.Entry(todoItem).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (_databaseSet.Any(e => e.Id == id) is not true)
                    return NotFound();

                throw;
            }

            return NoContent();
        }

        [HttpPost]
        public async Task<ActionResult<TodoItem>> PostTodoItem(TodoItem todoItem)
        {
            _databaseSet.Add(todoItem);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetTodoItem", new {id = todoItem.Id}, todoItem);
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult<TodoItem>> DeleteTodoItem(Guid id)
        {
            var todoItem = await _databaseSet.FindAsync(id);

            if (todoItem is null)
                return NotFound();

            _databaseSet.Remove(todoItem);
            await _context.SaveChangesAsync();

            return todoItem;
        }
    }
}

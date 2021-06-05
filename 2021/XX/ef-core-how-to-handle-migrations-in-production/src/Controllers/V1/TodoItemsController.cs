using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using EFCoreHandlingMigrations.Configs;
using EFCoreHandlingMigrations.Models;
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

        public TodoItemsController(AppDbContext context)
        {
            _context = context;
            _databaseSet = context.TodoItems;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<TodoItem>>> GetTodoItems()
        {
            return await _databaseSet.ToListAsync();
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

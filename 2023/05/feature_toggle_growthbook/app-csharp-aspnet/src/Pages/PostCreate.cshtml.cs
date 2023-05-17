using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace Flaggy.Pages;

public class CreateModel : PageModel
{
    private readonly ApplicationContext _context;

    public CreateModel(ApplicationContext context)
    {
        _context = context;
    }

    public IActionResult OnGet()
    {
        ViewData["BlogId"] = new SelectList(_context.Blogs, "BlogId", "BlogId");
        return Page();
    }

    [BindProperty] public Post Post { get; set; } = default!;

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid || Post is null)
        {
            ViewData["BlogId"] = new SelectList(_context.Blogs, "BlogId", "BlogId");
            return Page();
        }

        _context.Posts.Add(Post);
        await _context.SaveChangesAsync();

        return RedirectToPage("./Index");
    }
}

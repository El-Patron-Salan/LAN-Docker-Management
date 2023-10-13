using JsonProperties;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace Controllers
{
    [ApiController]
    public class DockerInfoController : Controller
    {
    private readonly DockerInfoContext _context;

    public DockerInfoController(DockerInfoContext context)
    {
        _context = context;
    }

    [HttpGet("API/containers information")]
    public async Task<ActionResult<IEnumerable<ContainerProperties>>> GetContainers()
    {
        var containers = await _context.containers.ToListAsync();
        return Ok(containers);
    }

    [HttpGet("API/images information")]
    public async Task<ActionResult<IEnumerable<ImageProperties>>> GetImages()
    {
        var images = await _context.images.ToListAsync();
        return Ok(images);
    }

    [HttpGet("API/logs")]
    public async Task<ActionResult<IEnumerable<LogProperties>>> GetLog()
    {
        var log = await _context.create_logs.ToListAsync();
        return Ok(log);
    }

    [HttpPost("API/create-container")]
    public async Task<ActionResult<PullProperties>> CreateContainer([FromBody] PullProperties pullProperties)
    {
        if (pullProperties == null || string.IsNullOrWhiteSpace(pullProperties.image_name) || string.IsNullOrWhiteSpace(pullProperties.image_version))
        {
            return BadRequest("Invalid input. Please provide 'image_name' and 'image_version'.");
        }

        string image_name = pullProperties.image_name;
        string image_version = pullProperties.image_version;

        _context.pull.Add(pullProperties);
        await _context.SaveChangesAsync();

        return Ok(pullProperties);
    }

    }
}

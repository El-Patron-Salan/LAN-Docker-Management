using Microsoft.EntityFrameworkCore;
using JsonProperties;

public class DockerInfoContext : DbContext
{
    public DbSet<ImageProperties> images { get; set; }
    public DbSet<ContainerProperties> containers { get; set; }
    public DbSet<PullProperties> pull { get; set; }
    public DbSet<LogProperties> create_logs { get; set; }


    public DockerInfoContext(DbContextOptions<DockerInfoContext> options) : base(options) { }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            string connectionString = "Server=localhost;Database=docker_info;User=root;Password=SilneHaslo123;";
            optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
        }
    }
}
namespace JsonProperties
{
    public class ContainerProperties
    {
    public int ID { get; set; }
    public string? ID_container { get; set; }
    public DateTime? Created { get; set; } // Użyj DateTime? (nullable) dla obsługi wartości NULL
    public string? Status { get; set; }
    public string? ID_img { get; set; }
    }
}

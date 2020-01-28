using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using GeoJSON.Net.Feature;
using GeoJSON.Net.Geometry;
using Newtonsoft.Json;

namespace MyApp.Namespace
{
    // a POCO to match the JSON comming from Azure CLI
    public class AzureCLILocationPOCO 
    {
        public string displayName { get; set; }
        public string id { get; set; }
        public string latitude { get; set; }
        public string longitude { get; set; }
        public string name { get; set; }
        public string subscriptionId { get; set; }
    }
    
    public class GeoJsonModel : PageModel
    {
        [ViewData]
        public string JsonString { get; set; }
        public void OnGet()
        {
            try 
            {
                // Convert the result from Azure CLI output file to GeoJson and deliver to mapbox
                using (StreamReader sr = new StreamReader("Azure/list-locations.json"))
                {
                    // deserialize Json to List of POCOs
                    var azureCLILocations = new List<AzureCLILocationPOCO>();
                    azureCLILocations = 
                        System.Text.Json.JsonSerializer.Deserialize<List<AzureCLILocationPOCO>>(sr.ReadToEnd());

                    // Referenced FeatureCollection Unit Test for usage
                    // https://github.com/GeoJSON-Net/GeoJSON.Net/blob/master/src/GeoJSON.Net.Tests/Feature/FeatureCollectionTests.cs
                    var model = new FeatureCollection();
                    foreach (var location in azureCLILocations)
                    {
                        var geom = new Point(
                            new Position(location.latitude, location.longitude)
                        );

                        var props = new Dictionary<string, object>
                        {
                            { "region", location.displayName },
                            { "message", location.name },
                        };

                        var feature = new Feature(geom, props);
                        model.Features.Add(feature);
                    }

                    // serialize to Json string
                    var options = new JsonSerializerOptions
                    {
                        WriteIndented = true,
                    };
                    
                    // tried using the System version
                    // JsonString = System.Text.Json.JsonSerializer.Serialize(model, options);

                    // GeoJson.NET library doesn't work with the System version yet, so still
                    // using Newtonsoft version
                    JsonString = Newtonsoft.Json.JsonConvert.SerializeObject(model);
                    
                    // Console.WriteLine(JsonString);
                }
            }
            catch (Exception e) 
            {
                // Let the user know what went wrong.
                Console.WriteLine("The file could not be read:");
                Console.WriteLine(e.Message);
            }
        }
    }
}

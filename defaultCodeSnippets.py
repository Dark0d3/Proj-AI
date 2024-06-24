default_code_snippets = {
     '.csproj': """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.App" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="6.0.0" />
  </ItemGroup>
</Project>""",
    '.cshtml': "<!-- HTML template code -->\n<html>\n<head>\n    <title>Page Title</title>\n</head>\n<body>\n    <h1>This is a Heading</h1>\n    <p>This is a paragraph.</p>\n</body>\n</html>",
    '.js': "// JavaScript default code\ndocument.addEventListener('DOMContentLoaded', function() {\n    console.log('Page loaded');\n});",
    '.json': "{\n  \"key\": \"value\"\n}",
    '.html': "<!-- HTML default code -->\n<html>\n<head>\n    <title>Page Title</title>\n</head>\n<body>\n    <h1>This is a Heading</h1>\n    <p>This is a paragraph.</p>\n</body>\n</html>",
    # Add more file types and default codes as needed
}

default_code_snippets_dotnet = {
      'Startup.cs': """using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace MyAppNamespace
{
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllersWithViews();
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllerRoute(
                    name: "default",
                    pattern: "{controller=Home}/{action=Index}/{id?}");
            });
        }
    }
}""",
    'Program.cs': """using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace MyAppNamespace
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}""",
}
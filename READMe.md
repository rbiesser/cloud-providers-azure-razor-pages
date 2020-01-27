Cloud Computing Providers
---
Created following the tutorial located at:

https://docs.microsoft.com/en-us/aspnet/core/tutorials/razor-pages/razor-pages-start?view=aspnetcore-3.1&tabs=visual-studio-code

# Prerequisites
- Visual Studio Code
- C# for Visual Studio Code (Nuget Package)
- .NET CORE 3.1 SDK or later

# Create a Razor Pages web app
- Create a new folder to contain the project
```
dotnet new webapp
```

# Run the app
- Trust the HTTPS development certificate
```
dotnet dev-certs https --trust
```
- Run from the Terminal
```
dotnet run
```
- Or use the Debug menu, which uses .vscode/launch.json configuration
using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.JSInterop;

namespace MauiLearningPlatform.Services
{
    public class VirtualFile
    {
        public string Name { get; set; }
        public string Content { get; set; }
        public string Path { get; set; } // e.g., "ViewModels/MainViewModel.cs"
        public string Type { get; set; } // "csharp", "xml", "json", "image"

        public string Folder => Path.Contains("/") ? Path.Substring(0, Path.LastIndexOf("/")) : "";
    }

    public class ProjectState
    {
        public List<VirtualFile> Files { get; private set; } = new();
        public VirtualFile ActiveFile { get; private set; }
        public event Action OnChange;

        private readonly IJSRuntime _jsRuntime;
        private const string STORAGE_KEY = "maui_playground_files_v2"; // Versioned key to avoid conflict with old structure

        // Constructor injection for JSRuntime
        public ProjectState(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime;
            // We cannot call async JS here, so we initialize with defaults
            // and let the UI trigger the load
            LoadDefaultProject();
        }

        public async System.Threading.Tasks.Task LoadProjectAsync()
        {
            try
            {
                var json = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", STORAGE_KEY);
                if (!string.IsNullOrEmpty(json))
                {
                    var savedFiles = System.Text.Json.JsonSerializer.Deserialize<List<VirtualFile>>(json);
                    if (savedFiles != null && savedFiles.Count > 0)
                    {
                        Files = savedFiles;
                        // Try to restore active file, or default to MainViewModel
                        SetActiveFile(Files.FirstOrDefault(f => f.Name.EndsWith("MainViewModel.cs")) ?? Files.First());
                        NotifyStateChanged();
                        return;
                    }
                }
            }
            catch 
            {
                // Ignore errors, fallback to default
            }
            
            // If load failed or empty, ensure defaults are there
            if (Files.Count == 0) LoadDefaultProject();
        }

        public async void SaveProject()
        {
            try
            {
                var json = System.Text.Json.JsonSerializer.Serialize(Files);
                await _jsRuntime.InvokeVoidAsync("localStorage.setItem", new object[] { STORAGE_KEY, json });
            }
            catch
            {
                // Ignore save errors
            }
        }

        public string ExportProject()
        {
            return System.Text.Json.JsonSerializer.Serialize(Files);
        }

        public void ImportProject(string json)
        {
            try
            {
                var savedFiles = System.Text.Json.JsonSerializer.Deserialize<List<VirtualFile>>(json);
                if (savedFiles != null && savedFiles.Count > 0)
                {
                    Files = savedFiles;
                    SetActiveFile(Files.FirstOrDefault(f => f.Name.EndsWith("MainViewModel.cs")) ?? Files.First());
                    NotifyStateChanged();
                    SaveProject(); // Persist imported data
                }
            }
            catch
            {
                // Handle invalid JSON
            }
        }

        public void LoadDefaultProject()
        {
            Files.Clear();
            
            // Root Files
            AddFile("App.xaml", "<Application xmlns=\"http://schemas.microsoft.com/dotnet/2021/maui\"\n             xmlns:x=\"http://schemas.microsoft.com/winfx/2009/xaml\"\n             xmlns:local=\"clr-namespace:MauiLearningPlatform\"\n             x:Class=\"MauiLearningPlatform.App\">\n    <Application.MainPage>\n        <NavigationPage>\n            <x:Arguments>\n                <local:MainPage />\n            </x:Arguments>\n        </NavigationPage>\n    </Application.MainPage>\n</Application>", "xml", false);
            AddFile("AppShell.xaml", "<Shell xmlns=\"http://schemas.microsoft.com/dotnet/2021/maui\"\n       xmlns:x=\"http://schemas.microsoft.com/winfx/2009/xaml\"\n       x:Class=\"MauiLearningPlatform.AppShell\">\n</Shell>", "xml", false);
            AddFile("MauiProgram.cs", "namespace MauiLearningPlatform;\n\npublic static class MauiProgram\n{\n    public static MauiApp CreateMauiApp()\n    {\n        var builder = MauiApp.CreateBuilder();\n        builder\n            .UseMauiApp<App>()\n            .ConfigureFonts(fonts =>\n            {\n                fonts.AddFont(\"OpenSans-Regular.ttf\", \"OpenSansRegular\");\n            });\n\n        return builder.Build();\n    }\n}", "csharp", false);
            AddFile("GlobalUsings.cs", "global using MauiLearningPlatform.Data;\nglobal using MauiLearningPlatform.Models;\nglobal using MauiLearningPlatform.ViewModels;\nglobal using MauiLearningPlatform.Views;", "csharp", false);

            // Properties
            AddFile("Properties/launchSettings.json", "{\n  \"profiles\": {\n    \"Windows Machine\": {\n      \"commandName\": \"Project\",\n      \"nativeDebugging\": false\n    }\n  }\n}", "json", false);

            // Data
            AddFile("Data/IRepositories/INoteRepository.cs", "namespace MauiLearningPlatform.Data.IRepositories;\n\npublic interface INoteRepository\n{\n    void AddNote(string note);\n    List<string> GetNotes();\n}", "csharp", false);
            AddFile("Data/Repositories/NoteRepository.cs", "namespace MauiLearningPlatform.Data.Repositories;\n\npublic class NoteRepository : INoteRepository\n{\n    private List<string> _notes = new();\n\n    public void AddNote(string note)\n    {\n        _notes.Add(note);\n    }\n\n    public List<string> GetNotes()\n    {\n        return _notes;\n    }\n}", "csharp", false);

            // Models
            AddFile("Models/Note.cs", "namespace MauiLearningPlatform.Models;\n\npublic class Note\n{\n    public string Text { get; set; }\n    public DateTime Date { get; set; }\n}", "csharp", false);

            // Platforms (Empty placeholders for structure)
            AddFile("Platforms/Android/MainActivity.cs", "// Android specific code", "csharp", false);
            AddFile("Platforms/iOS/AppDelegate.cs", "// iOS specific code", "csharp", false);
            AddFile("Platforms/Windows/App.xaml.cs", "// Windows specific code", "csharp", false);

            // Resources
            AddFile("Resources/Images/dotnet_bot.svg", "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjNTEyQkQ0IiBkPSJNMjU2IDUxMkEyNTYgMjU2IDAgMSAwIDI1NiAwYTI1NiAyNTYgMCAxIDAgMCA1MTJ6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTM2Ny42IDM2Ny42aC0yMjMuMnYtMjIzLjJoMjIzLjJ2MjIzLjJ6Ii8+PC9zdmc+", "image", false); // Placeholder
            AddFile("Resources/Styles/Colors.xaml", "<ResourceDictionary xmlns=\"http://schemas.microsoft.com/dotnet/2021/maui\"\n                    xmlns:x=\"http://schemas.microsoft.com/winfx/2009/xaml\">\n    <Color x:Key=\"Primary\">#512BD4</Color>\n</ResourceDictionary>", "xml", false);

            // ViewModels
            AddFile("ViewModels/MainViewModel.cs", "using CommunityToolkit.Mvvm.ComponentModel;\nusing CommunityToolkit.Mvvm.Input;\nusing System.Collections.ObjectModel;\nusing MauiLearningPlatform.Data.IRepositories;\n\nnamespace MauiLearningPlatform.ViewModels;\n\npublic partial class MainViewModel : ObservableObject\n{\n    private readonly INoteRepository _repository;\n\n    [ObservableProperty]\n    private string newNoteText;\n\n    public ObservableCollection<string> Notes { get; } = new();\n\n    public MainViewModel(INoteRepository repository)\n    {\n        _repository = repository;\n        Refresh();\n    }\n\n    [RelayCommand]\n    private void AddNote()\n    {\n        if (!string.IsNullOrWhiteSpace(NewNoteText))\n        {\n            _repository.AddNote(NewNoteText);\n            NewNoteText = string.Empty;\n            Refresh();\n        }\n    }\n\n    private void Refresh()\n    {\n        Notes.Clear();\n        foreach (var note in _repository.GetNotes())\n        {\n            Notes.Add(note);\n        }\n    }\n}", "csharp", false);

            // Views
            AddFile("Views/MainPage.xaml", "<ContentPage xmlns=\"http://schemas.microsoft.com/dotnet/2021/maui\"\n             xmlns:x=\"http://schemas.microsoft.com/winfx/2009/xaml\"\n             xmlns:vm=\"clr-namespace:MauiLearningPlatform.ViewModels\"\n             x:Class=\"MauiLearningPlatform.Views.MainPage\"\n             Title=\"Notes\">\n    <ContentPage.BindingContext>\n        <vm:MainViewModel />\n    </ContentPage.BindingContext>\n    <VerticalStackLayout Padding=\"20\" Spacing=\"10\">\n        <Image Source=\"dotnet_bot.svg\" HeightRequest=\"200\" HorizontalOptions=\"Center\" />\n        <Entry Text=\"{Binding NewNoteText}\" Placeholder=\"Enter note...\" />\n        <Button Text=\"Add Note\" Command=\"{Binding AddNoteCommand}\" />\n        <CollectionView ItemsSource=\"{Binding Notes}\">\n            <CollectionView.ItemTemplate>\n                <DataTemplate>\n                    <Label Text=\"{Binding .}\" FontSize=\"18\" />\n                </DataTemplate>\n            </CollectionView.ItemTemplate>\n        </CollectionView>\n    </VerticalStackLayout>\n</ContentPage>", "xml", false);

            // Exercise 2: Color Picker
            AddFile("Views/ColorPickerPage.xaml", "<ContentPage xmlns=\"http://schemas.microsoft.com/dotnet/2021/maui\"\n             xmlns:x=\"http://schemas.microsoft.com/winfx/2009/xaml\"\n             xmlns:vm=\"clr-namespace:MauiLearningPlatform.ViewModels\"\n             x:Class=\"MauiLearningPlatform.Views.ColorPickerPage\"\n             Title=\"Color Picker\">\n    <ContentPage.BindingContext>\n        <vm:ColorPickerViewModel />\n    </ContentPage.BindingContext>\n    <VerticalStackLayout Padding=\"20\" Spacing=\"20\">\n        <BoxView Color=\"{Binding CurrentColor}\" HeightRequest=\"200\" WidthRequest=\"200\" HorizontalOptions=\"Center\" />\n        <Label Text=\"Red\" />\n        <Slider Minimum=\"0\" Maximum=\"255\" Value=\"{Binding Red}\" />\n        <Label Text=\"Green\" />\n        <Slider Minimum=\"0\" Maximum=\"255\" Value=\"{Binding Green}\" />\n        <Label Text=\"Blue\" />\n        <Slider Minimum=\"0\" Maximum=\"255\" Value=\"{Binding Blue}\" />\n        <Label Text=\"(Note: Color updates require a smarter SimulationEngine)\" TextColor=\"Gray\" HorizontalOptions=\"Center\" />\n    </VerticalStackLayout>\n</ContentPage>", "xml", false);

            AddFile("ViewModels/ColorPickerViewModel.cs", "using CommunityToolkit.Mvvm.ComponentModel;\n\nnamespace MauiLearningPlatform.ViewModels;\n\npublic partial class ColorPickerViewModel : ObservableObject\n{\n    [ObservableProperty]\n    private double red;\n\n    [ObservableProperty]\n    private double green;\n\n    [ObservableProperty]\n    private double blue;\n\n    // In a real app, this would update automatically.\n    // In this simulation, we default to a static color because the engine\n    // doesn't support complex property change logic yet.\n    public string CurrentColor { get; set; } = \"#512BD4\";\n}", "csharp", false);

            SetActiveFile(Files.FirstOrDefault(f => f.Name == "MainViewModel.cs"));
        }

        public void AddFile(string path, string content, string type, bool save = true)
        {
            if (Files.Any(f => f.Path == path)) return; // Prevent duplicates

            var file = new VirtualFile 
            { 
                Path = path, 
                Name = path.Contains("/") ? path.Substring(path.LastIndexOf("/") + 1) : path,
                Content = content, 
                Type = type 
            };
            Files.Add(file);
            NotifyStateChanged();
            if (save) SaveProject();
        }

        public void DeleteFile(VirtualFile file)
        {
            Files.Remove(file);
            if (ActiveFile == file)
            {
                ActiveFile = null;
            }
            NotifyStateChanged();
            SaveProject();
        }

        public void SetActiveFile(VirtualFile file)
        {
            ActiveFile = file;
            NotifyStateChanged();
        }

        public void UpdateFileContent(string path, string content)
        {
            var file = Files.FirstOrDefault(f => f.Path == path);
            if (file != null)
            {
                file.Content = content;
                // No notify here to avoid re-rendering editor while typing
                SaveProject();
            }
        }

        private void NotifyStateChanged() => OnChange?.Invoke();
    }
}

# Hoofdstuk 2 – Professionele Data-laag: Repositories, Interfaces & DI

Nu gaan we dieper: de ViewModel zou nooit rechtstreeks SQL, HTTP-calls, of file-IO moeten doen. Dat hoort in een aparte laag: de Repository.

We voegen onder de ViewModel een extra laag toe:
View → ViewModel → Repository (via Interface) → Database/API/Bestand

## 2.1 Menukaart & Keuken: Interface vs Repository

Stel:
- **Interface (ITodoRepository)** = menukaart. Hier staat: “Dit kan ik doen: HaalTakenOpAsync, VoegTaakToeAsync, …”. Geen implementatie.
- **Repository (TodoRepository)** = keuken. Hier beslis je hoe je die vragen uitvoert: via SQLite, REST API, JSON-file, etc.

**Voordelen:**
- **Flexibiliteit**: Je kunt later switchen van lokale database naar een web-API zonder de ViewModels aan te passen.
- **Testbaarheid**: Je kunt een “Fake” of “Mock” repository maken tijdens unit tests.

## 2.2 Model & Interface voor Todo’s

**Model – Models/TodoItem.cs**
```csharp
namespace MijnMauiApp.Models;

public class TodoItem
{
    public int Id { get; set; }
    public string Titel { get; set; }
    public bool IsAfgerond { get; set; }
}
```

**Interface – Services/ITodoRepository.cs**
```csharp
using MijnMauiApp.Models;

namespace MijnMauiApp.Services;

public interface ITodoRepository
{
    Task<List<TodoItem>> HaalAlleTakenOpAsync();
    Task VoegTaakToeAsync(TodoItem item);
    Task VerwijderTaakAsync(TodoItem item);
}
```
Let op het gebruik van `Task`: Data ophalen kost tijd → asynchroon (async/await). UI blijft responsief.

## 2.3 Implementatie van de Repository

**Services/TodoRepository.cs**
```csharp
using MijnMauiApp.Models;

namespace MijnMauiApp.Services;

public class TodoRepository : ITodoRepository
{
    private readonly List<TodoItem> _database = new();

    public async Task<List<TodoItem>> HaalAlleTakenOpAsync()
    {
        await Task.Delay(500); // Simuleer database- of netwerkvertraging
        return _database;
    }

    public async Task VoegTaakToeAsync(TodoItem item)
    {
        _database.Add(item);
        await Task.CompletedTask;
    }

    public async Task VerwijderTaakAsync(TodoItem item)
    {
        _database.Remove(item);
        await Task.CompletedTask;
    }
}
```
In een echte app vervang je later `_database` door een echte SQLite-/API-implementatie.

## 2.4 ViewModel koppelen aan Repository (Constructor Injection)

**TodoViewModel met repository**
```csharp
public partial class TodoViewModel : ObservableObject
{
    private readonly ITodoRepository _repository;

    [ObservableProperty]
    private ObservableCollection<TodoItem> taken;

    public TodoViewModel(ITodoRepository repository)
    {
        _repository = repository;
        Taken = new ObservableCollection<TodoItem>();
    }

    public async Task LaadTaken()
    {
        var resultaat = await _repository.HaalAlleTakenOpAsync();
        Taken.Clear();
        foreach (var t in resultaat)
            Taken.Add(t);
    }
}
```
**Let op:** De ViewModel kent alleen `ITodoRepository`, niet `TodoRepository`. We roepen nooit `new TodoRepository()` in de ViewModel. We verwachten dat iets anders (DI) deze parameter injecteert.

## 2.5 Dependency Injection in MauiProgram.cs

We vertellen de app welke implementatie hoort bij welke interface en welke ViewModels/Pages beschikbaar zijn.

```csharp
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    // ... standaard MAUI setup ...

    // 1. Services (Repositories)
    builder.Services.AddSingleton<ITodoRepository, TodoRepository>();

    // 2. ViewModels
    builder.Services.AddTransient<TodoViewModel>();

    // 3. Pages
    builder.Services.AddTransient<MainPage>();

    return builder.Build();
}
```

- `AddSingleton<ITodoRepository, TodoRepository>()`: Voor elke ITodoRepository in de app krijgt iedereen dezelfde TodoRepository instantie.
- `AddTransient<TodoViewModel>()`: Elke keer dat een pagina een TodoViewModel nodig heeft, wordt er een nieuwe gemaakt.

## 2.6 View koppelen via constructor-injectie

**MainPage.xaml.cs**
```csharp
using MijnMauiApp.ViewModels;

public partial class MainPage : ContentPage
{
    public MainPage(TodoViewModel vm)
    {
        InitializeComponent();
        BindingContext = vm;
    }
}
```
De DI-container ziet: “MainPage heeft een TodoViewModel nodig.” Die TodoViewModel heeft een ITodoRepository nodig. DI maakt automatisch een TodoRepository en injecteert alles.

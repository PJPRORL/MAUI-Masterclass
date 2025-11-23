# Hoofdstuk 4 – Complexe Data-interactie: Picker, ObservableCollection & Equals

We breiden het Todo-model uit met categorieën en laten de gebruiker in een Picker een categorie kiezen. Dit is een klassiek punt waar je tegen een probleem botst: objectvergelijking.

## 4.1 Probleem: Picker en objectvergelijking

Stel:
- Je hebt een Picker met een lijst `ObservableCollection<Categorie>`.
- Je toont Naam (“Werk”, “Privé”, …).
- In een TodoItem zit een property `Categorie` die uit de database komt.

Standaard vergelijkt C#: “Zijn deze twee objecten dezelfde referentie in het geheugen?” → nee, dus de SelectedItem wordt niet gezet. De Picker lijkt “leeg”.

**Oplossing:** `Equals` en `GetHashCode` in het Categorie-model overschrijven.

## 4.2 Categorie model met Equals & GetHashCode

**Models/Categorie.cs**
```csharp
namespace MijnMauiApp.Models;

public class Categorie
{
    public int Id { get; set; }
    public string Naam { get; set; }

    public override bool Equals(object obj)
    {
        if (obj is not Categorie andereCategorie)
            return false;
        return Id == andereCategorie.Id;
    }

    public override int GetHashCode()
    {
        return Id.GetHashCode();
    }
}
```
Nu zegt C#: twee Categorie-objecten zijn gelijk als hun Id gelijk is.

## 4.3 TodoItem uitbreiden met Categorie

```csharp
public class TodoItem
{
    public int Id { get; set; }
    public string Titel { get; set; }
    public bool IsAfgerond { get; set; }
    public Categorie Categorie { get; set; }
}
```

## 4.4 ViewModel uitbreiden voor Picker-binding

We hebben nodig:
- Een lijst met alle categorieën (`ObservableCollection<Categorie>`).
- De actuele selectie (`Categorie GeselecteerdeCategorie`).

```csharp
public partial class TodoViewModel : BaseViewModel
{
    // ...
    [ObservableProperty]
    private ObservableCollection<Categorie> categorieen;

    [ObservableProperty]
    private Categorie geselecteerdeCategorie;

    public TodoViewModel(ITodoRepository repository)
    {
        // ...
        LaadCategorieen();
    }

    private void LaadCategorieen()
    {
        Categorieen = new ObservableCollection<Categorie>
        {
            new Categorie { Id = 1, Naam = "Werk" },
            new Categorie { Id = 2, Naam = "Privé" },
            new Categorie { Id = 3, Naam = "Boodschappen" }
        };
        GeselecteerdeCategorie = Categorieen.FirstOrDefault();
    }
    // ...
}
```

## 4.5 Picker binden in XAML

```xml
<VerticalStackLayout Padding="20" Spacing="10">
    <Entry Text="{Binding HuidigeTitel, Mode=TwoWay}"
           Placeholder="Nieuwe taak..." />
           
    <Label Text="Kies een categorie:" />
    
    <Picker Title="Selecteer categorie"
            ItemsSource="{Binding Categorieen}"
            SelectedItem="{Binding GeselecteerdeCategorie, Mode=TwoWay}"
            ItemDisplayBinding="{Binding Naam}" />
            
    <Button Text="Toevoegen"
            Command="{Binding VoegTaakToeCommand}"
            IsEnabled="{Binding IsNotBusy}" />
</VerticalStackLayout>
```

- `ItemsSource` krijgt de lijst.
- `SelectedItem` is gebonden aan `GeselecteerdeCategorie`.
- `ItemDisplayBinding` bepaalt wat de gebruiker ziet (Naam).

Dankzij de `Equals`-implementatie zal de `SelectedItem` correct gezet worden, ook als het object uit de database een andere referentie is dan die in de lijst.

# Hoofdstuk 1 – De Fundering: MVVM & Data Binding

## 1.1 Wat is .NET MAUI?

.NET MAUI (Multi-platform App UI) is de opvolger van Xamarin.Forms. Met één C#-codebase en één projectstructuur kun je native apps bouwen voor:
- Android
- iOS
- Windows
- macOS

Het hart van moderne .NET MAUI-ontwikkeling is het MVVM-patroon. Je stopt met denken in losse event-handlers (zoals `Button_Clicked`) en begint te denken in state (toestand) en bindings tussen View en ViewModel.

## 1.2 MVVM: Model – View – ViewModel

MVVM zorgt voor scheiding van verantwoordelijkheden.

### Model
- Puur data-objecten (bijvoorbeeld Klant, Taak, Categorie).
- Geen UI-logica, geen database-logica.
- “Domme” klassen met properties.

### View (XAML)
- De gebruikersinterface: knoppen, labels, listviews, etc.
- Ziet er mooi uit, maar kent geen C#-logica.
- Toont alleen data via `{Binding ...}`.

### ViewModel
- Het “brein” tussen View en Model.
- Bevat state (eigenschappen) en logica (commando’s) die de View gebruikt.
- Weet niets over de concrete UI-controls (geen Button, geen Label), alleen over properties en commands.

**Waarom is dit belangrijk?**
- Geen spaghetti in `MainPage.xaml.cs`.
- Code wordt testbaar (ViewModel kun je unit-testen).
- Herbruikbare logica, ook als je de UI later vervangt.
- “Loosely coupled”: View en data-laag zijn losjes gekoppeld.

## 1.3 De oude manier: INotifyPropertyChanged handmatig

Vroeger, zonder CommunityToolkit, moest je zelf `INotifyPropertyChanged` implementeren om de View te vertellen: “Deze property is veranderd, werk de UI bij”.

```csharp
// OUDE MANIER (niet meer zo doen)
public class PersoonViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;
    private string _naam;

    public string Naam
    {
        get => _naam;
        set
        {
            if (_naam != value)
            {
                _naam = value;
                OnPropertyChanged(nameof(Naam));
            }
        }
    }

    protected void OnPropertyChanged(string propertyName)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}
```

Voor elke property moest je:
1. Een private field maken.
2. In de setter `OnPropertyChanged` aanroepen.
3. De interface implementeren.

Dat wordt snel veel “boilerplate”.

## 1.4 De moderne manier: CommunityToolkit & ObservableObject

Met `CommunityToolkit.Mvvm` gebruik je:
- `ObservableObject` als basis.
- Attributen zoals `[ObservableProperty]` en `[NotifyPropertyChangedFor]`.
- De compiler genereert de boilerplate-implementatie voor je.

**Voorbeeld: eenvoudige ViewModel**

```csharp
using CommunityToolkit.Mvvm.ComponentModel;

public partial class PersoonViewModel : ObservableObject
{
    // [ObservableProperty] op een private field:
    // - maakt automatisch een public property 'Voornaam'
    // - implementeert OnPropertyChanged achter de schermen
    [ObservableProperty]
    private string voornaam;

    [ObservableProperty]
    private string achternaam;

    // Berekende property (computed)
    public string VolledigeNaam => $"{Voornaam} {Achternaam}";
}
```

**Belangrijk:**
- Je schrijft alleen het private veld en attribuut.
- De toolkit maakt de publieke property en alles van `INotifyPropertyChanged` automatisch.

## 1.5 Eerste Data Binding: View koppelen aan ViewModel

De View moet weten met welke ViewModel hij praat. Dit doe je via de `BindingContext`.

**BindingContext instellen in code-behind**

```csharp
// MainPage.xaml.cs
public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
        BindingContext = new PersoonViewModel();
    }
}
```

**Binding in XAML**

Nu kun je in XAML properties van de ViewModel binden:

```xml
<VerticalStackLayout Padding="30">
    <Entry Text="{Binding Voornaam, Mode=TwoWay}"
           Placeholder="Typ je voornaam" />
    
    <Entry Text="{Binding Achternaam, Mode=TwoWay}"
           Placeholder="Typ je achternaam" />

    <Label Text="{Binding VolledigeNaam}"
           FontSize="Large" />
</VerticalStackLayout>
```

**Binding modes:**
- `OneWay` (standaard bij Label, BoxView, etc.): ViewModel → View. UI past zich aan als de data verandert, maar niet andersom.
- `TwoWay` (standaard bij Entry): ViewModel ⇆ View. Gebruik bij invoervelden (Entry) waar de gebruiker tekst invult die terug de ViewModel in moet.

## 1.6 Concreet mini-project: Groet-voorbeeld

We bouwen een klein scherm dat je naam vraagt en je begroet.

**ViewModel – MainViewModel.cs**
```csharp
using CommunityToolkit.Mvvm.ComponentModel;

namespace MijnMauiApp.ViewModels;

public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(GroetBericht))]
    private string naam;

    public string GroetBericht => string.IsNullOrWhiteSpace(Naam)
        ? "Hallo vreemdeling!"
        : $"Welkom terug, {Naam}!";
}
```

**View – MainPage.xaml**
```xml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MijnMauiApp.MainPage">
    <VerticalStackLayout Spacing="20" Padding="30" VerticalOptions="Center">
        <Label Text="Vul je gegevens in:" FontAttributes="Bold" />
        
        <Entry Text="{Binding Naam, Mode=TwoWay}"
               Placeholder="Typ hier je naam..." />
               
        <BoxView HeightRequest="1" Color="Gray" />
        
        <Label Text="{Binding GroetBericht}"
               FontSize="24"
               TextColor="Purple"
               HorizontalOptions="Center" />
    </VerticalStackLayout>
</ContentPage>
```

**BindingContext – MainPage.xaml.cs**
```csharp
using MijnMauiApp.ViewModels;

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
        BindingContext = new MainViewModel();
    }
}
```

## 1.7 Lijsten tonen: List<T> vs ObservableCollection<T>

**Veel beginnersfout:**
```csharp
// FOUTE MANIER
public List<TodoItem> Taken { get; set; } = new List<TodoItem>();
```
Als je in de ViewModel `Taken.Add(...)` doet, ziet de UI daar niets van. `List` stuurt geen notificatie naar de View.

**Oplossing: ObservableCollection<T>**
```csharp
// GOEDE MANIER
[ObservableProperty]
private ObservableCollection<TodoItem> taken;
```
`ObservableCollection<T>` zit in `System.Collections.ObjectModel`. Als je `Add`, `Remove` of `Clear` gebruikt, zal de UI automatisch updaten.

## 1.8 Compiled Bindings: x:DataType

Standaard moet .NET MAUI tijdens runtime “gokken” of de property bestaat. Dat gebeurt via reflection en is trager en foutgevoelig. Compiled Bindings lossen dit op.

**Voordelen:**
- Performance: bindings worden bij compile-time gecheckt.
- IntelliSense in XAML.
- Compile-time errors als properties niet bestaan.

**Voorbeeld: x:DataType op een pagina**
```xml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:viewmodels="clr-namespace:MijnMauiApp.ViewModels"
             x:Class="MijnMauiApp.MainPage"
             x:DataType="viewmodels:TodoViewModel">
    <CollectionView ItemsSource="{Binding Taken}">
        <!-- ... -->
    </CollectionView>
</ContentPage>
```

**x:DataType in een DataTemplate**
```xml
<DataTemplate x:DataType="models:TodoItem">
    <HorizontalStackLayout>
        <Label Text="{Binding Titel}" />
    </HorizontalStackLayout>
</DataTemplate>
```
Gebruik `x:DataType` altijd waar mogelijk: op pagina’s, data templates, etc.

## 1.9 Value Converters

Soms klopt de type-combinatie niet (bijv. `bool` naar `Color`). Oplossing: `IValueConverter` implementeren.

**Converter klasse – BoolToColorConverter.cs**
```csharp
using System.Globalization;

public class BoolToColorConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is bool isAfgerond && isAfgerond)
            return Colors.Green;
        return Colors.Red;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}
```

**Converter gebruiken in XAML**
```xml
<ContentPage.Resources>
    <local:BoolToColorConverter x:Key="StatusKleurConverter" />
</ContentPage.Resources>

<Label Text="Taak status"
       TextColor="{Binding IsAfgerond, Converter={StaticResource StatusKleurConverter}}" />
```
